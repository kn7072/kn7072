class MetaClass(type):
    """
    Описание принимаемых параметров:

    mcs – объект метакласса, например <__main__.MetaClass>
    name – строка, имя класса, для которого используется
      данный метакласс, например "User"
    bases – кортеж из классов-родителей, например (SomeMixin, AbstractUser)
    attrs – dict-like объект, хранит в себе значения атрибутов и методов класса
    cls – созданный класс, например <__main__.User>
    extra_kwargs – дополнительные keyword-аргументы переданные в сигнатуру класса
    args и kwargs – аргументы переданные в конструктор класса
      при создании нового экземпляра
    """
    def __new__(mcs, name, bases, attrs, **extra_kwargs):
        print("__new__1")
        obj = super().__new__(mcs, name, bases, attrs)
        print("__new__2")
        return obj

    def __init__(cls, name, bases, attrs, **extra_kwargs):
        print("__init__1")
        super().__init__(cls)
        print("__init__2")

    @classmethod
    def __prepare__(mcs, cls, bases, **kwargs):
        print("__prepare__1")
        res = super().__prepare__(mcs, cls, bases, **kwargs)
        print("__prepare__2")

        res.update({"pr": "pr"})
        return res

    def __call__(cls, *args, **kwargs):
        print("__call__1")
        res = super().__call__(*args, **kwargs)
        print("__call__2")
        return res


class User(metaclass=MetaClass):

    def __new__(cls, name):
        print("__new__1_user")
        obj = super().__new__(cls)
        print("__new__2_user")
        return obj

    def __init__(self, name):
        print("__init__1_user")
        self.name = name


user = User(name='Alyosha')  # MetaClass.__call__(name='Alyosha')
"""
1 В момент вызова User(...) интерпретатор вызывает метод MetaClass.__call__(name='Alyosha'), куда передает объект класса и переданные аргументы.
2 MetaClass.__call__ вызывает User.__new__(name='Alyosha') – метод-конструктор, который создает и возвращает экземпляр класса User
3 Далее MetaClass.__call__ вызывает User.__init__(name='Alyosha') – метод-инициализатор, который добавляет новые атрибуты к созданному экземпляру.
4 MetaClass.__call__ возвращает созданный и проинициализированный экземпляр класса User.
5 В этот момент экземпляр класса считается созданным.
"""
user.pr
user