# TGBot

# 简介

这是一个个人娱乐的TelegramBot机器人项目、管理员页面支持。

包括一下几个功能

- 菜单按钮
- 多级菜单
- 硅基流动、chatGPT支持
- 每日新闻
- 签到功能
- 多语言支持
- 后端bot管理

# 使用说明
## python版本3.10+

## 安装配置mysql

```mysql
-- 新建一个tgbot库
create database tgbot charset = utf8;
```

## 配置文件

- 按照eg.ini为模板、新建.env文件、填入对应的值即可

- [硅基流动平台注册链接](https://cloud.siliconflow.cn/i/AJcwLpuG)、注册立即送2000万TOKEN

- [API-TOKEN连接](https://cloud.siliconflow.cn/account/ak)（填入配置文件open_key的值）

# 运行程序

CTR + C: STOP

```CMD
python main.py

# 注意取消main.py文件的既可每次自动编译po文件
compile_mo_files()

```

# 效果图如下

<img src="static/start.png" alt="开始菜单" style="zoom: 80%;" />

<img src="static/菜单.png" alt="开始菜单" style="zoom: 80%;" />
    
<img src="static/管理员页面.png" alt="管理员页面" style="zoom: 80%;" >    
