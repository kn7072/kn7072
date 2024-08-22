Account = {
    balance = 0,
    withdwraw = function(self, v) self.balance = self.balance - v end
}

function Account:deposit(v) self.balance = self.balance + v end

Account:deposit(1000)
Account:withdwraw(100)
print(string.format("total balance %d ", Account.balance))
