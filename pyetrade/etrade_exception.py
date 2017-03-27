#!/usr/bin/python3
'''Custom exceptions for pyetrade'''
class OrderException(Exception):
    def __init__(self, explanation=None, params=None):
        self.required = params
        self.args = (explanation, params, )

    def __str__(self):
        return 'Missing required paramiters'
