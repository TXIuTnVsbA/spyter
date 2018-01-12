# spyter

自用爬虫小框架

    xpath(url,xp_context)
    
    url与xpath语句，返回一个列表或者某个类
    
    
    download(url,log)
    
    = =这个东西有缺陷的所以导致后面的xpath_download函数也有缺陷
    
    比如http://xxx.com/a/b/?123就出错了
    
    目前不知道怎么解决
    
    log=1时候打印出url
    
    
    
    list_thread(list,max = 16,target=None)
    
    根据列表元素的个数，使用多线程
    
    = =拿来多线程运行download函数的
    
    max=16,一边遍历一边运行，当遍历到第16个的时候阻塞并等待运行结束
    
    target，函数名
    
