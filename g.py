#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# import urllib2
import re

import htmllib,urllib,formatter,string,os
import threading, multiprocessing
from multiprocessing import Value

url = 'http://www.deyilou3.com/plus/list.php?tid=10'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'

# headers = { 'User-Agent': user_agent}

# req = urllib2.Request(url, '', headers)

# response = urllib2.urlopen(req)

# the_page = response.read()

# re_pattern = '<a.*?href="(.+)".*?>(.*?)</a>'

# ret = re.search(re_pattern, the_page)


baseLink = 'http://www.deyilou3.com'

# sizeImg = 0

muxlock = threading.Lock()


''''' 
import chardet,sys 
type = sys.getdefaultencoding() 
'''  
class GetLinks(htmllib.HTMLParser): #从HTMLParser类中继承  
    def __init__(self): #初始化的时候调用，将links设置为空。这里的links为字典结构  
        self.links = {} #存放地址->链接的字典  
        self.isrcs = {}
        f = formatter.NullFormatter()#将传输过来的数据不做处理，格式化为数据流  
        htmllib.HTMLParser.__init__(self, f)  
  
    def anchor_bgn(self, href, name, type): #锚点标签开始的时候处理  
        self.save_bgn()  
        self.link = href  
  
    def anchor_end(self): #锚点标签结束的时候处理  
        text = string.strip(self.save_end()) #去掉A标签保留A标签的信息 
        # print(text) 
        if self.link and text:  
            self.links[text] = self.link#self.links.get(text, []) + [self.link]  
            #print self.links  
            #exit()  
    def handle_image(self,source, alt, ismap, align, width, height):
    	# print(source, alt)
    	# print(alt)
    	self.isrc = source
    	if source:
    		self.isrcs[source] = source

def mkdir(path):
	path = path.strip()
	path = path.rstrip('\\')
	if not os.path.exists(path):
		os.makedirs(path)
	return path


def countImg():
	sizeImg.value = sizeImg.value + 1
	print(sizeImg.value)
	print(multiprocessing.current_process().name)
	# muxlock.acquire()
	# with muxlock:
	# 	global sizeImg
	# 	sizeImg = sizeImg + 1
	# 	print(sizeImg)
	# 	print(multiprocessing.current_process().name)
	# muxlock.release()

def saveImg(path, file_name, data):
	if data == None:
		return

	mkdir(path)
	if(not path.endswith("/")):
		path = path + "/"

	print('*******')
	print('save file to '+ path+file_name)
	
	file = open(path+file_name, 'wb')
	file.write(data)
	file.flush()
	file.close()

def downloadImg(url):
	countImg()

	filename = os.path.basename(url)
	path = os.getcwd()
	path = os.path.join(path, 'imgs')
	if os.path.exists(os.path.join(path, filename)):
		return None
	try:
		fp = urllib.urlopen(url)
		data = fp.read()
		fp.close()
		saveImg(path, filename, data)
	except Exception as e:
		print(e)
		return None


def getImg(url, baseSrc='', linkFilter = None):
	try:
		fp = urllib.urlopen(url) #打开指定的URL  
		data = fp.read()  
		fp.close()  
	except Exception as e:
		print(e)
		return
	
	  
	linkdemo = GetLinks() #实例化一个LinkDemo对象  
	linkdemo.feed(data) #给HTMLParser喂食  
	linkdemo.close() 
	for src in linkdemo.isrcs.items():

		# print(src)
		srclink = baseSrc+src[1];
		if (linkFilter != None):
			if  srclink.find(str(linkFilter)) > -1:
				print(srclink)
				downloadImg(srclink)
		else:
			print(srclink)
			downloadImg(srclink)



def getAHtml(url, baseLink=''):
	try:
		fp = urllib.urlopen(url) #打开指定的URL  
		data = fp.read()  
		print(data)
		fp.close() 
	except Exception as e:
		print(e)
		return
	
	  
	linkdemo = GetLinks() #实例化一个LinkDemo对象  
	linkdemo.feed(data) #给HTMLParser喂食  
	linkdemo.close()  

	# getImg(url, baseLink);
	 
	for href, link in linkdemo.links.items(): #打印相关的信息 
		# print(link) 
		if link.find('tupian') > -1:
			print ("=>", baseLink+link) 
			getImg(baseLink+link, baseLink)
			# break


if __name__ == '__main__':
	urllist = 'http://www.deyilou3.com/plus/list.php?tid=10&TotalResult=490&PageNo='
	# getAHtml(url)
	baseLink = 'http://www.deyilou3.com'

	sizeImg = Value('i', 0)
	psize = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(processes = psize)

	# p1 = multiprocessing.Process(target = getAHtml, args=(url))
	# pool.apply_async(getAHtml, (url, baseLink))
	getAHtml(url, baseLink)
	# img = 'http://www.deyilou3.com/tupian/yazhou/2017/0805/2623.html'
	# getImg(img, 'http://www.deyilou3.com')
	for i in range(2,19):
		print(i)
		# getAHtml(urllist+str(i))
		# p = multiprocessing.Process(target=getAHtml, args=(urllist+str(i)))
		# p.start()
		# pool.apply_async(getAHtml, (urllist+str(i),))

	print('主进程任务结束 end!')
	pool.close()
	pool.join()
	print('子进程结束')
