s = "abbaabba"
s = "abcdabscabcdabia"
p = [0]*len(s)

for i in range(1, len(s)):
    print(s[i])
    if s[i] == s[p[i-1]]:
        p[i] = p[i-1] + 1
    else:
        j = p[i-1]
        while j:
            if s[j] == s[i]:
                p[i] = j + 1
                break
            else:
                j = p[j-1] 
        if s[i] == s[0]:
            p[i] = 1
print(p)                   