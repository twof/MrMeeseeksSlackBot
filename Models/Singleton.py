class Singleton(object):
    _instance = None

    @staticmethod
    def __new__(class_, *args, **kwargs):
        print(class_._instance)
        print(class_)
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            return class_._instance
        else:
            return class_._instance
