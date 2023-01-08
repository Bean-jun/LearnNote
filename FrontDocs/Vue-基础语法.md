# 一、 配置环境

1. 安装nodejs
2. 安装vue  `npm install vue@next`
3. 安装命令行工具
    ```shell
    npm install -g @vue/cli
    npm i -g @vue/cli-init
    ```
4. 创建项目 
    ```shell
    # npm 7+，需要加上额外的双短横线
    $ npm init vite@latest <project-name> -- --template vue

    # 或者
    $ vue init webpack <project-name>

    $ cd <project-name>
    $ npm install
    $ npm run dev
    ```

5. 打包项目     `npm run build`

# 二、 vue2基础语法

## 1. 数据绑定

### 1.1 v-bind 单向绑定（数据仅仅只能从data流向页面）
### 1.2 v-model 双向绑定(数据可以在页面和data之间流通，当前操作仅仅用于表单) 
```html
<div id="app">
    <input type="text" name="xxx" v-bind:value="value" />
    <!-- 简写 -->
    <input type="text" name="xxx" :value="value" />

    <input type="text" name="xxx" v-model:value="value" />
    <!-- 简写 -->
    <input type="text" name="xxx" v-model="value" />

</div>

<script>
    new Vue({
        el: "#app",
        data: {
            value: "请输入"
        }
    })
</script>
```

### 1.3 v-if
### 1.4 v-else
```html
<h1 v-if="status===true">确实如此</h1>
<h1 v-else>确实不如此</h1>

<script>
    const vm = new Vue({
        el: "#app",
        data: {
            message: "hello vue",
            status: false,
            type: "A",
            datas: [
                {key: "0"},
                {key: "1"},
                {key: "2"},
                {key: "3"},
                {key: "4"},
            ]
        }
    });
</script>
```

### 1.5 v-else-if
```html
<h1 v-if="type==='A'">A</h1>
<h1 v-else-if="type==='B'">B</h1>
<h1 v-else>C</h1>

<script>
    const vm = new Vue({
        el: "#app",
        data: {
            message: "hello vue",
            status: false,
            type: "A",
            datas: [
                {key: "0"},
                {key: "1"},
                {key: "2"},
                {key: "3"},
                {key: "4"},
            ]
        }
    });
</script>
```

### 1.6 v-for
```html
<h3 v-for="v in datas">
    {{v.key}}
</h3>

<script>
    const vm = new Vue({
        el: "#app",
        data: {
            message: "hello vue",
            status: false,
            type: "A",
            datas: [
                {key: "0"},
                {key: "1"},
                {key: "2"},
                {key: "3"},
                {key: "4"},
            ]
        }
    });
</script>
```

### 1.7 v-on:
```html
<button v-on:click="sayHai">click</button>
<!-- 简写 -->
<button @click="sayHai">click2</button>

<script>
    const vm = new Vue({
        el: "#app",
        data: {
            message: "hello vue",
            status: false,
            type: "A",
        },
        methods: {
            sayHai: function() {
                alert("别点我");
                console.log(event)
            }
        },
    });
</script>
```

## 2. 组件使用

### 2.1 注册组件

使用时`compontent`中第一个表示组件名称，在日常使用功能组件时 它们与 new Vue 接收相同的选项，例如 data、computed、watch、methods 以及生命周期钩子等。仅有的例外是像 el 这样根实例特有的选项。

#### 2.1.1 全局注册组件
```html
<div id="components-demo">
    <button-counter></button-counter><br />
    <button-counter></button-counter><br />
</div>
<script>
    Vue.component('button-counter', {
        data: function () {
            return {
                count: 0
            }
        },
        template: '<button @click="count++"><button @click="Say">666</button>You clicked me {{ count }} times.</button>',
        methods: {
            Say: function() {
                alert("????????")
            }
        },
    })
    const vm = new Vue({
        el: "#components-demo",
    });
</script>
```

#### 2.1.2 局部注册组件
全局注册往往是不够理想的。比如，如果你使用一个像 webpack 这样的构建系统，全局注册所有的组件意味着即便你已经不再使用一个组件了，它仍然会被包含在你最终的构建结果中。这造成了用户下载的 JavaScript 的无谓的增加。
```html
<div id="components-demo">
    <button-counter></button-counter><br />
    <button-counter></button-counter><br />
</div>
<script>
    
    const vm = new Vue({
        el: "#components-demo",
        components: {
            "ButtonCounter": Vue.component('ButtonCounter', {
                    data: function () {
                        return {
                            count: 0
                        }
                    },
                template: '<button @click="count++"><button @click="Say">666</button>You clicked me {{ count }} times.</button>',
                methods: {
                    Say: function() {
                        alert("????????")
                    }
                },
    })
        }
    });
</script>
```

### 2.2 向子组件中传值 `Props`

```html
<div id="components-demo">
    <button-counter title="第一个"></button-counter><br />
    <button-counter title="第二个"></button-counter><br />
</div>
<script>
Vue.component('button-counter', {
    data: function () {
        return {
            count: 0
        }
    },
    props: ["title"],

    // 使用如下方式进行传值类型约束
    // props: {
    //         title: String,
    //     },
    template: '<button @click="count++"><button @click="Say">666</button>You {{ title || 100 }} clicked me {{ count }} times.</button>',
    methods: {
        Say: function() {
            alert("????????")
        }
    },
})
const vm = new Vue({
    el: "#components-demo",
});
</script>
```

### 2.3 向父组件传递事件、值 `$emit`

```html
<ul>
    <div v-bind:style="{fontSize: chapterFontSize + 'em'}">
        <blog v-for="c in chapter" v-bind:id="c.id" v-bind:title="c.title" @elnlarge="chapterFontSize += $event"></blog>
    </div>
</ul>
<scritp>
Vue.component("blog",{
        props: ["id", "title"],
        // 当button被点击时，elnlarge事件将被向上传递, 其值1也将被传递，获取方式可以使用$event获取
        template: `<li>???? {{id}}-{{title}}  <button @click="$emit('elnlarge', 1)">点击放大</button>  ?????</li>`,
    });
</scritp>
```

### 2.4 插槽 `<slot></slot>`

```html
<ul>
    <blog>插槽内容</blog>
</ul>
<scritp>
Vue.component("blog",{
        template: `<li><slot></slot></li>`,
    });
</scritp>
```


# 三、常见使用

1. npm换源

```shell
由于npm下载源在国外，严重影响速度。因此，乐于分享的淘宝团队，将npm下载源部署到了国内。

来自官网：“这是一个完整 npmjs.org 镜像，你可以用此代替官方版本(只读)，同步频率目前为 10分钟 一次以保证尽量与官方服务同步。”

换源方法：

1.使用阿里定制的 cnpm 命令行工具代替默认的 npm，输入下面代码进行安装：

$ npm install -g cnpm --registry=https://registry.npm.taobao.org

以后安装插件只需要使用cnpm intall即可。

2.如果习惯了npm，又不想使用cnpm怎么办呢？也不是没有办法。

输入以下命令：

npm config set registry https://registry.npm.taobao.org

再输入：

npm config list

可以看到，已经换源了：

$ npm config list
; cli configs
metrics-registry = "https://registry.npm.taobao.org/"
scope = ""
user-agent = "npm/6.4.1 node/v10.15.1 linux x64"

; userconfig /home/dounine/.npmrc
registry = "https://registry.npm.taobao.org/"

; node bin location = /usr/app/node-v10.15.1/bin/node
; cwd = /usr/app/node-v10.15.1/lib/node_modules
; HOME = /home/dounine
; "npm config ls -l" to show all defaults.
npm最常用的便是安装各种包。其中，分为 全局安装 和 本地安装：

npm install <package>      # 本地安装
npm install <package> -g   # 全局安装
将安装包放在 ./node_modules 下（运行 npm 命令时所在的目录，项目根目录），如果没有 node_modules 目录，会在当前执行 npm 命令的目录下生成 node_modules 目录。

可以通过 require() 来引入本地安装的包。

所以，我们第一次运行项目需要npm install的原因就是：下载所有项目依赖包。

注意：若在项目过程中需要引入外包，npm install <package> 不会将包录入package.json中。而，npm install <package> --save才会。package.json即每次npm install安装项目依赖包的参照文件。

将安装包放在 $NODE_HOME/lib/node_modules，可以直接在命令行里使用。如：安装vue-cli：npm install vue-cli -g，安装完便可直接使用 vue 命令。

注意：进行全局安装时，若不是root用户则可能出现以下问题：

npm WARN checkPermissions Missing write access to /usr/app/node-v10.15.1/lib/node_modules

/usr/app/node-v10.15.1是我地node安装目录，但对该目录修改需要root权限。

因此，全局安装命令应改为：sudo npm install vue-cli -g

在项目根目录下 npm run dev

在项目根目录下 npm build

生成 dist/ 目录，是项目编译后的静态文件

```