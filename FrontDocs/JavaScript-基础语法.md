### 1.1 脚本引入
- 内联
	
	- 直接在行间写入
- 内嵌
	```html
	<script type="text/javascript"></script>
	```
- 外联
	```html
	<script type="text/javascript" src="地址"></script>
	```

### 1.2 变量
- 使用规范
	
	区分大小写
	
	首字符必须是字母、下划线或者$
	
	其他字符可以是字母、下划线或者$、数字
	
定义变量需要使用关键字`var`.
```html
var iNum = 45;
```
- 数据类型
  
	数字类型 number
  
	字符串类型 string

	布尔类型 boolean

	undefined类型 undefined

	null类型 null ----- 一般在页面中获取不到就为null

- 类型转换
```html
parseInt()  将内容转换为整数
parseFloat() 将内容转换为小数
```
- 变量的作用域

	函数外面的变量在任何范围都可以访问。并且可以直接修改。

	函数内部的变量只能在函数内部使用。

### 1.3 获取元素
- document.getElementById(id名称)
```html
var oDiv = document.getElementById('div1');

oDiv.style.color = 'green';
oDiv.style.fontSize = '30px';
```
- document.getElementsByTagName("li")

	这种方式获取到的内容是一个结果集，`基本`可以像数组一样操作

### 1.4 操作元素属性
- 操作方式
	- 使用.   【针对变量不可以】
	- 使用[]	   【专门针对js的变量使用】
	
- 属性写法
	- html中的属性基本和js一致
	- class要写成className
	- style中加-的要改为驼峰式
	
- 修改html中内嵌的内容
	 - innerHTML
	```html
		<!-- 	读取-->
		var oDiv = document.getElementById('div1');
		var sTr = oDiv.innerHTML;
 		alert(sTr);
		<!--    修改-->
		oDiv.innerHTML = "我裂开了";
	```
 
### 1.5 函数
#### 1.5.1 基本定义
```html
<!--基本定义-->
function myFunction()
{
    alert("Hello World!");
}
<!--调用函数-->
myFunction();
```

#### 1.5.2 提取行间事件
```html
<script type="text/javascript">
	window.onload = function (){
		var oBtn = document.getElementById('div1')

		oBtn.onclick = fnChange;

		function fnChange(){
			var oDiv = document.getElementById('div1');
			oDiv.style.color = "red";
			oDiv.fonSize = "30px";
			}
	}
</script>

<div class="box"  id="div1">哈哈哈哈</div>
```
#### 1.5.3 匿名函数
不给函数名称，及那个函数直接赋值给元素绑定的事件。
```html
<script type="text/javascript">
	window.onload = function (){
		var oBox = document.getElementById('box1')
		oBox.onclick = function(){
			oBox.style.color = 'red';
		}
	}
</script>
```
注意看上面的
```
oBox.onclick = function(){
	oBox.style.color = 'red';
}
```
#### 1.5.4 函数传参
```html
function fnChange(mystyle, val){
	var oDiv  = document.getElementById("div1");
	oDiv.style[mystyle] = val;
}
<div id="div1" onclick="fnChange('color','red')">这是div哦</div>
```
#### 1.5.5 返回值
- return 关键字
	 - 返回函数的运行结果
	 - 结束函数的执行
```html
function fnAdd(a, b){
	return a+b;
}
alert(fnAdd(1, 3));
```

### 1.6 条件语句
`==`和`===`的区别

	== 是用来判断内容是否相等
	=== 是先比较两边数据的类型，然后在比较内容

条件语句在使用上和C++类似，条件需要加上()

#### 1.6.1 if
```html
if (3<4){
	alert("ok");
}
```
#### 1.6.2 if...else
```html
if (3>4){
	alert("1");
}
else{
	alert("2");
}


if (3>4){
	alert("1");
}
else if (3 > 10){
	alert("2");
}
else{
	alert("3");
}
```
#### 1.6.3 switch
```html
var iNum = 3;
switch (iNum){
	case 1:
		...;
		break;
	case 2:
		...;
		break;
	.....
	default:
		...;
		break;
}
```
### 1.7 数组
#### 1.7.1 创建方式
- 使用对象创建
var aList = new Array(1,2,3);
  
- 直接创建
var aList = [1, 2, 3]
  
#### 1.7.2 操作数据的方式
- 获取长度
aList.length;
  
- 获取某一个内容
aList[]
  
- join()将数组成员拼接为一串字符串
aList.join('-')
	```html
	var aList = [1,2,3,4]
	alert(aList.join('-')
	```
- push()和pop()
	```html
	var aList = [1,2,3,4];
	aList.push(5); aList数组中变为 1,2,3,4,5
	aList.pop();  aList数组中变为 1,2,3,4
	```

- unshift()和 shift() 
	```html
	var aList = [1,2,3,4];
	aList.unshift(5); aList数组中变为5,1,2,3,4
	aList.shift(); aList数组中变为1,2,3,4
	```
 
- reverse() 将数组反转
	```html
	aList.reverse()
	```
- indexOf() 返回数组中元素第一次出现的索引值
	```html
	aList.indexOf(xxx)
	```
 
- splice() 在数组中增加或删除成员
	```html
	var aList = [1,2,3,4];
	aList.splice(2,1,7,8,9); //从第2个元素开始，删除1个元素，然后在此位置增加'7,8,9'三个元素
	alert(aList); //弹出 1,2,7,8,9,4
	```
 #### 1.7.3 多维数组
- 实例
var aList = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
  
### 1.8 循环
- for 循环
```html
for(var i = 0;i<9;i++){
	
}
``` 
- while循环
```html
var i= 0；
while (i<8){
	i++;	
}	
```
- break
- continue

### 1.9 字符串
- split() 分割
- charAt() 获取字符串中的某一个字符
- indexOf() 获取内容是否存在，存在则返回索引，不存在返回-1
- substring(start,end) 类似于Python的切片
- toUpperCase() 转换为大写
- toLowerCase() 转换为小写


### 1.10 调试程序的方法
- alert 直接弹出
- console.log 显示在控制台
- document.title 显示在标题栏

### 1.11 定时器
- 功能
	- 制作动画
	- 异步操作
	- 函数缓存与节流
	
- 使用方式
	```html
	定时器
	setTimeout 只执行一次的定时器
	clearTimeout 关闭只执行一次的定时器
	
	setInterval 反复执行定时
	clearInterval 关闭反复执行的定时器
	```
 
- 具体方式
	- setTimeout(函数名, 时间[单位：毫秒])
	- 要关闭,需要将定时器和变量关联，然后关闭
	```html
	function fnTest(){
		alert("hello world");
	}
	var timer01 = setTimeout(fnTest, 1000);

	// 关闭只执行一次的定时器
	clearTimeout(timer01);
 	```
 	
	- 关于反复执行的定时器，使用方式和单次定时的内容一致
	
### 1.12 鼠标事件
- 对象.onmouseover 鼠标移入
- 对象.onmouseout 鼠标移出

### 1.13 封闭函数
- 封闭函数是javascript中匿名函数的另外一种写法，创建一个一开始就执行而不用命名的函数。
	```html
	一般定义的函数和执行函数：
	function myalert(){
		alert('hello!');
	};
	myalert();
 
	封闭函数：	
	(function myalert(){
		alert('hello!');
	})();
 
	还可以在函数定义前加上“~”和“!”等符号来定义匿名函数
	!function myalert(){
		alert('hello!');
	}()
	```
 - 封闭函数可以创造一个独立的空间，在封闭函数内定义的变量和函数不会影响外部同名的函数和变量，可以避免命名冲突，在页面上引入多个js文件时，用这种方式添加js文件比较安全

### 1.14 内置方法
- Date()  获取时间
- document.referrer 存储上一个页面的地址
- window.location对象
	- href 获取或者重定向链接
	- search 获取地址参数部分 获取？后的内容
	- hash 获取页面的hash值  获取# 后的内容
- Math对象
	- Math.random 获取0-1的随机数
	- Math.floor 向下取整
	- Math.ceil 向上取整