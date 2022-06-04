### 1.1 脚本引入
```javascript
<script type="text/javascript" src="xxxx"></script>
```

### 1.2 简写
```html
<script type="text/javascript" src="js/jquery-1.12.4.js"></script>
<script type="text/javascript">
    $(document).ready(function (){
        ...
    });
</script>

<!--或者如下：两种方式一致-->
<script type="text/javascript" src="js/jquery-1.12.4.js"></script>
<script type="text/javascript">
    $(function(){
        ....
    });
</script>
```

### 1.3 操作元素
- 原JavaScript写法
```html
<script type="text/javascript">
    window.onload = function (){
        var oDiv = document.getElementById('div1');
        
        alert("我是老方式哦");
    }
</script>
```
- JQuery写法
```html
<script type="text/javascript" src="js/jquery-1.12.4.js"></script>
<script type="text/javascript">
    $(document).ready(function (){
        var $oDiv = $('#div1');
        alert("这是新方式哦");
    })
</script>

<!--或者-->
<script type="text/javascript" src="js/jquery-1.12.4.js"></script>
<script type="text/javascript">
    $(function (){
        var $oDiv = $('#div1');
        alert("这是新方式哦");
    })
</script>
```
#### 1.3.1 节选部分选择器
- jquery有容错机制，即使没有找到元素，也不会出错，可以用length属性来判断是否找到了元素,length等于0，就是没选择到元素，length大于0，就是选择到了元素。
```html
$('#myId') //选择id为myId的网页元素
$('.myClass') // 选择class为myClass的元素
$('li') //选择所有的li元素
$('#ul1 li span') //选择id为为ul1元素下的所有li下的span元素
$('input[name=first]') // 选择name属性等于first的input元素
```
```html
$('div').has('p'); // 选择包含p元素的div元素
$('div').not('.myClass'); //选择class不等于myClass的div元素
$('div').filter('.myClass'); //选择class等于myClass的div元素
$('div').eq(5); //选择第6个div元素
```
```html
$('div').prev(); //选择div元素前面紧挨的同辈元素
$('div').prevAll(); //选择div元素之前所有的同辈元素
$('div').next(); //选择div元素后面紧挨的同辈元素
$('div').nextAll(); //选择div元素后面所有的同辈元素
$('div').parent(); //选择div的父元素
$('div').children(); //选择div的所有子元素
$('div').siblings(); //选择div的同级元素
$('div').find('.myClass'); //选择div内的class等于myClass的元素
```

#### 1.3.2 操作样式
```html
// 获取div的样式
$("div").css("width");
$("div").css("color");

//设置div的样式
$("div").css("width","30px");
$("div").css("height","30px");
$("div").css({fontSize:"30px",color:"red"});
```

#### 1.3.3 样式名操作
```html
$("#div1").addClass("divClass2") //为id为div1的对象追加样式divClass2
$("#div1").removeClass("divClass")  //移除id为div1的对象的class名为divClass的样式
$("#div1").removeClass("divClass divClass2") //移除多个样式
$("#div1").toggleClass("anotherClass") //重复切换anotherClass样式
```

### 1.4 绑定click事件
```html
选择对象.click(function(){
    // 内部的this指的是原生对象

    // 使用jquery对象用 $(this)
)
```

### 1.5 jQuery特殊效果
```html
fadeIn() 淡入

    $btn.click(function(){

        $('#div1').fadeIn(1000,'swing',function(){
            alert('done!');
        });

    });

fadeOut() 淡出
fadeToggle() 切换淡入淡出
hide() 隐藏元素
show() 显示元素
toggle() 切换元素的可见状态
slideDown() 向下展开
slideUp() 向上卷起
slideToggle() 依次展开或卷起某个元素  
    可能遇到bug，在sildeToggle()前加入stop()即可
```
### 1.6 animate动画
- 参考00007animate.html动画
```html
$('#div1').animate({
    width:300,
    height:300
},1000,'swing',function(){
    alert('done!');
});

$('#div1').animate({
    width:'+=100',
    height:300
},1000,'swing',function(){
    alert('done!');
});
```

### 1.7 尺寸及滚动事件
#### 1.7.1 获取和设置元素的尺寸
- width()、height()    获取元素width和height  
- innerWidth()、innerHeight()  包括padding的width和height
- outerWidth()、outerHeight()  包括padding和border的width和height  
- outerWidth(true)、outerHeight(true)   包括padding和border以及margin的width和height
#### 1.7.2 获取元素相对页面的绝对位置
- offset()
#### 1.7.3 获取浏览器可视区宽度高度
- $(window).width();
- $(window).height();
#### 1.7.4 获取页面文档的宽度高度
- $(document).width();
- $(document).height();
#### 1.7.5 获取页面滚动距离
- $(document).scrollTop();  
- $(document).scrollLeft();
#### 1.7.6 页面滚动事件
    $(window).scroll(function(){  
        ......  
    })

### 1.8 属性操作
- html取出或者设置内容
```html
// 取出html内容

var $htm = $('#div1').html();

// 设置html内容

$('#div1').html('<span>添加文字</span>');
```

- prop取出或者设置某个属性的值
```html
// 取出图片的地址

var $src = $('#img1').prop('src');

// 设置图片的地址和alt属性

$('#img1').prop({src: "test.jpg", alt: "Test Image" });
```

### 1.9 jQuery循环
- 对jQuery选择的对象集合分别进行操作
- each可以对每个内容进行操作
  - 参考000010jQuery循环.html
  - 在使用时可以将每一个内容取到，可以使用$(this).index()来获取索引；也可以使用对应参数来得到。
  
### 1.10 jQuery事件
- 函数事件
```html
blur() 元素失去焦点
focus() 元素获得焦点
click() 鼠标单击
mouseover() 鼠标进入（进入子元素也触发）
mouseout() 鼠标离开（离开子元素也触发）
mouseenter() 鼠标进入（进入子元素不触发）
mouseleave() 鼠标离开（离开子元素不触发）
hover() 同时为mouseenter和mouseleave事件指定处理函数
ready() DOM加载完成
resize() 浏览器窗口的大小发生改变
scroll() 滚动条的位置发生变化
submit() 用户递交表单
```
- 绑定事件的其他方式
```html
$(function(){
    $('#div1').bind('mouseover click', function(event) {
        alert($(this).html());
    });
});
```

- 取消绑定事件
```html
$(function(){
    $('#div1').bind('mouseover click', function(event) {
        alert($(this).html());

        // $(this).unbind();
        $(this).unbind('mouseover');

    });
});
```
### 1.11 事件冒泡
- 什么是事件冒泡
>在一个对象上触发某类事件（比如单击onclick事件），如果此对象定义了此事件的处理程序，那么此事件就会调用这个处理程序，如果没有定义此事件处理程序或者事件返回true，那么这个事件会向这个对象的父级对象传播，从里到外，直至它被处理（父级对象所有同类事件都将被激活），或者它到达了对象层次的最顶层，即document对象（有些浏览器是window）。

- 事件冒泡的作用
>事件冒泡允许多个操作被集中处理（把事件处理器添加到一个父级元素上，避免把事件处理器添加到多个子级元素上），它还可以让你在对象层的不同级别捕获事件。

- 阻止事件冒泡
```html
// 阻止事件冒泡
// event.stopPropagation();
// 阻止默认行为
// event.preventDefault();                                                                                                                                                                                                                                                                                                                                                                                                      

// 合并写法：
return false;
```
### 1.12 事件委托或者事件代理
>事件委托就是利用冒泡的原理，把事件加到父级上，通过判断事件来源的子集，执行相应的操作，事件委托首先可以极大减少事件绑定次数，提高性能；其次可以让新加入的子元素也可以拥有相同的操作。
- delegate 事件委托
```html
// 一般绑定事件的写法

$(function(){
    $ali = $('#list li');
    $ali.click(function() {
        $(this).css({background:'red'});
    });
})

// 事件委托的写法

$(function(){
    $list = $('#list');
    $list.delegate('li', 'click', function() {
        $(this).css({background:'red'});
    });
})

<ul id="list">
    <li>1</li>
    <li>2</li>
    <li>3</li>
    <li>4</li>
    <li>5</li>
</ul>
```
### 1.13 节点操作
- 创建节点
```html
var $div = $("<div>");
var $div1 $("<div>这是创建的节点</div>");
```
- 插入节点
  
  - `append()`和`appendTo()`：在现存元素的内部，从后面插入元素
  ```html
    var $span = $('<span>这是一个span元素</span>');
    $('#div1').append($span);
    ......
    <div id="div1"></div>
  ```
  
  - `prepend()`和`prependTo()`：在现存元素的内部，从前面插入元素

  - `after()`和`insertAfter()`：在现存元素的外部，从后面插入元素

  - `before()`和`insertBefore()`：在现存元素的外部，从前面插入元素

- 删除节点
  
  - $('#div1').remove(); 