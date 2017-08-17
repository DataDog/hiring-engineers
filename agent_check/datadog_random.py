#!/bin/env python3
from random import random
from checks import AgentCheck


class RandomTest(AgentCheck):

    def check(self, instance):
        self.gauge('test.support.random', random())
