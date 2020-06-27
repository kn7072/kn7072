import weakref


class Account(object):
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.observers = set()

    def __del__(self):
        for ob in self.observers:
            ob.close()
        del self.observers

    def register(self, observer):
        self.observers.add(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for ob in self.observers:
            ob.update()

    def withdraw(self, amt):
        self.balance -= amt
        self.notify()


class AccountObserver(object):
    def __init__(self, theaccount):
        self.theaccount = weakref.ref(theaccount)  # Создаст слабую ссылку
        theaccount.register(self)

    def __del__(self):
        self.theaccount.unregister(self)
        del self.theaccount

    def update(self):
        print("Баланс: %0.2f" % self.theaccount.balance)

    def close(self):
        print("Наблюдение за счетом окончено")

# Пример создания
a = Account("Дейв", 1000.00)
a_ob = AccountObserver(a)
