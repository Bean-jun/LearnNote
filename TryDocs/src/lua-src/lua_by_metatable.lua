local mytable_metatable = {}

-- 为表设置元（类似python中的魔法方法）
mytable_metatable.__tostring = function(t)
    local strs = ""
    for i, v in pairs(t) do
        -- 字符串拼接
        strs = strs .. i
        strs = strs .. v
    end
    return strs
end

-- 自定义一个表
a = {4, 1, 3}
-- 为自定义表绑定元表
setmetatable(a, mytable_metatable)
-- 尝试tostring方法
print(a)
