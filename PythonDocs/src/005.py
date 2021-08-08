# for循环
for i in range(10):
    print(i)

# while循环
flag = True
a = 0
while True:
    if flag is False:
        break
    a += 1
    print('哈' * a, "!")
    if a > 6:
        flag = False
