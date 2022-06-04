# crontab

提交和管理用户的需要周期性执行的任务

##  补充说明

crontab 命令 被用来提交和管理用户的需要周期性执行的任务，与
windows
下的计划任务类似，当安装完成操作系统后，默认会安装此服务工具，并且会自动启动
crond 进程，crond
进程每分钟会定期检查是否有要执行的任务，如果有要执行的任务，则自动执行该任务。

###  语法

crontab(选项)(参数)

###  选项

```shell
-e：编辑该用户的计时器设置；
-l：列出该用户的计时器设置；
-r：删除该用户的计时器设置；
-u<用户名称>：指定要设定计时器的用户名称。
```

###  参数

crontab 文件：指定包含待执行任务的 crontab 文件。

###  知识扩展

Linux 下的任务调度分为两类： 系统任务调度 和 用户任务调度 。

系统任务调度：
系统周期性所要执行的工作，比如写缓存数据到硬盘、日志清理等。在/etc
目录下有一个 crontab 文件，这个就是系统任务调度的配置文件。

/etc/crontab 文件包括下面几行：

SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=""HOME=/

# run-parts

```shell
51 * * * * root run-parts
/etc/cron.hourly
24 7 * * * root run-parts
/etc/cron.daily
22 4 * * 0 root run-parts
/etc/cron.weekly
42 4 1 * * root run-parts
/etc/cron.monthly

# 前四行是用来配置 crond 任务运行的环境变量，第一行 SHELL
# 变量指定了系统要使用哪个 shell，这里是 bash，第二行 PATH
# 变量指定了系统执行命令的路径，第三行 MAILTO 变量指定了 crond
# 的任务执行信息将通过电子邮件发送给 root 用户，如果 MAILTO
# 变量的值为空，则表示不发送任务执行信息给用户，第四行的 HOME
# 变量指定了在执行命令或者脚本时使用的主目录。

# 用户任务调度： 用户定期要执行的工作，比如用户数据备份、定时邮件提醒等。用户可以
# 使用 crontab 工具来定制自己的计划任务。所有用户定义的 crontab
# 文件都被保存在/var/spool/cron
# 目录中。其文件名与用户名一致，使用者权限文件如下：

/etc/cron.deny     该文件中所列用户不允许使用 crontab
命令
/etc/cron.allow    该文件中所列用户允许使用 crontab
命令
/var/spool/cron/   所有用户 crontab
文件存放的目录,以用户名命名

crontab 文件的含义：用户所建立的 crontab 文件中，每一行都代表一
项任务，每行的每个字段代表一项设置，它的格式共分为六个字段，前五段是时间设定段，
第六段是要执行的命令段，格式如下：

minute   hour   day   month   week
command     顺序：分 时 日 月 周

# 其中：

# - minute： 表示分钟，可以是从 0 到 59 之间的任何整数。
# - hour：表示小时，可以是从 0 到 23 之间的任何整数。
# - day：表示日期，可以是从 1 到 31 之间的任何整数。
# - month：表示月份，可以是从 1 到 12 之间的任何整数。
# - week：表示星期几，可以是从 0 到 7 之间的任何整数，这里的 0 或
# 7 代表星期日。
# - command：要执行的命令，可以是系统命令，也可以是自己编写的脚本文件。

# 在以上各个字段中，还可以使用以下特殊字符：

# - 星号（*）：代表所有可能的值，例如 month
# 字段如果是星号，则表示在满足其它字段的制约条件后每月都执行该命令操作。
# -
# 逗号（,）：可以用逗号隔开的值指定一个列表范围，例如，“1,2,5,7,8,9”
# - 中杠（-）：可以用整数之间的中杠表示一个整数范围，例如“2-
# 6”表示“2,3,4,5,6”
# - 正斜线（/）：可以用正斜线指定时间的间隔频率，例如“0-
# 23/2”表示每两小时执行一次。同时正斜线可以和星号一起使用，例如*/10，如果
# 用在 minute 字段，表示每十分钟执行一次。
```

crond 服务

```shell
/sbin/service crond start    # 启动服务
/sbin/service crond stop     # 关闭服务
/sbin/service crond restart  # 重启服务
/sbin/service crond reload   # 重新载入配置
```

查看 crontab 服务状态：

```shell
service crond status
```

手动启动 crontab 服务：

```shell
service crond start
```

查看 crontab 服务是否已设置为开机启动，执行命令：

```shell
ntsysv
```

加入开机自动启动：

```shell
chkconfig –level 35 crond on
```

###  实例

每 1 分钟执行一次 command

```shell
* * * * * command
```

每小时的第 3 和第 15 分钟执行

```shell
3,15 * * * * command
```

在上午 8 点到 11 点的第 3 和第 15 分钟执行

```shell
3,15 8-11 * * * command
```

每隔两天的上午 8 点到 11 点的第 3 和第 15 分钟执行

```shell
3,15 8-11 */2 * * command
```

每个星期一的上午 8 点到 11 点的第 3 和第 15 分钟执行

```shell
3,15 8-11 * * 1 command
```

每晚的 21:30 重启 smb

```shell
30 21 * * * /etc/init.d/smb restart
```

每月 1、10、22 日的 4 : 45 重启 smb

```shell
45 4 1,10,22 * * /etc/init.d/smb restart
```

每周六、周日的 1:10 重启 smb

```shell
10 1 * * 6,0 /etc/init.d/smb restart
```

每天 18 : 00 至 23 : 00 之间每隔 30 分钟重启 smb

```shell
0,30 18-23 * * * /etc/init.d/smb restart
```

每星期六的晚上 11:00 pm 重启 smb

```shell
0 23 * * 6 /etc/init.d/smb restart
```

每一小时重启 smb

```shell
* */1 * * * /etc/init.d/smb restart
```

晚上 11 点到早上 7 点之间，每隔一小时重启 smb

```shell
* 23-7/1 * * * /etc/init.d/smb restart
```

每月的 4 号与每周一到周三的 11 点重启 smb

```shell
0 11 4 * mon-wed /etc/init.d/smb restart
```

一月一号的 4 点重启 smb

```shell
0 4 1 jan * /etc/init.d/smb restart
```

每小时执行/etc/cron.hourly 目录内的脚本

```shell
01 * * * * root run-parts
/etc/cron.hourly
```