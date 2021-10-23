"""
A-Z: 65-90
a-z: 97-122
"""
dic = {}
n = 0
for i in range(10):
    dic[n] = str(i)
    n += 1


for i in range(65, 91):
    dic[n] = chr(i)
    n += 1


for i in range(97, 123):
    dic[n] = chr(i)
    n += 1


print(dic)
