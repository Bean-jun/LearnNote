file = io.open("lua_module.lua", 'r')
-- file.read()
-- 设置读文件
io.input(file)
-- 设置写文件
-- io.output(file)

print(io.read())
print(io.read())
print(io.read())
-- 使用完全模式 替代io.input或io.output 使用io操作的方法
print(file:read())
io.close()