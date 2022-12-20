#weibo_photo_crawl
微博相册批量爬取

开发工具

windows10

pycharm

### 编译环境
Python 3.10.4 (tags/v3.10.4:9d38120, Mar 23 2022, 23:13:41) [MSC v.1929 64 bit (AMD64)] on win32

### 简介
pip install requests (安装requests模块)
pip install pyyaml (安装yaml模块)

### 使用说明
main是程序入口
运行前在config.yml下粘贴自己的cookie(注意yaml的格式,冒号后面空一格),cookie的获取可以在打开chrome微博->f12->network->任意选择一个请求复制headers里的cookie
(cookie易失效,有效期大概24小时)

运行后根据终端提示输入微博用户的uid(网址上面有),格式为纯数字,如3669102477
