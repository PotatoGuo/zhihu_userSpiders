# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class PeopleItem(Item):
    _id = Field()
    name = Field()
    gender = Field()
    introduction = Field()
    location = Field()
    industry = Field()
    position = Field()
    education = Field()
    description = Field()
    sinaweibo = Field()
    agree = Field()
    thanks = Field()
    marked = Field()
    logs = Field()
    followees = Field()
    followers = Field()
    asks = Field()
    answers = Field()
    posts = Field()
    collections = Field()
    employment = Field()
    column_num = Field()
    topic_num = Field()

class OrgItem(Item):
    _id = Field()
    name = Field()
    followees = Field()
    followers = Field()
    introduction = Field()
    description = Field()
    marked = Field()
    industry = Field()
    company = Field()
    org_url = Field()
    column_num = Field()
    topic_num = Field()
