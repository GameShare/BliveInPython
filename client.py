#coding=utf-8

import sys
import socket
import time
import subprocess
from PyQt4 import QtGui, QtCore

layer = 20
timeP = 1000
delay = 9000
slot = 5000
HOST='133.130.116.215'
PORT=8080

def OnTimer():
	try:
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((HOST,PORT))
		cmd = 'new data?'
		s.sendall(cmd)
		data=s.recv(1024)
		s.close()
		# print data
		if data != "-1":
			insertMessage(data)
		# s.close()
	except:
		s.close()
		insertMessage("socket出错！")

def insertMessage(str):
	parameterStr = '{"ShortcutFileName":"DesktopToast.Proxy.lnk","ShortcutTargetFilePath":"C:DesktopToast.Proxy.exe","ToastTitle":"DesktopToast Proxy Sample","ToastBody":"' + str.decode('utf-8') + u'","AppId":"DesktopToast.Proxy",}'
	# print sys.getfilesystemencoding()
	sub = subprocess.Popen(["DesktopToast.Proxy.exe",parameterStr.encode(sys.getfilesystemencoding())])

def appQuit():
	print "OK!"
	app.quit()
	
app = QtGui.QApplication(sys.argv)

 
icon = QtGui.QIcon("icon.ico")
trayIcon = QtGui.QSystemTrayIcon(app)
trayIcon.setIcon(icon)
trayIcon.setToolTip("Blive")
trayIcon.show()
trayIcon.activated.connect(appQuit)
timer=QtCore.QTimer()
QtCore.QObject.connect(timer,QtCore.SIGNAL("timeout()"), OnTimer)
timer.start( slot )

sys.exit(app.exec_())

