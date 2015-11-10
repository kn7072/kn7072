import hashlib
item = 'wqefasfdasddsfadsfsfk;dfkljsdf;asjdflksdjfadskjfasdklfjsdfkjl;aslkfj'
def hash(string):
    return hashlib.md5(str(string).encode()).hexdigest()
print(hash(item))

item2 = 'wqefasfdasddsfadsfsfk;dfkljsdf;asjdflksdjfadskjfasdklfjsdfkjl;aslkfx'
print(hash(item2))