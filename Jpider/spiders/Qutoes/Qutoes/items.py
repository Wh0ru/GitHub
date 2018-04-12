# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from spiders.models import Article,Author,Tag
from scrapy_djangoitem import DjangoItem


class QutoesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Authoritem(DjangoItem):
    django_model = Author

class ArticleItem(DjangoItem):
    django_model = Article

class TagItem(DjangoItem):
    django_model = Tag
