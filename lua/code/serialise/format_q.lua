local a = 'a "problematic" \\string'
print(string.format("%q", a))
io.write(string.format("%q", a))
