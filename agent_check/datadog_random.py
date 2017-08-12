#!/bin/env python3
from random import random
from checks import AgentCheck


class (AgentCheck):

    def check(self, instance):
        try:
            self.gauge('test.support.random', random())
            break
        except Exception as e:
            self.log.info(e)
