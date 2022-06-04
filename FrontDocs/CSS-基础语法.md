### 1.1 引入css的方式
（在html的head引入）
- 外联式：通过link标签，链接到外部样式表到页面中。
```html
# 这种需要在外部创建css的文件
<link rel="stylesheet" type="text/css" href="css/main.css">
```
- 嵌入式：通过style标签，在网页上创建嵌入的样式表。
```html
<style type="text/css">
    div{ width:100px; height:100px; color:red }
    ......
</style>
```
- 内联式：通过标签的style属性，在标签上直接写样式。（一般不推荐）

### 1.2 常用文本样式
- color 设置颜色
- font-size 设置文字大小
- font-family 设置文字的字体
- font-style 设置字体是否倾斜
    - normal 不倾斜
    - italic 倾斜
- font-weight 设置是否加粗
    - bold 加粗
    - normal 不加粗
- line-height 设置文字行高
- font 可以设置文字的属性  请按顺序来
    - 是否加粗、字号/行高 字体
- text-decoration 设置文字的下划线
    - underline 加下划线
    - none 去掉下划线
- text-indent 设置文字首行缩进
- text-align 设置文字水平对齐

### 1.2 css样式选择器
- 标签选择器
    - 影响范围大，一般用于层级选择器中
- id选择器
    - 通过id来选择元素，元素的id值不可以重复，但是一般不推荐
- 类选择器
    - 通过类名选择元素 使用较多
```html
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
    <title>Document</title>
    <style>
        .small{
            font-size: 40px;
        }
    </style>
</head>
<body>
    <div class="small">
        这是一个类选择器实现的样式效果。
    </div>
</body>
</html>
```
- 层级选择器
    - 定义在类选择器或者标签选择器下
```html
# 例如如下代码
.box span{color:red}
.box .red{color:pink}
.red{color:red}

<div class="box">
    <span>....</span>
    <a href="#" class="red">....</a>
</div>

<h3 class="red">....</h3>
```
- 组选择器 多个选择器，如果有同样的样式设置，可以使用组选择器节省代码
```html
.box1,.box2,.box3{width:100px;height:100px}
.box1{background:red}
.box2{background:pink}
.box2{background:gold}

<div class="box1">....</div>
<div class="box2">....</div>
<div class="box3">....</div>
```
- 伪类及伪类元素选择器
    - 常用的伪类选择器有hover，表示鼠标悬浮在元素上时的状态，
    - 伪元素选择器有before和after,它们可以通过样式在元素中插入内容。
```html
.box1:hover{color:red}
.box2:before{content:'行首文字';}
.box3:after{content:'行尾文字';}


<div class="box1">....</div>
<div class="box2">....</div>
<div class="box3">....</div>
```
### 1.3盒子模型
- 关键词
  - padding 填充 直接设置时，是顺时针方向
  - border 边框
  - margin 盒子之间的距离
- 设置宽高
```html
width:200px;  /* 设置盒子的宽度，此宽度是指盒子内容的宽度，不是盒子整体宽度(难点) */ 
height:200px; /* 设置盒子的高度，此高度是指盒子内容的高度，不是盒子整体高度(难点) */
```
- 设置边框 border
```html
border-top-color:red;    /* 设置顶部边框颜色为红色 */  
border-top-width:10px;   /* 设置顶部边框粗细为10px */   
border-top-style:solid;  /* 设置顶部边框的线性为实线，常用的有：solid(实线)  
  dashed(虚线)  dotted(点线); */

上面三句可以简写成一句：

border-top:10px solid red;
设置其它三个边的方法和上面一样，把上面的'top'换成'left'就是设置左边，换成'right'就是设置右边，换成'bottom'就是设置底边。

四个边如果设置一样，可以将四个边的设置合并成一句：

border:10px solid red;
```
- 设置间距 padding
```html
设置盒子四边的内间距，可设置如下：

padding-top：20px;     /* 设置顶部内间距20px */ 
padding-left:30px;     /* 设置左边内间距30px */ 
padding-right:40px;    /* 设置右边内间距40px */ 
padding-bottom:50px;   /* 设置底部内间距50px */
上面的设置可以简写如下：

padding：20px 40px 50px 30px; /* 四个值按照顺时针方向，分别设置的是 上 右 下 左  
四个方向的内边距值。 */
padding后面还可以跟3个值，2个值和1个值，它们分别设置的项目如下：

padding：20px 40px 50px; /* 设置顶部内边距为20px，左右内边距为40px，底部内边距为50px */ 
padding：20px 40px; /* 设置上下内边距为20px，左右内边距为40px*/ 
padding：20px; /* 设置四边内边距为20px */
```
- 设置外间距 margin 使用方式和padding相同
  - auto 自动居中

  - margin-top 中的塌陷问题，解决方式
    - 1 .border: 1px solid black;
    - 2 .overflow: hidden
    - 3 .
      ```html
      .clearfix:before{
                content: '';
                display:table;
            }
      ```
  
### 1.4 元素溢出
- 当子元素大小大于父元素就会溢出，此时可以使用overflow来处理
- overflow 
  - visible 默认值，保持不变
  - hidden 内容直接剪掉，一般用来解决margin-top塌陷和浮动问题
  - scroll 内容被修剪，不过浏览器会显示滚动条
  - auto 自动处理


### 1.5 display属性
- 块元素 【行元素】
  - div p ul li h1-h6 dl dt dd这些都是块元素
    - 支持全部样式
    - 若是不设置宽度，默认是父级的宽度
    - 单独占据一
- 内联元素 
  - a span em b strong i
    - 支持部分样式 （不支持宽高、margin上下、padding上下）
    - 宽高由内容决定
    - 盒子是并行在一行的，代码换行，盒子之间就会产生间距
      - 写成一行
      - 将父级的font-size设置为0，然后设置自己的font-size设置的大一点
    - 子元素是内联元素，父元素可以使用text_align设置水平对其方式
  
- 内联块元素
  - 例如： image input 这类归类于内联元素，可以使用display将`块元素`或者`内联元素`转化为内联块元素
  - 在布局中表现的行为  
    - 支持全部样式
    - 若是没有设置宽高，宽高由内容决定
    - 盒子并在一行
    - 代码换行 盒子会产生间隙
    - 子元素是内联块元素 父级可以使用text-align设置对平方式
  
- display
  - none 元素隐藏且不占位置
  - block 元素以块元素显示
  - inline 元素以内联元素显示
  - inline-block 元素以内联块元素显示
  
- 注意：
  - 在实际开发中，一般将内联元素转换为块元素，少量转换内联块，使用内联元素时，不用块元素转换
  
### 1.6 浮动布局
- 浮动特性

  - 1、浮动元素有左浮动(float:left)和右浮动(float:right)两种
  
  - 2、浮动的元素会向左或向右浮动，碰到父元素边界、其他元素才停下来
  
  - 3、相邻浮动的块元素可以并在一行，超出父级宽度就换行
  
  - 4、浮动让行内元素或块元素自动转化为行内块元素(此时不会有行内块元素间隙问题)
  
  - 5、浮动元素后面没有浮动的元素会占据浮动元素的位置，没有浮动的元素内的文字会避开浮动的元素，形成文字饶图的效果
  
  - 6、父元素如果没有设置尺寸(一般是高度不设置)，父元素内整体浮动的元素无法撑开父元素，父元素需要清除浮动
  
  - 7、浮动元素之间没有垂直margin的合并
   
- list-style:去掉ul的小圆点

### 1.7 定位
- 文档流【所以引出定位】
  - 受排版限制，先写先排，格式从上往下排，无法修改
  
- 使用定位突破限制
  - 使用css的position属性来设置元素的定位类型，position的属性如下：
    - relative 生成相对定位的元素，元素所占的文档流位置保留，元素本身相对于本身原位置进行偏移
    - absolute 生产绝对定位元素，元素脱离文档流，不占用文档流的位置，可以认为是悬浮在文档上方，
      相对于上一个设置了定位的父级元素来进行定位，若是找不到以body来定位
      
    - fixed 生产固定定位的元素，元素脱离文档流，相对于浏览器窗口进行定位
    - static 默认值  没有定位 元素出现在正常的文档流中，相当于取消了定位属性或者不设置定位属性
    - inherit 从父级继承position属性的值
  - 偏移
    - 定位的元素需要使用left right top bottom开始偏移
  - 定位层级
    - 可以使用z-index属性来设置元素的层级
      -  z-index中的数字设置的越大，越在最上面
  - 定位元素特性
     - 绝对定位和固定定位的块元素和行内元素会自动转换为行内块元素
  
### 1.8 background属性
- background-color 设置背景颜色
- background-image 设置背景图片地址
- background-repeat 设置背景图片如何重复平铺
  - repeat-x 平铺x轴方向
  - repeat-y 平铺y轴方向
  - no-repeat 平铺一次
- background-position 设置背景图的位置
  - 可以使用方位值
  - 也可以使用数值
- background-attachment 设置背景图时固定还是随着页面滚动条滚动

### 1.9 CSS3圆角
- 设置某一个角的圆角，比如设置左上角的圆角：border-top-left-radius:30px 60px;

- 同时分别设置四个角： border-radius:30px 60px 120px 150px;

- 设置四个圆角相同：border-radius:50%
### 1.10 rgba 颜色表示法
- 设置盒子的透明度
    - 直接在rgba中设置
    - 使用opacity加上对应的内容即可
        - 针对IE还需要加上
            - filter:alpha(opacity=30)
    
### 1.11 transition动画
- 一般用于部分网站，主页一般不要使用
- 设置在原始盒子上，对于跳变的不要使用
- transition-property 设置过度属性，比如width
- transition-duration 设置过度时间
- transition-timing-function 设置过渡运行方式
    - liner 匀速
    - ease 缓冲运动
- transition-delay 设置动画延迟
- transition: 同时设置上面四个属性 
    - transition: all;表示将多个属性同时做动画
        
### 1.12 transform变换【变形】
- translate(x,y) 设置盒子的位移 【比定位性能高】
- scale(x,y) 设置盒子缩放
- rotate(deg) 设置盒子旋转
- skew(x-angle,y-angle) 设置盒子斜切
- transform-origin 设置盒子的旋转中心
- translateX、translateY、translateZ 设置三维移动
- rotateX、rotateY、rotateZ 设置三维旋转
- scaleX、scaleY、scaleZ 设置三维缩放
- perspective 设置透视距离 结合三维旋转使用

- transform-style flat | preserve-3d 设置盒子是否按3d空间显示
- backface-visibility 设置盒子背面是否可见

### 1.13 animation动画
- @keyframes 定义关键帧动画
- animation-name 动画名称
- animation-duration 动画时间
- animation-timing-function 动画曲线 linear(匀速)|ease(缓冲)|steps(步数)【相当于跳变】
- animation-delay 动画延迟
- animation-iteration-count 动画播放次数 n|infinite
- animation-direction 动画结束后是否反向还原 normal|alternate
- animation-play-state 动画状态 paused(停止)|running(运动)
- animation-fill-mode 动画前后的状态 none(缺省)|forwards(结束时停留在最后一帧)|backwards(开始时停留在定义的开始帧)|both(前后都应用)
- animation:name duration timing-function delay iteration-count direction;同时设置多个属性

### 1.14 选择器
- E:nth-child(n)：匹配元素类型为E且是父元素的第n个子元素
- E:first-child：匹配元素类型为E且是父元素的第一个子元素
- E:last-child：匹配元素类型为E且是父元素的最后一个子元素
- E > F E元素下面第一层子集
- E ~ F E元素后面的兄弟元素
- E + F 紧挨着的后面的兄弟元素

- 属性选择器：
    - E[attr] 含有attr属性的元素
    - E[attr='ok'] 含有attr属性的元素且它的值为“ok”
    - E[attr^='ok'] 含有attr属性的元素且它的值的开头含有“ok”
    - E[attr$='ok'] 含有attr属性的元素且它的值的结尾含有“ok”
    - E[attr*='ok'] 含有attr属性的元素且它的值中含有“ok”
    
### 1.15 权重的等级
可以把样式的应用方式分为几个等级，按照等级来计算权重

- !important，加在样式属性值后，权重值为 10000
- 内联样式，如：style=””，权重值为1000
- ID选择器，如：#content，权重值为100
- 类，伪类和属性选择器，如： content、:hover 权重值为10
- 标签选择器和伪元素选择器，如：div、p、:before 权重值为1
- 通用选择器（*）、子选择器（>）、相邻选择器（+）、同胞选择器（~）、权重值为0

### 1.16 css3样式前缀
- -ms 兼容IE
- -moz 兼容Firefox
- -o 兼容oprea
- -webkit 兼容chrome和safari
```html
<!--比如-->
div
{    
    -ms-transform: rotate(30deg);        
    -webkit-transform: rotate(30deg);    
    -o-transform: rotate(30deg);        
    -moz-transform: rotate(30deg);    
    transform: rotate(30deg);
}
```
```html
自动添加浏览器前缀
目前的状况是，有些CSS3属性需要加前缀，有些不需要加，有些只需要加一部分，这些加前缀的工作可以交给插件来完成，比如安装： autoprefixer

可以在Sublime text中通过package control 安装 autoprefixer

Autoprefixer在Sublime text中的设置：
1、preferences/key Bindings-User

{ "keys": ["ctrl+alt+x"], "command": "autoprefixer" }
2、Preferences>package setting>AutoPrefixer>Setting-User

{
    "browsers": ["last 7 versions"],
    "cascade": true,
    "remove": true
}
last 7 versions：最新的浏览器的7个版本
cascade：缩进美化属性值
remove：是否去掉不必要的前缀
```


### 1.17 视口
视口是移动设备上用来显示网页的区域，一般会比移动设备可视区域大，宽度可能是980px或者1024px，目的是为了显示下整个为PC端设计的网页，这样带来的后果是移动端会出现横向滚动条，为了避免这种情况，移动端会将视口缩放到移动端窗口的大小
- 解决方案
```html
<!--设置方法如下( 快捷方式：meta:vp + tab )：-->
<head>
......
<meta name="viewport" content="width=device-width, user-scalable=no,
 initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
......
</head>
```