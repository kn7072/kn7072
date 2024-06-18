Account = {balance = 100}

function Account:withdraw(v) self.balance = self.balance - v end

Account.withdraw(Account, 10)
Account:withdraw(10)
print(string.format("total %d", Account.balance))

a2 = {balance = 333, withdraw = Account.withdraw}
a2:withdraw(33)
print(string.format("a2 total %d", a2.balance))
