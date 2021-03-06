from enum import Enum, unique
from string import capwords
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class HtmlContent(models.Model):
    url = models.TextField()
    name = models.CharField(max_length=30, unique=True)
    scraping_strategy = models.IntegerField()
    outer_content_selector = models.TextField(null=True, blank=True)
    inner_content_selector = models.TextField(null=True, blank=True)
    title_selector = models.TextField(null=True, blank=True)
    ignore_first_n_posts = models.IntegerField(default=0)
    ignore_last_n_posts = models.IntegerField(default=0)
    date_parsing_strategy = models.IntegerField(default=0)
    date_selector = models.TextField(null=True, blank=True)
    time_selector = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    users = models.ManyToManyField(User)

    def clean_fields(self, exclude=None):
        if self.scraping_strategy != ScrapingStrategy.atom_feed.value:
            required_html_fields = ('outer_content_selector', 'inner_content_selector', 'title_selector', 'date_selector')
            for f in self._meta.fields:
                if f.name in required_html_fields:
                    f.blank = False

        super(HtmlContent, self).clean_fields(exclude)


class HtmlContentForm(ModelForm):
    class Meta:
        model = HtmlContent
        fields = ['url', 'name', 'scraping_strategy', 'outer_content_selector', 'inner_content_selector', 'title_selector', 'ignore_first_n_posts', 'ignore_last_n_posts',
                  'date_selector', 'time_selector']


@unique
class ScrapingStrategy(Enum):
    element_per_news_entry = 1
    news_entries_listed_in_containing_element = 2
    atom_feed = 3

    def get_display_text(self):
        return capwords(self.name, '_').replace('_', ' ')

    def __str__(self):
        return self.get_display_text()

    @staticmethod
    def get_all_sorted_by_display_string():
        return sorted([scraping_strategy[1] for scraping_strategy in ScrapingStrategy.__members__.items()], key=ScrapingStrategy.__str__)


class QuickSidebarItem():
    def __init__(self, news_source_id, news_source_name, checked):
        self.news_source_id = news_source_id
        self.news_source_name = news_source_name
        self.checked = checked