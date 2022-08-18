# 一、软件运行环境和简介

功能定制，商务合作，问题/交流群: [512897146](https://jq.qq.com/?_wv=1027&k=V2mVBvL3)

特别说明, 本作品 前端[FlawPlatformVue](https://github.com/S2eTo/FlawPlatformVue), 后端[FlawPlatformMatch](https://github.com/S2eTo/FlawPlatform)可开源使用，但必须免费提供使用。用于任何形式的商务/盈利活动，请提前联系交流群群主。

## 1.1 软件简介

程序基于 Docker ，使用 Python + Django 前后端分离开发的在线答题程序

# 二、安装说明

## 2.1 前端地址

项目为前后端分离项目，前端仓库：https://gitee.com/J0hNs0N/FlawPlatformVue

## 2.2 安装 Python 3

安装依赖环境

```sh
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
```

下载 python 3.7.1。若出现 command not found 的错误，通过命令 yum -y install wget 安装 wget 即可

```sh
wget https://www.python.org/ftp/python/3.7.1/Python-3.7.2.tgz
```

创建安装目录

```sh
mkdir -p /usr/local/python3
```

解压安装包

```sh
tar -zxvf Python-3.7.2.tgz
```

安装 gcc

```sh
yum install gcc -y
```

Python 3.7 版本之后需要多安装一个依赖环境

```sh
yum install libffi-devel -y
```

进入解压后的 Python 3 安装包目录

```sh
cd Python-3.7.1
```

生成编译脚本

```sh
./configure --prefix=/usr/local/python3
```

编译安装

```sh
make && make install
```

测试安装是否成功

```sh
/usr/local/python3/bin/python3
```

创建软连接

```sh
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
```

安装所需依赖

```sh
yum install python-devel -y
yum install zlib-devel -y
yum install libjpeg-turbo-devel -y
```

## 2.3 使用 SQLite3 数据库

程序默认使用 SQLite3 数据库，但需要升级，若不想使用 SQLite3 可以直接跳转到下一章 **3. 使用Mysql 数据库**

### 2.3.1 升级 SQLite3

获取安装包下载地址：https://www.sqlite.org/download.html

![image-20220329121505366](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329121505366.png)

下载 Sqlite 最新版安装包

```sh
wget https://www.sqlite.org/2022/sqlite-autoconf-3380200.tar.gz
```

解压安装包

```sh
tar zxvf sqlite-autoconf-3380200.tar.gz
```

进入解压后的安装包目录

```sh
cd sqlite-autoconf-3380200
```

生成编译脚本

```sh
./configure --prefix=/usr/local/sqlite3
```

编译安装

```sh
make && make install
```

检查安装是否成功

```sh
/usr/local/sqlite3/bin/sqlite3 --version
```

检查旧版本

```sh
/usr/bin/sqlite3 --version
```

将旧版本更换名字

```sh
mv /usr/bin/sqlite3  /usr/bin/sqlite3_old
```

设置新版本软连接

```sh
ln -s /usr/local/sqlite3/bin/sqlite3 /usr/bin/sqlite3
```

检查 *sqlite3* 版本

```sh
sqlite3 --version
```

编辑环境变量文件 `$HOME/.bash_profile` 添加下列变量

```
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/sqlite3/lib"
```

![image-20220330230801271](D:\广东省大学生计算机设计大赛\说明文档\FlawPlatform 漏洞靶场\image-20220330230801272.png)

重新加载环境变量

```
source $HOME/.bash_profile
```

检查版本

![image-20220329123359686](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329123359686.png)

### 2.3.2 迁移数据库

解压项目压缩文件后，cd 切换工作目录到项目文件夹中，与 `manage.py` 同级

![image-20220329154328034](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329154328034.png)

创建迁移记录

```sh
pyhton3 manage.py makemigrations
```

![image-20220329160345458](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329160345458.png)

迁移创建数据库

```sh
pyhton3 manage.py migrate
```

![image-20220329160403589](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329160403589.png)

## 2.4 使用 Mysql 数据库

### 2.4.1 安装 Mysql 数据库

centos 直接安装 mariadb 即可

```sh
yum -y install mariadb
```

### 2.4.2 修改程序配置文件

建议设置只在内网开放 3306 端口 通过 `bind-address` 设置（注意保存后重启服务）

```sh
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
# 2.Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
# 2.Settings user and group are ignored when systemd is used.
# 2.If you need to run mysqld under a different user or group,
# 2.customize your systemd unit file for mariadb according to the
# 2.instructions in http://fedoraproject.org/wiki/Systemd

# 2.设置绑定的 IP 地址为环回口地址 127.0.0.1
bind-address=127.0.0.1

[mysqld_safe]
log-error=/var/log/mariadb/mariadb.log
pid-file=/var/run/mariadb/mariadb.pid

#
# 2.include all files from the config directory
#
!includedir /etc/my.cnf.d
```

重启服务

```sh
systemctl restart mariadb
```

检查端口绑定情况

![image-20220329152729950](D:\广东省大学生计算机设计大赛\说明文档\FlawPlatform 漏洞靶场\image-20220329152729950-16488048778422.png)

### 2.4.3 设置 Mysql 密码

为了安全考虑，哪怕只开在回环口也需要设置登录密码。如果觉得不需要设置，可以跳过这一步

默认密码是空的，可以直接通过 `mysql -u root -p` 空密码登录即可

![image-20220329152835883](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329152835883.png)

这里通过直接更新数据表的方式修改密码

```mysql
UPDATE user SET Password = PASSWORD('密码') WHERE user = 'root';
```

刷新

```mysql
FLUSH PRIVILEGES;
```

### 2.4.4 创建数据库

为程序创建一个数据库，名字自定义。但后面配置 Django 时需要填对

```
flaw_platform
```

![image-20220329160204619](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329160204619.png)

### 2.4.5 配置编码

编辑 `/etc/my.conf` ，设置 编码。记得重启 mariadb 服务

```sh
[client]
# 2.设置编码
default-character-set=utf8

[mysql]
# 2.设置编码
default-character-set=utf8

[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
# 2.Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
# 2.Settings user and group are ignored when systemd is used.
# 2.If you need to run mysqld under a different user or group,
# 2.customize your systemd unit file for mariadb according to the
# 2.instructions in http://fedoraproject.org/wiki/Systemd

# 2.设置绑定地址
bind-address=127.0.0.1


# 2.设置编码
collation-server=utf8_unicode_ci
init-connect='SET NAMES utf8'
character-set-server=utf8


[mysqld_safe]
log-error=/var/log/mariadb/mariadb.log
pid-file=/var/run/mariadb/mariadb.pid

#
# 2.include all files from the config directory
#
!includedir /etc/my.cnf.d
```

### 2.4.6 配置 Django 使用 Mysql 数据库

解压项目压缩文件后，cd 切换工作目录到项目文件夹中，与 `manage.py` 同级

![image-20220329154324473](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329154324473.png)

安装 mysqlclient

```sh
pip3 install mysqlclient
```

出现报错以下两种方法解决

```
# 2.更新pip
pip3 install --upgrade pip

# 2.安装 mysql-devel
yum install mysql-devel
```

编辑 `common/settings.py` 文件

```sh
vim common/settings.py
```

进行如下修改, 注意保存

```sh
# 2.Database
# 2.https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 2.'ENGINE': 'django.db.backends.sqlite3',
        # 2.'NAME': BASE_DIR / 'db.sqlite3',

        'ENGINE': 'django.db.backends.mysql',   # 2.数据库引擎
        'NAME': '',                             # 2.数据库名，先前创建的
        'USER': 'root',                         # 2.用户名，可以自己创建用户
        'PASSWORD': 'xxxx',                     # 2.密码
        'HOST': '127.0.0.1',                    # 2.mysql服务所在的主机ip
        'PORT': '3306',                         # 2.mysql服务端口
    }
}
```

创建迁移记录

```sh
pyhton3 manage.py makemigrations
```

![image-20220329160345458](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329160345458.png)

迁移创建数据库

```sh
pyhton3 manage.py migrate
```

![image-20220329160403589](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329160403589.png)

## 2.5 配置 Docker

### 2.5.1 安装 docker

通过 yum 一键安装即可

```sh
yum -y install docker
```

### 2.5.2 配置 Remote API

编辑服务配置文件

```sh
vim /usr/lib/systemd/system/docker.service
```

再  ExecStart 值中添加多一行，**注: 这里最好不要暴露在公网上，因为这里的 Remote API 没有身份校验。任何人都可以通过这个 Remote API 操作你的 Docker，进行操作。**

```
-H tcp://127.0.0.1:2375 -H unix:///var/run/docker.sock
```

![image-20220329104619088](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329104619088.png)

重启 Docker 服务

```sh
systemctl daemon-reload
systemctl restart docker
```

检查端口是否开启，如果 `netstat command not found` 需要安装 *net-tools* : `yum -y install net-tools` 

```
netstat -ano | grep 2375
```

![image-20220329104535343](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329104535343.png)

### 2.5.3 配置 Django Docker Remote API 信息

cd 切换工作目录到项目文件夹中，与 `manage.py` 同级

![image-20220329154324473](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329154324473.png)

编辑 `common/settings.py` 文件

```sh
vim common/settings.py
```

进行如下修改, 注意保存

```python
DOCKER_API = {
    'URL': 'tcp://127.0.0.1:2375',
    
    # 2.外部映射地址, 只起到显示作用。同时是提供外部访问容器端口的地址
    'EXTERNAL_URL': '10.8.7.46',
    
    # 2.随机 Flag 设置的环境变量名称，建议默认
    'FLAG_ENVIRONMENT_NAME': 'RANDOM_FLAG',
    
    # 2.自动删除容器/靶机时间如: +1 为一小时后自动关闭
    'AUTO_REMOVE_CONTAINER': +1
}
```

## 2.7 配置邮件服务器

### 2.7.1 获取授权码

已 QQ 邮箱为例子，打开 QQ 邮箱 点击设置

![image-20220211005244106](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211005244106.png)

点击账户

![image-20220211005355961](D:\广东省大学生计算机设计大赛\说明文档\FlawPlatform 漏洞靶场\image-20220211005355962.png)

将服务全部开启

![image-20220211005429208](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211005429208.png)

点击生成授权码获取授权码

![image-20220211005502921](D:\广东省大学生计算机设计大赛\说明文档\FlawPlatform 漏洞靶场\image-20220211005502922.png)

### 2.7.2 配置文件

配置 `common/settings.py`

![image-20220329201355598](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329201355598.png)

## 2.8 部署后端

### 2.8.1 安装所需包

cd 切换工作目录到项目文件夹中，与 `manage.py` 同级

![image-20220329154324473](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329154324473.png)

使用 *pip* 安装 *requirements.txt* 

```
pip3 install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
```

### 2.8.2 启动服务

cd 切换工作目录到项目文件夹中，与 `manage.py` 同级

![image-20220329154324473](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329154324473.png)

启动服务

```sh
# 2.python3 manage.py runserver IP:PORT
python3 manage.py runserver 10.8.7.46:8000
```

![image-20220329161803886](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329161803886.png)

### 2.8.3 管理后台

通过 `createsuperuser` 创建超级管理员用户，我这里设置的用户为：`gdcp_flawplatform_admin`，密码：`gdcp123abc..`

```
python3 manage.py createsuperuser
```

![image-20220329162927817](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329162927817.png)

即可通过创建的用户民密码登录后台：`http://ip:port/admin/`

![image-20220329163126113](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329163126113.png)

## 2.9 部署前端

### 2.9.1 打包程序

打开项目文件 `src/common/http-service.js` 根据后端部署的地址和端口进行设置

![image-20220329161728154](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329161728154.png)

在项目目录文件夹下 使用 ` npm run build` 进行打包，注意与 `package.json` 同目录

![image-20220329162043944](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329162043944.png)

打包完成后回生成一个 dist 目录

![image-20220329162118374](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329162118374.png)

将生成的文件部署到 http 服务中即可

![image-20220329162140036](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329162140036.png)

### 2.9.2 安装 httpd 服务

这里使用 httpd 提供 http 服务，通过 yum 安装

```
yum -y install httpd
```

安装成功后，将打包的前端程序部署到 www 站点目录下

![image-20220329162431652](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329162431652.png)

这里最好重启一下服务

```
systemctl restart httpd
```

即可通过浏览器访问

![image-20220329162624624](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220329162624624.png)

# 三、使用说明

## 3.1 后台使用说明

进入子页面后，可通过 `breadcrumbs` 跳转至父级页面（这里只是演示）

![image-20220211222658291](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211222658291.png)

### 3.1.1 管理员操作

#### (1) 管理员登录

在浏览器访问 `http://127.0.0.1:8000/admin` 进入后台登录界面，输入用户名密码，点击登录进入后台。这里使用的是超级管理员账户，如果没有账户请回到本文 **2.2.5 创建管理员账户** 一章进行创建

![image-20220211023150087](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211023150087.png)

登录成功

![image-20220211023455408](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211023455408.png)

#### (2) 修改管理员密码

登录成功点击右上角 修改密码

![image-20220212000719787](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212000719787.png)

根据提示要求，输入旧密码、新密码、新密码确认后点击右下角修改我的密码即可

![image-20220212000750273](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212000750273.png)

### 3.1.2 题目管理

#### (1) 增加题目

点击题目可以进入题目列表

![image-20220211100325147](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211100325147.png)

点击右上角`增加 题目 +` 进入添加界面

![image-20220211100350494](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211100350494.png)

可选择题目环境：镜像环境或附件环境，默认为镜像环境。镜像环境模式下可选择 Flag 形式：环境变量随机 FLAG或文件内容随机FLAG，默认为环境变量随机 FLAG

![image-20220211100532192](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211100532192.png)

##### (1.1) 镜像环境 - 环境变量随机 FLAG

这里以**`j0hns0n/view_source:latest ID：81fb8003157e `**为例

![image-20220211101350810](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211101350810.png)

填写完成 镜像ID 后程序会自动调用 Docker API 获取镜像信息：镜像标签与开放端口信息

![image-20220211101603480](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211101603480.png)

填写完相应信息后点击保存即可添加成功

![image-20220211101735209](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211101735209.png)

添加成功后会在列表中展示（当题目超过十条时，会自动分页，每页十条）

![image-20220211101821976](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211101821976.png)

##### (1.2) 镜像环境 - 文件内容随机 FLAG

这里以 `j0hns0n/robots:latest ID: 31d68e72be64` 为例

![image-20220211101941172](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211101941172.png)

1、选择本地文件随机FLAG形式，2、填写文件路径（程序会自动随机成FLAG，写入到填写的文件路径中），填写文件内容模板 `{}` 为FLAG 存放的位置

![image-20220211102219888](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211102219888.png)

填写完成题目信息后点击保存即可

![image-20220211102711703](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211102711703.png)

保存成功后会在列表中展示

![image-20220211102733895](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211102733895.png)

##### (1.3) 附件环境

选择题目环境为：附件环境、上传附件、设置附件FLAG：这里填写的 FLAG 不会影响附件内的FLAG，值用于校验。所以附件中应已有FLAG存在。

![image-20220211103020677](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211103020677.png)

填写基本信息后点击保存即可

![image-20220211103142542](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211103142542.png)

发布成功后会在列表中显示

![image-20220211103757696](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211103757696.png)

#### (2) 题目搜索

在题目列表中可根据：题目名称、来源、描述、镜像 ID 进行搜索，输入搜索内容点击搜索即可

![image-20220211104116644](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211104116644.png)

点击`总共 [num]` 可返回所有题目列表

![image-20220211104309696](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211104309696.png)

#### (3) 题目过滤器

题目列表右侧过滤器可以选择： 题目难度、题目环境、题目类型、题目状态、创建时间、最近更新时间 进行多选过滤

![image-20220211133314359](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211133314359.png)

点击 “清除所有过滤器” 来显示所有内容

![image-20220211221523666](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211221523666.png)

#### (4) 题目信息编辑修改

点击题目名称可进入编辑相应题目

![image-20220211104403502](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211104403502.png)

修改完成后点击保存即可

![image-20220211104437840](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211104437840.png)

#### (5) 删除题目

删除题目后，会自动清理题目附件，但不会影响 Docker 镜像。

##### (5.1) 列表多选删除

可以通过列表处的多选，使用 ”删除所选题目“ 的动作点击执行，删除选中的题目

![image-20220211133508572](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211133508572.png)

##### (5.2) 题目详细中删除

在列表处，点击题目名称进入题目详细

![image-20220211133723883](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211133723883.png)

在点击底部的按钮进行删除，进行删除

![image-20220211133824052](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211133824052.png)

#### (6) 修改题目状态 - 上/下架题目

题目状态为下架时，前台是不会显示下架题目的。只有当题目状态为上架才会显示在前台的页面中

##### (6.1) 通过列表处修改状态

可以通过列表处的题目状态选择上/下架，选择完成后点击保存即可

![image-20220211134134358](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211134134358.png)

前台效果

![image-20220211134524780](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211134524780.png)

##### (6.2) 通过题目详细中修改状态

点击题目名称进入题目详细

![image-20220211134235164](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211134235164.png)

在题目中的题目状态选择相应状态后点击保存即可

![image-20220211134316377](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211134316377.png)

前台效果

![image-20220211134608932](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211134608932.png)

重新上架后会显示在相应类型中

![image-20220211134642764](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211134642764.png)

前台效果：进入相应题目类型

![image-20220211134725572](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211134725572.png)

即可看到题目

![image-20220211134742517](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211134742517.png)

#### (7) 排序

可以在列表页点击表头进行排序

![image-20220211224839728](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211224839728.png)

首次点击，如下效果为正序

![image-20220211224820707](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211224820707.png)

再次点击为降序

![image-20220211225913896](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211225913896.png)

鼠标移到表头处，点击如下按钮可清除该列的排序

![image-20220211225939737](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211225939737.png)

可多列同时进行排序

![image-20220211225956825](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211225956825.png)

### 3.1.3 靶机(容器)管理

用户启动题目容器后会在后台显示

![image-20220211213927702](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211213927702.png)

#### (1) 增加靶机

点击右上角增加 靶机(容器)

![image-20220211214015881](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211214015881.png)

选择题目（可以根据题目名称进行搜索）

![image-20220211214111395](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211214111395.png)

选择好后点击保存

![image-20220211214151514](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211214151514.png)

添加成功后，可以看到开放端口的信息 （当题目超过十条时，会自动分页，每页十条）

![image-20220211214210706](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211214210706.png)

可以通过浏览器访问

![image-20220211214751811](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211214751811.png)

#### (2) 靶机(容器)搜索

在题目列表中可根据：题目名称、用户名称、容器ID、镜像 ID 进行搜索，输入搜索内容点击搜索即可（这里我为了演示效果所有加多了一条数据）

![image-20220211221250076](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211221250076.png)

点击 **`总共 [num]` ** 可返回所有靶机(容器)列表

![image-20220211221348507](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211221348507.png)

#### (3) 靶机(容器) 过滤器

题目列表右侧过滤器可以选择： 创建时间、最近更新时间 进行多选过滤

![image-20220211221424546](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211221424546.png)

点击 “清除所有过滤器” 来显示所有内容

![image-20220211222208451](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211222208451.png)

#### (4) 靶机(容器) 信息编辑修改（无法编辑修改）

这里设计是一旦开启（环境）容器就无法镜像修改任何内容

![image-20220211214846762](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211214846762.png)

点击容器 ID 只能查看题目详细信息

![image-20220211214959956](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211214959956.png)

#### (5) 删除靶机(容器)

##### (5.1) 列表多选删除

可以通过列表处的多选，使用 ”删除所选靶机(容器)“ 的动作点击执行，删除选中的靶机(容器)

![image-20220211220057926](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211220057926.png)

##### (5.2) 容器详细中删除

在列表处，点击容器 ID 进入靶机(容器)详细

![image-20220211220630409](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211220630409.png)

点击底部的按钮进行删除，进行删除

![image-20220211220601107](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211220601107.png)

#### (6) 排序

可以在列表页点击表头进行排序

![image-20220211223724244](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211223724244.png)

首次点击，如下效果为正序

![image-20220211223759660](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211223759660.png)

再次点击为降序

![image-20220211224019525](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211224019525.png)

鼠标移到表头处，点击如下按钮可清除该列的排序

![image-20220211224117371](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211224117371.png)

可多列同时进行排序

![image-20220211224216723](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211224216723.png)

### 3.1.4 答题记录管理

用户在成功答题后，会答题记录中添加一条记录，在后台只有查看的权限。无法进行：增、删、改操作，

![image-20220211231024699](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211231024699-16445922358851.png)

### 3.1.5 用户管理

#### (1) 增加用户

在首页点击用户进入用户列表页面

![image-20220211232003562](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211232003562.png)

进入用户列表后，点击右上角 增加用户

![image-20220211231803163](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211231803163.png)

按照提示要求，完成填写用户名密码，点击保存即可

![image-20220211232148065](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211232148065.png)

保存成功后会进入该用户的详细编辑界面

![image-20220211232650426](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211232650426.png)

#### (2) 用户信息编辑修改

这里只提一些较为难理解的权限方面的帮助

##### (1.1) 基本状态

如下有三种状态：有效、工作人员、超级用户状态。其中在有效被选中时用户才可进行登录，当工作人员被勾选时可以登录后台，但不给予具体的权限只是能登录后台而已，无法进行任何操作。当勾选超级用户状态，无需给予具体权限可登录和操作后台所有功能（除开发者直接限制之外）。

![image-20220211233118429](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211233118429.png)

##### (1.2) 权限分配

前面说到可以分配具体权限，有两种形式：将用户添加到特定用户组中或者直接给予用户权限, 用户组后面说

![image-20220211233652500](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211233652500.png)

对一个模块权限分为：Can add 添加、Can change 修改、Can delete 删除、Can view 查看。  

![image-20220211235307553](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211235307553.png)

选择相应权限，点击中间的右箭头添加权限

![image-20220211235457742](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211235457742.png)

添加后效果

![image-20220211235600576](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211235600576.png)

为了方便演示，勾选上工作人员状态

![image-20220211235620812](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211235620812.png)

点击保存

![image-20220211235649660](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211235649660.png)

保存成功后可以看到工作人员状态已开启

![image-20220212000001210](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212000001210.png)

点击右上角注销，退出当前账户

![image-20220211235716505](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211235716505.png)

点击重新登录

![image-20220211235740066](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211235740066.png)

使用刚刚添加的用户进行登录

![image-20220211235755505](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220211235755505.png)

登录到后台，可以看到当前用户只能对题目进行管理

![image-20220212000029561](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212000029561.png)

选择 ”选中的 用户权限“ 里的权限，点击左箭头可以删除分配的权限

![image-20220212001439319](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212001439319.png)

登录后可以看到没有任何的权限

![image-20220212001622105](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212001622105.png)

#### (3) 用户密码修改

进入用户详细界面，点击 “这个表单” 进行密码修改

![image-20220212002252179](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212002252179.png)

根据提示要求，填写新密码，与确认密码点击右下角修改密码即可，此处为强制修改，无需输入旧密码。

![image-20220212002511242](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212002511242.png)

#### (4) 用户搜索

在题目列表中可根据：用户名、姓氏、名字、邮箱进行搜索查询

![image-20220212003258271](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212003258271.png)

点击 **`总共 [num]` ** 可返回所有用户列表

![image-20220212003326032](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212003326032.png)

#### (5) 用户过滤器

用户列表右侧过滤器可以选择： 工作人员状态、超级用户状态、是否有效、用户组 进行多选过滤

![image-20220212003411140](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212003411140.png)

点击 “清除所有过滤器” 来显示所有内容

![image-20220212003513227](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212003513227.png)

#### (6) 用户删除

##### (6.1) 列表多选删除

可以通过列表处的多选，使用 ”删除所选 用户“ 的动作点击执行，删除选中的用户

![image-20220212003831587](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212003831587.png)

##### (6.2) 用户详细中删除

在列表处，点击用户名进入用户详细页面

![image-20220212004104354](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212004104354.png)

点击底部的按钮进行删除，进行删除

![image-20220212004122216](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212004122216.png)

### 3.1.6 用户组管理

点击认证和授权中的 组 进入用户组列表

![image-20220212000149227](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212000149227.png)

#### (1) 增加用户组

进入用户组列表后点击右上角 增加 组

![image-20220212000447290](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212000447290.png)

输入用户组名称后，选择需要给予的权限，点击右箭头进行添加

![image-20220212001106363](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212001106363.png)

选择好后, 点击保存即可

![image-20220212001156723](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212001156723.png)

保存成功后会在列表中显示 （当题目超过十条时，会自动分页，每页十条）

![image-20220212001238028](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212001238028.png)

#### (2) 给用户分配用户组

进入用户详细，当前是刚刚演示中添加的用户 user001, 选择相应用户组，点击右箭头进行添加

![image-20220212001727310](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212001727310.png)

重新登录后可以看到效果与直接分配权限是一样的

![image-20220212001831585](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212001831585.png)

### 3.1.7 Captcha stores 验证码存储

用于存储生成的验证码，让其在后台显示的初衷是防止验证码垃圾数据过多，可以定时在后台清理记录。

### 3.1.8 邮箱认证 Token

用于存储生成的有效认证 Token，让其在后台显示的初衷是防止验证码垃圾数据过多，可以定时在后台清理记录。

## 3.2 前台使用说明

### 3.2.1 注册

打开站点后, 若没有登录，会自动跳转到登录页面。在登录页面点击 “点击注册” 跳转到注册页面

![image-20220212113330621](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212113330621.png)

输入邮箱，验证码点击立即注册，成功后会提示邮件已经发送指邮箱

![image-20220212113412996](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212113412996.png)

打开邮件后，可以看到提示点击连接完成注册，该链接 30 分钟内有效，超过 30 分钟后就需要重新获取。若收件箱中没有邮件，请检查邮箱地址是否正确，并查看垃圾邮件，检查邮件是否被拦截

![image-20220212113944487](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212113944487.png)

点击连接后会跳转到完成注册页面

![image-20220212114019132](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212114019132.png)

根据提示完成输入：用户名密码及确认密码，验证码点击提交即可

![image-20220212114102764](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212114102764.png)

注册完成后会自动跳转到登录页面

![image-20220212114138388](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212114138388.png)

### 3.2.2 登录

在登录页面根据提示输入用户名密码，验证码点击登录即可

![image-20220212114341164](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212114341164.png)

登录成功后会自动跳转到主页

![image-20220212114412972](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212114412972.png)

鼠标放在右上角的 “用户名和头像” 上，会显示 “个人中心” 及 “退出” 按钮，点击 “退出” 。会退出当前登录并跳转到登录页面

![image-20220212114532907](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212114532907.png)

### 3.2.3 忘记密码

在登录页面点击 “忘记密码？” 进入找回密码页面

![image-20220212114647584](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212114647584.png)

根据提示输入注册时的邮箱，验证码点击 “发送重置密码邮箱” 即可

![image-20220212114837286](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212114837286.png)

根据提示，在 30 分钟内点击右键中连接进行密码重置。若 30 分钟内为进行密码重置，该链接会失效，需要重新获取。若收件箱中没有邮件，请检查邮箱地址是否正确，并查看垃圾邮件，检查邮件是否被拦截

![image-20220212115319164](C:\Users\JOHNSON\Desktop\project\报告\image-20220212115319164-16446380990692.png)

跳转到重置密码页面后，根据提示输入密码、确认密码及验证码点击提交即可

![image-20220212115504891](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212115504891.png)

重置成功后会跳转到登录页面

![image-20220212115529675](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212115529675.png)

### 3.2.4 更换头像

鼠标放在右上角的 “用户名和头像” 上，会显示 “个人中心” 及 “退出” 按钮，点击 “个人中心” 。会跳转到当前用户的个人中心页面

![image-20220212115839056](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212115839056.png)

在个人中心页面可以看到自己的答题记录，邮件地址、当前积分等信息

![image-20220212120019747](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212120019747.png)

鼠标移动到头像上回提示 “更换头像” ，点击更换头像，会弹出文件选择窗口， 图片只允许 JPG 格式图片，大小最大在 400 × 400 像素。

![image-20220212120106244](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212120106244.png)

选择好后，即可替换成功。

![image-20220212120205284](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212120205284.png)

### 3.2.5 镜像环境答题

点击相应分类，注：并不是只有 Web 分类能设置镜像环境题目，而是我只在 Web 分类中添加了镜像环境

![image-20220212140509177](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212140509177.png)

进入题目后可以看到相题目，当当前分类及难度题目数量大于10题，会自动分页每页 10 题。

![image-20220212140602874](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212140602874.png)

可以通过难度一栏切换当前分类的难度级别

![image-20220212141038697](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212141038697.png)

点击 “入门” 切换至 入门难度，当前无入门难度的题目。

![image-20220212141652065](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212141652065.png)

点击题目可进入题目详细页面

![image-20220212141741896](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212141741896.png)

点击启动在线场景

![image-20220212141821109](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212141821109.png)

启动成功后会显示当前环境的连接，和倒计时，倒计时结束后，程序会自动销毁当前环境。

![image-20220212141840181](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212141840181.png)

访问提供的环境连接即可进行答题

![image-20220212141928863](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212141928863.png)

找到题目中的 Flag 后，将 Flag 输入到输入框中，点击提交即可

![image-20220212142006648](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212142006648.png)

提交成功后，会自动加分。

![image-20220212142038344](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212142038344.png)

当不需要环境时，可以点击 “删除场景” -> “确认” 进行删除

![image-20220212142100439](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212142100439.png)

答题完成后，在题目列表中，相应题目会变成金色

![image-20220212173833206](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212173833206.png)

可以在个人中心看到答题记录，及当前分数

![image-20220212142151332](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212142151332.png)

一个用户无法同时启动多个环境，当已经存在启动环境时，会提示：已启动 xxx 题目的环境，是否将其关闭并启动当前容器？

![image-20220212142216601](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212142216601.png)

当点击确认后，会关闭正在允许的环境，启动当前题目环境

![image-20220212142336312](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212142336312.png)

### 3.2.6 附件环境答题

进入到附件题目，点击附件，可以下载附件

![image-20220212173613711](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212173613711.png)

找到 flag 后，输入 Flag 点击提交即可

![image-20220212173642966](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212173642966.png)

提交成功

![image-20220212173709959](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212173709959.png)

答题完成后，在题目列表中，相应题目会变成金色

![image-20220212173929023](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212173929023.png)

### 3.2.7 排行榜

在排行榜中会显示，Top 10 的用户，只有积分大于 0 的情况下才会上榜。

![image-20220212234240910](https://gitee.com/J0hNs0N/read-me-images/raw/master/FlawPlatform%20%E6%BC%8F%E6%B4%9E%E9%9D%B6%E5%9C%BA.assets/image-20220212234240910.png)
