# 相关代码已经修改调试成功----2017-4-5  #
## **一、说明** ##

**1.目标网址：**[豆瓣网](https://www.douban.com)

2.实现：模拟登录豆瓣，验证码处理，登录到个人主页就算是success。

3.数据：没有抓取数据，此实战主要是模拟登录和处理验证码的学习。要是有需求要抓取数据，编写相关的抓取规则即可抓取内容。

本项目是在scrapy的基础上实现的，主要代码是spiders文件夹下的py文件，其他py文件基本没什么改动，对scarpy有一定了解的应该都看的懂。

登录成功展示如图：
![](http://images2015.cnblogs.com/blog/1129740/201704/1129740-20170405213650035-747309275.png)

## **二、运行** ##
1. 先填入自己**豆瓣的账号和密码，若快打码平台的帐号和密码**，代码中都是*号的位置；
2. 运行start.py文件即可运行；

## 三、问题----欢迎留言提出问题 ##
声明：本项目主要是学习scrapy模拟登录
> 1. 豆瓣的验证码是英文字母，长度不知道，识别成功率比较低；
> 2. 登录失败时，我用yield Request(url,callback=self.start_request)为什么会不行。每次登录失败都是重新运行start.py（待解决）
> 3. 如果运行程序结束，什么都没有输出，打开豆瓣网站看看，是否有 Please try later.提示，这时候就需要换用代理ip，代理IP池请看我博客：[python爬虫实战（三）--------搜狗微信文章（IP代理池和用户代理池设定----scrapy）](http://www.cnblogs.com/jinxiao-pu/p/6665180.html) 

**欢迎有兴趣的小伙伴帮我优化，解决以上问题，之后我将合并你的代码，作为贡献者,共同成长。**

## **四、笔记** ##
知识点：

1. return Request的用法

		return [Request(url=url,meta={"cookiejar":1},callback=self.parse)]   #可以传递一个标示符来使用多个。如meta={'cookiejar': 1}这句，后面那个1就是标示符
1. 打码平台的使用
	
		直接利用验证码图片的url接口即可
1. FormRequest的用法

		return [
		     FormRequest.from_response(
		         response,
		         meta={"cookiejar":response.meta["cookiejar"]},
		         headers=self.header,
		         formdata=data,
		         callback=self.get_content,
		     )
		 ]

----------
如果本项目对你有用请给我一颗star，万分感谢。 