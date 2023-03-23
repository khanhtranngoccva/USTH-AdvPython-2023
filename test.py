class Foo:
    @staticmethod
    def class_decorate(func):
        def outer(self, *args, **kwargs):
            print(self.__reallyPrivate)
            func(self, *args, **kwargs)

        return outer

    def __init__(self):
        self.__reallyPrivate = 2

    @class_decorate
    def test(self):
        print("Testing decorator private properties")


test_obj = Foo()
print(test_obj.__dict__)
# test_obj.test()
