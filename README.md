# s1_spider
db 用的 PostgreSQL，自己建库吧，表名用户名能不能改我忘记了。**创建表**：utils/init_db.py

**基本功能**：接收指定的 thread_id（帖子id），然后爬取该帖拆开按回复存放到数据库中。

例如要爬取卓明谷版规帖：

帖子地址为 https://bbs.saraba1st.com/2b/thread-334540-1-1.html

则 thread_id 为 334540

**两个需要自行设置的配置文件：**

- config/config.ini

用于设置数据库配置、用户名及密码信息；

爬虫基于selenium，引擎使用Firefox。

免窗口模式未测试。另外还有关于检测是否登录入自动登录的偶发性bug未修。

- config/s1_account.ini

用不用随意，用于存储登录网站的用户名/密码。
