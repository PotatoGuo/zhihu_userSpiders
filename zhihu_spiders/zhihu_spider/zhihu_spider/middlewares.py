# -*- coding: utf-8 -*-

import random

from cookies import cookies
from user_agents import agents

class CookiesMiddleware(object):
    """添加cookie"""
    def process_request(self, request, spider):
        request.cookies = random.choice(cookies)

class AgentMiddleware(object):
    """添加user-agent"""
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(agents)
