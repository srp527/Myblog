# SRP

## 博客网址:http://srpblog.wangsir.wang

模块安装：

    pip freeze >requirements.txt   #导出安装过的库
    pip install -r requirements.txt

大致思路：

   
    1，创建django项目 Myblog
    2，创建app  users、blogarticle、operation
    3，配置 settings.py

      注册app

      #通过自定义userprofile覆盖默认user表
      AUTH_USER_MODEL = 'users.UserProfile'

      数据库连接

      xadmin配置
      python manage.py createsuperuser


      pip install django-pure-pagination  #分页用的包
      注意：TypeError: 'Page' object is not iterable


项目说明:

    个人练手项目;
    记录一些学习过程中遇到的问题和网上查到的解决方法以及自己的一些总结,
    功能上没有添加太多


博客 试用账号:

    账号:test
    密码:testtest

登入方式: 

    用户名或邮箱地址都可 (注册 暂时没有加邮箱验证功能)

基本功能:

    0.文章的增/改/删
    1.按标签分类文章
    2.简单权限管理: 用户只能操作自己的文章,admin可以操作所有
    3.用户头像/个人信息修改
  





