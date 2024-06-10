local dog = {}

local mt = {
    __index = dog
}

-- dog.eat(self) 可以简化为dog:eat()  其中self可以不写，在函数内部可以直接使用
function dog.eat(self)
    print("dog eat", self)
end

function dog:sleep()
    print("dog sleep", self)
end

function dog.work()
    print("dog work")
end

function dog.new(self)
    -- 通过元表，将dog new出去
    return setmetatable(self, mt)
end


local mydog = dog:new()
mydog:eat()
-- 或者这样调用
dog.eat(mydog)

local mydog2 = dog.new(dog)
mydog2:eat()
-- 或者这样调用
dog.eat(mydog2)


-- : 面向对象的写法，会自动传入self
-- . 非面向对象写法，需要手动传入self对象