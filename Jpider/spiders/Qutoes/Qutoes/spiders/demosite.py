# -*- coding: utf-8 -*-
import scrapy
from faker import Faker
from lxml import etree
import requests
import random
from ..items import ArticleItem,Authoritem,TagItem
import time

class DemositeSpider(scrapy.Spider):
    name = 'demosite'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def __init__(self):
        faker=Faker()
        self.host_url='http://quotes.toscrape.com{}'
        self.headers={
            'User-Agent':faker.user_agent(),
        }
        # self.Au=Authoritem()
        # self.Ar=ArticleItem()
        # self.Ta=TagItem()

    def parse(self, response):
        titles=response.xpath(".//span[@class='text']/text()").extract()
        authors=response.xpath(".//small[@class='author']/text()").extract()
        tags_name=list(set(response.xpath(".//a[@class='tag']/text()").extract()))
        details=response.xpath(".//div[@class='quote']//span[2]/a/@href").extract()
        for x,y,z in zip(titles,authors,details):
            Au = Authoritem()
            Ar = ArticleItem()
            Ta = TagItem()
            Ar['title']=x
            Au['name']=y
            Ta['name']=random.choice(tags_name)
            print(type(z))
            print(self.host_url.format(z))
            Ar['body'],Au['born_date'],Au['born_location'] =self.parser_details(self.host_url.format(z))
            # scrapy.Request(url=self.host_url.format(z),headers=self.headers,callback=self.parser_details)
            try:
                Au.save()
                Ar.save()
                Ta.save()
            except:
                pass
            # self.Au.save()
            # self.Ta.save()
            # self.Ar.save()
        next_link=''.join(response.xpath(".//li[@class='next']/a/@href").extract())
        print(next_link)
        print(self.host_url.format(next_link))
        if next_link:
            yield scrapy.Request(url=self.host_url.format(next_link),callback=self.parse,headers=self.headers)

    def parser_details(self,url):
        response=requests.get(url)
        content=response.content.decode()
        html=etree.HTML(content)
        born_date=''.join(html.xpath(".//span[@class='author-born-date']/text()"))
        born_location=''.join(html.xpath(".//span[@class='author-born-location']/text()"))
        body=''.join(html.xpath(".//div[@class='author-description']/text()"))
        return body,born_date,born_location
        # Ta=response.meta.get('Ta')
        # Au = Authoritem()
        # Ar = ArticleItem()
        # Au['born_date']=''.join(response.xpath(".//span[@class='author-born-date']/text()").extract())
        # # print('**********')
        # # print(Au['born_date'])
        # # print('**********')
        # Au['born_location']=''.join(response.xpath(".//span[@class='author-born-location']/text()").extract())
        # Ar['body']=''.join(response.xpath(".//div[@class='author-description']/text()").extract())

