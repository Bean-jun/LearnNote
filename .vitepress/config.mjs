import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base: "/LearnNote/",
  title: "LearnGuide",
  description: "A LearnGuide Site",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      {
        text: '编程那些事',
        items: [
          {
            text: "Python从入门到入土",
            link: 'PythonDocs/index'
          },
          {
            text: 'Golang从入门到入土',
            link: 'GolangDocs/index'
          },
          {
            text: 'Java从入门到入土',
            link: 'JavaDocs/index'
          },
          {
            text: '前端那些事',
            link: 'FrontDocs/index'
          },
        ]
      },
      // {
      //   text: '数据结构与算法',
      //   items: [
      //     { text: 'Item A', link: '/item-1' },
      //     { text: 'Item B', link: '/item-2' },
      //     { text: 'Item C', link: '/item-3' }
      //   ]
      // },
      {
        text: '设计模式',
        items: [
          { text: '面向对象设计原则', link: 'DesignDocs/设计模式.md#零面向对象设计原则' },
          { text: '创建型模式', link: 'DesignDocs/设计模式.md#一创建型模式-介绍对象创建' },
          { text: '结构型模式', link: 'DesignDocs/设计模式.md#二结构型模式-介绍不同对象之间的关系' },
          { text: '行为型模式', link: 'DesignDocs/设计模式.md#三行为型模式-介绍对象之间通信的关系' },
        ]
      },
      {
        text: '网络编程',
        items: [
          {
            text: 'UDP协议&&TCP协议',
            items: [
              { text: '基于Socket的UDP协议实现', link: 'NetworkDocs/基于Socket的UDP协议实现' },
              { text: '基于Socket的TCP协议实现', link: 'NetworkDocs/基于Socket的TCP协议实现' },
              { text: '基于Socket的简单封装对TCP粘包问题的小试牛刀', link: 'NetworkDocs/基于Socket的简单封装对TCP粘包问题的小试牛刀' },
              { text: '基于Socket的简易聊天室', link: 'NetworkDocs/基于Socket的简易聊天室-Python版本' },
            ]
          },
          {
            text: 'HTTP协议',
            items: [
              { text: '基于Socket的HTTP协议实现', link: 'NetworkDocs/基于Socket的HTTP协议实现' },
            ]
          },
          {
            text: 'WebSocket协议',
            items: [
              { text: '基于Socket的WebSocket协议实现', link: 'NetworkDocs/基于Socket的WebSocket协议实现' },
              { text: '结合SocketServer库的WebSocket协议实现', link: 'NetworkDocs/结合SocketServer库的WebSocket协议实现' },
              { text: 'websockets', link: 'https://websockets.readthedocs.io' },
              { text: 'Channels', link: 'https://channels.readthedocs.io' },
            ]
          },
        ]
      },
      {
        text: '数据库',
        items: [
          {
            text: 'MySQL',
            items: [
              { text: '入门使用', link: 'DatabaseDocs/MySQL-入门' },
              { text: '主从配置', link: 'DatabaseDocs/MySQL-主从配置' },
              { text: 'MySQL基础篇', link: 'DatabaseDocs/MySQL基础篇' },
              { text: 'MySQL架构篇', link: 'DatabaseDocs/MySQL架构篇' },
              { text: 'MySQL索引调优篇', link: 'DatabaseDocs/MySQL索引调优篇' },
              { text: 'MySQL事务篇', link: 'DatabaseDocs/MySQL事务篇' },
              { text: 'MySQL日志备份篇', link: 'DatabaseDocs/MySQL日志备份篇' },
            ]
          },
          {
            text: 'Redis',
            items: [
              { text: '入门使用', link: 'DatabaseDocs/Redis-入门' },
              { text: '事务', link: 'DatabaseDocs/Redis-事务' },
              { text: '持久化', link: 'DatabaseDocs/Redis-持久化' },
              { text: '复制&哨兵', link: 'DatabaseDocs/Redis-复制&哨兵' },
              { text: '缓存设计', link: 'DatabaseDocs/Redis-缓存设计' },
            ]
          },
          { text: 'MongoDB', link: '#' },
          {
            text: 'ORM工具【非数据库】',
            items: [
              { text: 'SQLAlchemy基本使用', link: 'OtherDocs/SQLAlchemy基本使用' },
              { text: 'peewee', link: 'http://docs.peewee-orm.com/en/latest/' },
              { text: 'GORM', link: 'https://gorm.io/zh_CN/docs/index.html' },
            ]
          },
        ]
      },
      {
        text: 'Web框架',
        items: [
          {
            text: 'Django',
            items: [
              { text: 'Django入门使用（修复中）', link: 'WebFrameDocs/Django-入门' },
              { text: 'DRF入门使用', link: 'WebFrameDocs/DRF-入门' },
              { text: '基于django实现的PersonBlog', link: 'https://github.com/Bean-jun/PersonBlogSystem.git' },
              { text: '基于django实现的AuthSystem', link: 'https://github.com/Bean-jun/AuthSystem.git' },
            ]
          },
          {
            text: 'Flask',
            items: [
              { text: '入门使用', link: 'WebFrameDocs/Flask-入门' },
              { text: 'flask-信号的使用', link: 'WebFrameDocs/Flask-信号的使用' },
              { text: 'flask源码分析第一弹', link: 'WebFrameDocs/Flask-源码分析' },
              { text: 'flask源码分析第二弹', link: 'WebFrameDocs/Flask-源码分析2' },
              { text: '基于flask实现的api-demo', link: 'https://github.com/Bean-jun/PersonBlogSystemFlask.git' },
            ]
          },
          {
            text: 'Fastapi',
            items: [
              { text: '基于fastAPI实现的文件对象存储', link: 'https://github.com/Bean-jun/fileStorage' },
            ]
          },
          {
            text: 'Tornado',
            items: [
              { text: '一个基于rbac模型的crud架子', link: 'https://github.com/Bean-jun/tornado_demo.git' },
            ]
          },
          { text: 'Aiohttp', link: 'https://docs.aiohttp.org/en/stable/' },
          { text: 'Gin', link: 'https://gin-gonic.com/zh-cn/' },
        ]
      },
      {
        text: '常用工具',
        items: [
          {
            text: 'nginx',
            items: [
              { text: 'nginx中的一些基本概念', link: 'OtherDocs/nginx' },
              { text: 'ubuntu下nginx简易安装', link: 'OtherDocs/nginx安装-Ubuntu' },
              { text: 'nginx+uwsgi项目部署', link: 'DeployDocs/nginx_uwsgi部署' },
              { text: 'OpenResty', link: 'OtherDocs/OpenResty' },
            ]
          },
          { text: 'docker', link: 'OtherDocs/docker' },
          { text: 'crontab', link: 'OtherDocs/crontab' },
          { text: 'celery', link: 'OtherDocs/celery使用' },
          { text: 'siege', link: 'https://www.joedog.org/siege-home' },
          { text: 'uwsgi', link: 'https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/index.html' },
          { text: 'frp', link: 'https://gofrp.org/' },
          { text: 'nacos', link: 'https://nacos.io/' },
        ]
      },
      {
        text: '开发知识',
        items: [
          { text: 'cookies、session、token', link: 'DevelopDocs/cookie_session_token介绍' },
          { text: 'OAuth2、SSO', link: 'DevelopDocs/oauth2_sso介绍' },
          { text: 'LVS', link: 'DevelopDocs/LVS介绍' }
        ]
      },
      {
        text: '遇见的BUG',
        items: [
          { text: 'cookie离谱的生效范围', link: 'BugDocs/cookie离谱的生效范围' },
          { text: 'go加密库执行慢的bug', link: 'BugDocs/go加密库执行慢的bug' },
          { text: '解决文件名冲突的工具函数竟是slow的元凶', link: 'BugDocs/解决文件名冲突的工具函数竟是slow的元凶' }
        ]
      },
      {
        text: '其他',
        items: [
          { text: '工具集合', link: 'ToolsDocs/工具集合' },
          { text: 'Jetson Nano环境搭建', link: 'TryDocs/Jetson_Nano_环境搭建' },
          { text: 'Pyinstaller工具小Tips', link: 'TryDocs/Pyinstaller工具小tips' },
          { text: 'Py快速将py脚本编译为pyd', link: 'TryDocs/Py快速将py脚本编译为pyd' },
          { text: 'Py脚本打包效率对比', link: 'TryDocs/Py脚本打包后执行效率对比' },
          { text: 'Lua基础', link: 'TryDocs/Lua基础' },
        ]
      },
    ],

    // sidebar: [
    //   {
    //     text: 'Examples',
    //     items: [
    //       { text: 'Markdown Examples', link: '/markdown-examples' },
    //       { text: 'Runtime API Examples', link: '/api-examples' },
    //     ]
    //   }
    // ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Bean-jun/LearnNote' }
    ],

    footer: {
      message: 'Released under the <a href="https://github.com/Bean-jun/LearnNote/blob/main/LICENSE">MIT License</a>.',
      copyright: 'Copyright © 2020-present <a href="https://github.com/Bean-jun">Bean-jun</a>'
    }
  }
})
