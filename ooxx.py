#coding: utf-8 #############################################################  
# File Name: main.py  
# Author:    
# mail:    
# Created Time: Wed 11 Jun 2014 08:22:12 PM CST  
#########################################################################  
#!/usr/bin/python  
  
import re,urllib2,threading,Queue
import sys,time,socket,os  
import sqlite3,md5

def dataInsert(path,insertStr,insertData):


def getHtml(PageUrl):
    req_header = {'User-Agent':'Mozilla/6.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    try:
        request=urllib2.Request(PageUrl,None,req_header)
        HTMLStr=urllib2.urlopen(request,None,timeout=30).read()
        print 'Html Download Success!'
    except Exception, e:
        print e
        return 0
    except socket.timeout as e:
        print e
        return 0
    return HTMLStr

def getDocument(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def getNextPage(Tmphtml):
    preRegex=r'previous-comment-page" href="http://jandan[.]net/ooxx/page-\d+#comments'
    prepattern=re.compile(preRegex)
    prePage=prepattern.search(Tmphtml)
    rHtml=r'http://jandan[\.]net/ooxx/page-\d+#comments'
    rHtmlpattern=re.compile(rHtml)
    nextPage=rHtmlpattern.search(prePage.group()).group()
    print 'NextPage is %s'%nextPage
    return nextPage

#下载第几页
DownRound=0
insertData=[]
def getImage(path,HTMLTempStr):
    '''
    正则获取gif、jpg、png和下一页
    '''
    if imageDownloadCount:
        tNum=imageDownloadCount
    else:tNim=0;
    print 'Rex going'
    regImage=r'(http\W+(\S)+[\.]jpg)|(http\W+(\S)+[\.]gif)'
    #regImage=r'(http\W+(\S)+[\.]gif)'
    patternImage=re.compile(regImage)
    imageUrl=re.finditer(patternImage, HTMLTempStr)
    print 'Rex going'
    if not imageUrl:
        print u'没有获取到图片地址'
        sys.exit()
#    insertData=[]
    for match in imageUrl:
        URL=match.group()
        filename=URL.split('/')[-1]
        fullname=path+filename
        if not os.path.exists(fullname):
            global f
            f.put({filename:fullname})
    return fullname,filename
#已下载图片数量
imageDownloadCount=0            
def downImage(DownList):##DownList=[URL,fullname,filename]
    for URL,fullname,filename in DownList:
        print u'下载文件: %s'%filename
        #文件下载
        try:
            cont=urllib2.urlopen(URL,timeout=13).read()
            f=open(fullname,'wb')
            f.write(cont)
            f.close()
            global imageDownloadCount
            global DownRound
            imageDownloadCount=imageDownloadCount+1
            print u'第 %d 页,第 %d 个图像下载完成'%(DownRound,imageDownloadCount)
            print u'第 %d 页,共下载 %d 个图像'%(DownRound,imageDownloadCount-tNum)
        except Exception,e:
            print e
     #下载下一页图片
    global DownRound
    DownRound=DownRound+1
    if DownRound<=12:
        nextPage=getNextPage(HTMLTempStr)
        getImage(path,getHtml(nextPage)) 
        

#图片保存目录
save_Path=u'E:/Girls/'
#开始的网址
page=1
#startPage='http://jiandan.net/ooxx/page-1569#comments'
#startPage='http://jiandan.net/ooxx/page-1558#comments'
#startPage='http://jiandan.net/ooxx/page-1534#comments'
#startPage='http://jiandan.net/ooxx/page-1486#comments'
#startPage='http://jiandan.net/ooxx/page-1534#comments'
#startPage='http://jiandan.net/ooxx/page-1770#comments'
startPage='http://jiandan.net/ooxx/page-'+str(page)+'#comments'
path=getDocument(save_Path)
html=getHtml(startPage)
getImage(path,html)
