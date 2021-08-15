# 使用with对文件操作
with open('log.txt', 'r', encoding='utf-8') as f:
    data = f.read()

print(data)

# 不使用with也可以对文件操作
fObj = open('log.txt', 'r', encoding='utf-8')
data_content = fObj.read()
fObj.close()
print(data_content)
