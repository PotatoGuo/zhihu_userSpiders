# -*- coding: utf-8 -*-

from zhihu_spider2.bloomfilter_redis.spiders import RedisCrawlSpider
from scrapy.selector import Selector
from scrapy import Request
import re
import json
import requests

from zhihu_spider2.items import PeopleItem, OrgItem

class Spider(RedisCrawlSpider):
    name = 'userSpider'
    redis_key = 'user:start_urls'

    def parse(self, response):
        print response.url
        followers_num = 0
        followees_num = 0
        _id = response.url.split('/')[4]
        is_org = response.url.split('/')[3] == 'org'
        if is_org:
            org_item = OrgItem(_id = _id,
                                description = '',
                                marked = '',
                                industry = '',
                                company = '',
                                org_url = '',
                                column_num = '',
                                topic_num = '',
                                )
            items_div = response.xpath("//div[@class='items']").extract_first()
            org_item['name'] = response.xpath("//span[@class='name']/text()").extract_first()#用户名
            org_item['introduction'] = response.xpath("//div[@class='bio ellipsis']/text()").extract_first()#简介
            org_item['followees'] = response.xpath("//a[@href='/org/%s/followees']/strong/text()" % _id).extract_first().strip()#关注了
            followees_num = int(org_item['followees'])
            org_item['followers'] = response.xpath("//a[@href='/org/%s/followers']/strong/text()" % _id).extract_first().strip()#关注者
            followers_num = int(org_item['followers'])
            if response.xpath("//textarea[@name='description']/text()"):
                org_item['description'] = response.xpath("//textarea[@name='description']/text()").extract_first()#个人描述
            if response.xpath("//div[@class='zm-profile-header-marked']/a"):
                org_item['marked'] = response.xpath("//div[@class='zm-profile-header-marked']/a/text()").extract_first()
            if response.xpath("//div[@class='items']/div[@class='item editable-group']/i[@class='icon sprite-global-icon-industry']"):
                org_item['industry'] = re.search(re.compile(u'industry.+?<span>(.+?)</span>', re.S), items_div).group(1)#行业
            if response.xpath("//div[@class='items']/div[@class='item editable-group']/i[@class='icon icon-profile-company']"):
                org_item['company'] = re.search(re.compile(u'company.+?<span>(.+?)</span>', re.S), items_div).group(1)#公司
            if response.xpath("//div[@class='items']/div[@class='item editable-group']/i[@class='icon zm-profile-header-icon']"):
                org_item['org_url'] = re.search(re.compile(u'<a.+?>(.+?)</a>', re.S), items_div).group(1)#网址
            if response.xpath("//a[@href='/org/%s/columns/followed']/strong" % _id):
                org_item['column_num'] = response.xpath("//a[@href='/org/%s/columns/followed']/strong/text()" % _id).extract_first()#专栏数
            if response.xpath("//a[@href='/org/%s/topics']/strong" % _id):
                org_item['topic_num'] = response.xpath("//a[@href='/org/%s/topics']/strong/text()" % _id).extract_first()#话题数
            yield org_item
        else:
            people_item = PeopleItem(_id = _id,
                                    location = '',
                                    industry = '',
                                    employment = '',
                                    position = '',
                                    education = '',
                                    description = '',
                                    sinaweibo = '',
                                    agree = '',
                                    thanks = '',
                                    marked = '',
                                    logs = '',
                                    column_num = '',
                                    topic_num = '',
                                    )
            people_item['followees'] = response.xpath("//a[@href='/people/%s/followees']/strong/text()" % _id).extract_first().strip()#关注了
            followees_num = int(people_item['followees'])
            people_item['followers'] = response.xpath("//a[@href='/people/%s/followers']/strong/text()" % _id).extract_first().strip()#关注者
            followers_num = int(people_item['followers'])
            people_item['asks'] = response.xpath("//a[@href='/people/%s/asks']/span[@class='num']/text()" % _id).extract_first().strip()#提问数
            people_item['answers'] = response.xpath("//a[@href='/people/%s/answers']/span[@class='num']/text()" % _id).extract_first().strip()#回答数
            people_item['posts'] = response.xpath("//a[@href='/people/%s/posts']/span[@class='num']/text()" % _id).extract_first().strip()#文章数
            people_item['collections'] = response.xpath("//a[@href='/people/%s/collections']/span[@class='num']/text()" % _id).extract_first().strip()#收藏数
            people_item['name'] = response.xpath("//span[@class='name']/text()").extract_first()#用户名
            people_item['gender'] = response.xpath("//input[@name='gender'][@checked='checked']/@class").extract_first()#性别
            people_item['introduction'] = response.xpath("//div[@class='bio ellipsis']/text()").extract_first()#简介
            if response.xpath("//a[@href='/people/%s/logs']/span[@class='num']/text()" % _id):
                people_item['logs'] = response.xpath("//a[@href='/people/%s/logs']/span[@class='num']/text()" % _id).extract_first()#公共编辑数
            if response.xpath("//span[@class='zm-profile-header-user-agree']/strong/text()"):
                people_item['agree'] = response.xpath("//span[@class='zm-profile-header-user-agree']/strong/text()").extract_first().strip()#总赞数
            if response.xpath("//span[@class='zm-profile-header-user-thanks']/strong/text()"):
                people_item['thanks'] = response.xpath("//span[@class='zm-profile-header-user-thanks']/strong/text()").extract_first().strip()#感谢数
            if response.xpath("//span[@class='location item']/a/text()"):
                people_item['location'] = response.xpath("//span[@class='location item']/a/text()").extract_first()#居住地
            if response.xpath("//span[@class='business item']/a/text()"):
                people_item['industry'] = response.xpath("//span[@class='business item']/a/text()").extract_first()#所在行业
            if response.xpath("//span[@class='employment item']/a/text()"):
                people_item['employment'] = response.xpath("//span[@class='employment item']/a/text()").extract_first()#职业
            if response.xpath("//span[@class='position item']/a/text()"):
                people_item['position'] = response.xpath("//span[@class='position item']/a/text()").extract_first()#岗位
            if response.xpath("//span[@class='education item']/a/text()"):
                people_item['education'] = response.xpath("//span[@class='education item']/a/text()").extract_first()#教育
                if response.xpath("//span[@class='education-extra item']/a/text()"):
                    people_item['education'] = people_item['education'] + u'.' + response.xpath("//span[@class='education-extra item']/a/text()").extract_first()
            elif response.xpath("//span[@class='education-extra item']/a/text()"):
                people_item['education'] = response.xpath("//span[@class='education-extra item']/a/text()").extract_first()
            if response.xpath("//textarea[@name='description']/text()"):
                people_item['description'] = response.xpath("//textarea[@name='description']/text()").extract_first()#个人描述
            if response.xpath("//a[@class='zm-profile-header-user-weibo']/@href"):
                people_item['sinaweibo'] = response.xpath("//a[@class='zm-profile-header-user-weibo']/@href").extract_first()#新浪微博
            if response.xpath("//div[@class='zm-profile-header-marked']/a"):
                people_item['marked'] = response.xpath("//div[@class='zm-profile-header-marked']/a/text()").extract_first()#被编辑推荐收录了
            if response.xpath("//a[@href='/people/%s/columns/followed']/strong" % _id):
                people_item['column_num'] = response.xpath("//a[@href='/people/%s/columns/followed']/strong/text()" % _id).extract_first()#专栏数
            if response.xpath("//a[@href='/people/%s/topics']/strong" % _id):
                people_item['topic_num'] = response.xpath("//a[@href='/people/%s/topics']/strong/text()" % _id).extract_first()#话题数
            yield people_item
        yield Request(url = response.url + '/followees', meta = {'followees_num': followees_num}, callback = self.parse_followees)
        #yield Request(url = response.url + '/followers', meta = {'followers_num': followers_num}, callback = self.parse_followers)

    def parse_followees(self, response):
        followees_num = response.meta['followees_num']
        urls = set()
        for url in response.xpath("//a[@class='zg-link author-link']/@href").extract():
            urls.add(url)
        if followees_num > 20:
            """获取ajax内容"""
            data = response.xpath("//div[@class='zh-general-list clearfix']/@data-init").extract_first()
            ajax_url = 'https://www.zhihu.com/node/%s' % json.loads(data).pop('nodename')
            times = followees_num // 20
            if followees_num % 20 == 0:
                for i in range(times - 1):
                    form_data = json.loads(data)
                    form_data.pop('nodename')
                    form_data['method'] = 'next'
                    form_data['params']['offset'] = 20*(i + 1)
                    form_data['params'] = json.dumps(form_data['params'])
                    rep = self.ajax_request(data = form_data, url = ajax_url, response = response)
                    texts = json.loads(rep.text)['msg']
                    for text in texts:
                        href = re.search(re.compile(u'zm-item-link-avatar.+?href=\"(.+?)\"', re.S), text).group(1)
                        url = 'https://www.zhihu.com%s' % href
                        urls.add(url)
            else:
                for i in range(times):
                    form_data = json.loads(data)
                    form_data.pop('nodename')
                    form_data['method'] = 'next'
                    form_data['params']['offset'] = 20*(i + 1)
                    form_data['params'] = json.dumps(form_data['params'])
                    rep = self.ajax_request(data = form_data, url = ajax_url, response = response)
                    texts = json.loads(rep.text)['msg']
                    for text in texts:
                        href = re.search(re.compile(u'zm-item-link-avatar.+?href=\"(.+?)\"', re.S), text).group(1)
                        url = 'https://www.zhihu.com%s' % href
                        urls.add(url)
        for url in urls:
            yield Request(url = url, callback = self.parse)

    def parse_followers(self, response):
        followers_num = response.meta['followers_num']
        urls = set()
        for url in response.xpath("//a[@class='zg-link author-link']/@href").extract():
            urls.add(url)
        if followers_num > 20:
            """获取ajax内容"""
            data = response.xpath("//div[@class='zh-general-list clearfix']/@data-init").extract_first()
            ajax_url = 'https://www.zhihu.com/node/%s' % json.loads(data).pop('nodename')
            times = followers_num // 20
            if followers_num % 20 == 0:
                for i in range(times - 1):
                    form_data = json.loads(data)
                    form_data.pop('nodename')
                    form_data['method'] = 'next'
                    form_data['params']['offset'] = 20*(i + 1)
                    form_data['params'] = json.dumps(form_data['params'])
                    rep = self.ajax_request(data = form_data, url = ajax_url, response = response)
                    texts = json.loads(rep.text)['msg']
                    for text in texts:
                        href = re.search(re.compile(u'zm-item-link-avatar.+?href=\"(.+?)\"', re.S), text).group(1)
                        url = 'https://www.zhihu.com%s' % href
                        urls.add(url)
            else:
                for i in range(times):
                    form_data = json.loads(data)
                    form_data.pop('nodename')
                    form_data['method'] = 'next'
                    form_data['params']['offset'] = 20*(i + 1)
                    form_data['params'] = json.dumps(form_data['params'])
                    rep = self.ajax_request(data = form_data, url = ajax_url, response = response)
                    texts = json.loads(rep.text)['msg']
                    for text in texts:
                        href = re.search(re.compile(u'zm-item-link-avatar.+?href=\"(.+?)\"', re.S), text).group(1)
                        url = 'https://www.zhihu.com%s' % href
                        urls.add(url)
        for url in urls:
            yield Request(url = url, callback = self.parse)

    def ajax_request(self, url, data, response):
        """伪装headers"""
        _xsrf = response.xpath("//input[@name='_xsrf']/@value").extract_first()
        headers = {}
        headers['User-Agent'] = response.request.headers['User-Agent']
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['X-Xsrftoken'] = _xsrf
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        headers['Accept'] = '*/*'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
        headers['Connection'] = 'keep-alive'
        session = requests.Session()
        rep = session.request(method = 'post', url = url, data = data, cookies = response.request.cookies, headers = headers)
        return rep
