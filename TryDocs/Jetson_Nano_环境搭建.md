# jetson nano 舒适折腾指南

### 1. 更新镜像源

```shell
# See http://help.ubuntu.com/community/UpgradeNotes for how to upgrade to
# newer versions of the distribution.
deb http://ports.ubuntu.com/ubuntu-ports/ bionic main restricted
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic main restricted

## Major bug fix updates produced after the final release of the
## distribution.
deb http://ports.ubuntu.com/ubuntu-ports/ bionic-updates main restricted
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic-updates main restricted

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu
## team. Also, please note that software in universe WILL NOT receive any
## review or updates from the Ubuntu security team.
deb http://ports.ubuntu.com/ubuntu-ports/ bionic universe
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic universe
deb http://ports.ubuntu.com/ubuntu-ports/ bionic-updates universe
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic-updates universe

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu
## team, and may not be under a free licence. Please satisfy yourself as to
## your rights to use the software. Also, please note that software in
## multiverse WILL NOT receive any review or updates from the Ubuntu
## security team.
deb http://ports.ubuntu.com/ubuntu-ports/ bionic multiverse
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic multiverse
deb http://ports.ubuntu.com/ubuntu-ports/ bionic-updates multiverse
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic-updates multiverse

## N.B. software from this repository may not have been tested as
## extensively as that contained in the main release, although it includes
## newer versions of some applications which may provide useful features.
## Also, please note that software in backports WILL NOT receive any review
## or updates from the Ubuntu security team.
deb http://ports.ubuntu.com/ubuntu-ports/ bionic-backports main restricted universe multiverse
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic-backports main restricted universe multiverse

## Uncomment the following two lines to add software from Canonical's
## 'partner' repository.
## This software is not part of Ubuntu, but is offered by Canonical and the
## respective vendors as a service to Ubuntu users.
# deb http://archive.canonical.com/ubuntu bionic partner
# deb-src http://archive.canonical.com/ubuntu bionic partner

deb http://ports.ubuntu.com/ubuntu-ports/ bionic-security main restricted
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic-security main restricted
deb http://ports.ubuntu.com/ubuntu-ports/ bionic-security universe
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic-security universe
deb http://ports.ubuntu.com/ubuntu-ports/ bionic-security multiverse
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic-security multiverse
```

### 2. 安装输入法[谷歌输入法]

```shell
# settings -> language support 将 keyboard input method system 设置为fcitx
sudo apt-get install fcitx-googlepinyin
# 重启
sudo reboot
# 可能出现的问题
```

```shell
# 中文候选词无法出现，操作方案 不使用 fcitx-qimpanel  这个有毒
killall fcitx-qimpanel
sudo apt-get remove fcitx-ui-qimpanel 
```

### 3. 安装娱乐环境[让你的nano可以使用蓝牙音箱]

```shell
# 打开配置文件
sudo vim /lib/systemd/system/bluetooth.service.d/nv-bluetooth-service.conf
# 修改配置文件
ExecStart=/usr/lib/bluetooth/bluetoothd -d --noplugin=audio,a2dp,avrcp
# 修改为
ExecStart=/usr/lib/bluetooth/bluetoothd -d
# 执行命令
sudo apt-get update
sudo apt-get install pulseaudio-module-bluetooth
sudo reboot
# 连接蓝牙音箱试试
```


### 4. 安装vscode

    直接上清华源下载VS codium安装即可


### 5. 安装开发环境[记住一点  无脑选择arm64就行]

    5.1 安装golang环境

    5.2 安装java环境

```bash
# bashrc 中添加如下配置
export PATH=/usr/local/node/bin:$PATH
export PATH=/usr/local/go/bin:$PATH
export JAVA_HOME=/usr/local/jdk17
export PATH=$JAVA_HOME/bin:$PATH
```

### 6. 更新git

```shell
sudo add-apt-repository ppa:git-core/ppa
sudo apt update
sudo apt install git
```