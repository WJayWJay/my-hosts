
import os
import subprocess
from datetime import date
import sys
import urllib
import platform

def dl(mainhost, filename):
	print("从这里下载hosts文件:" + mainhost)
	print("下载文件到："+ filename)
	res =os.system("curl "+mainhost+" -o "+filename)
	print("文件下载中....")
	# f = urllib.urlopen(mainhost)
	# if f.getcode() == 200 :
	# 	print("文件下载成功")
	# 	data = f.read()
	# 	with open(filename, "wb") as fw:
	# 		fw.write(data)
	# else: 
	# 	print("下载失败"+str(res))
	# 	exit()
	
	print("下载hosts文件!")
	if res == 0:
		print("文件下载成功!")
	else:
		print("下载hosts文件失败!")
		exit()
		
				
def moveHost(frompath):
	print("从这里复制文件到hosts:"+frompath)
	sysver = platform.system()
	sysver = sysver.lower() 
	if( sysver == "windows"):
		topath = "C:\Windows\system32\dirvers\etc\hosts"
	else:
		topath = "/etc/hosts"

	

	# 分析hosts 文件
	# 取出自定义的host 和 ip

	today = date.today()
	print("今天是:" + str(today))
	oldpath = topath +"."+ str(today)
	print("备份老的hosts: 从"+topath+ "=>to:"+oldpath)
	ores =os.system("sudo mv " +topath + " " + oldpath)
	if ores == 0:
		print("备份成功!")

	print("复制hosts到/etc/:"+frompath + "=>" +topath)
	res = os.system("sudo cp "+ frompath + " " +topath)
	if res == 0:
		os.system("sudo killall -HUP mDNSResponder")
		print("hosts更新成功")
	else:
		os.system("sudo mv " + oldpath + " " + topath)
		print("hosts更新失败")

def getOthersHosts(hosts):
	lines = []
	if os.path.exists(hosts):
		with open(hosts) as f:
			while True:
				line = f.readline()
				if not line:
					break
				if line.find("127.0.0") != -1 or line.find(".gf.com.cn") != -1 :
					if line.lower().find("localhost") == -1 :
						lines.append(line)

	return lines



if __name__ == "__main__":
	mainhost = "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"
	filename = "hosts"
	currentpath = sys.path[0]
	fileversionname = currentpath+"/version_hosts"
	savepath = currentpath+"/hosts"
	 
	lastupdate = "Last updated"
	lastupdate = lastupdate.lower()

	liveVersion = ''

	needUpdate = False

	

# download files
	dl(mainhost, savepath)
	
	h = getOthersHosts("/etc/hosts")
	if len(h) != 0:
		print("有额外数据需要写入")
		sf = open(savepath, "a")
		try:
			for i in h:
				sf.write(i)
				print("写入的数据是:="+i)
		except Exception as e:
			print("文件异常")
			sf.close()
			exit()
		finally:
			sf.close()


	verContent = ''
	if os.path.exists(fileversionname):
		with open(fileversionname) as f:
			verContent = f.readline()

	with open(filename) as file:
		while True:
			line = file.readline()
			if not line:
				break
			if line.lower().find(lastupdate) != -1 and line.find('#') != -1:
				print(line)
				liveVersion = line
				source = line.split(":")
				if line.lower() != verContent.lower():
					needUpdate = True		
			
	
	print(needUpdate)
	if needUpdate:
		print("文件需要更新:"+str(needUpdate))
		with open(fileversionname, "w") as fv:
			fv.write(liveVersion)

		moveHost(savepath)
	else:
		print("不需要更新!")
		print("文件已经是最新版!")

	exit()
	
				
