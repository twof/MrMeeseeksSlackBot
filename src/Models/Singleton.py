#!python
# -*- coding: utf-8 -*-


class Singleton(object):
    '''Implemented by plugins. Ensures that plugins are singletons'''
    _instance = None

    @staticmethod
    def __new__(class_, *args, **kwargs):
        '''
        Returns the instance if it exsits and creates a new one if it
        does not
        '''
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
