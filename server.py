#coding=utf-8
import sip
import sys
import SocketServer  
import threading
from SocketServer import StreamRequestHandler as SRH  
from time import ctime  
from PyQt4 import QtGui, QtCore

time = 10000
host = '127.0.0.1'  
port = 8883
addr = (host,port)  
transMessage = ""
class Example(QtGui.QWidget):
	
	def __init__(self):
		super(Example, self).__init__()
		self.label = [QtGui.QLabel(self)]
		self.labelNum = 0
		self.temp = [0,0]

		self.initUI()
	def initUI(self):
		#self.setGeometry(300, 300, 280, 170)

		# 透明度
		self.setWindowOpacity(1)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		# 去除边框
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.OnTimer)

		self.qp = QtGui.QPainter()
		self.adjustSize()
		self.show()

	def OnTimer(self):
		self.timer.stop()
		if transMessage != "":
			self.insertMessage(transMessage)
		temp = len(self.label)-2
		for i in self.label[:0:-1]:
			i.setGeometry(self.label[temp].x(), self.label[temp].y(), i.width(), i.height())
			temp -= 1
		temp = 0
		sip.delete(self.label[0])
		for i in self.label[1:]:
			self.label[temp] = i
			temp += 1

		del self.label[len(self.label)-1]
		print self.label
		self.labelNum -= 1
		if len(self.label) != 0:
			self.timer.start( time )


	def paintEvent(self, e):

		self.qp.begin(self)
		tempPosi = [0, 0];
		for i in self.label:
			tempPosi[0] += i.width()
			tempPosi[1] += i.height()
		self.qp.fillRect(0,0,tempPosi[0],tempPosi[1]+10, QtGui.QColor(0,0,0,169))
		# self.qp.fillRect(self.label[0].x(),self.label[0].y()-5,self.label[0].width(),self.label[0].height()+10, QtGui.QColor(0,0,0,169))
		self.qp.end()


	def keyPressEvent(self, e):

		if e.key() == QtCore.Qt.Key_Escape:
			server.shutdown()
			server.server_close()
			self.close()
		else:
			if e.key() == QtCore.Qt.Key_A:
				self.insertMessage("test")


	def mousePressEvent(self, e):
		self.temp = [e.x(), e.y()]

	def mouseMoveEvent(self,e):
		self.setGeometry(self.x()+e.x()-self.temp[0], self.y()+e.y()-self.temp[1], self.width(), self.height())
		self.temp[0]

	def insertMessage(self, str):
		tempLabel = QtGui.QLabel(self)
		tempLabel.setText(str)
		tempLabel.setFont(QtGui.QFont("Microsoft Yahei",25))
		if self.labelNum != 0:
			tempLabel.setGeometry(self.label[self.labelNum-1].x(), self.label[self.labelNum-1].y()+self.label[self.labelNum-1].height()+30,self.label[self.labelNum-1].width(),self.label[self.labelNum-1].height())
		else:
			self.timer.start( time )
		# 自动调整大小
		tempLabel.adjustSize()
		tempLabel.setAlignment(QtCore.Qt.AlignCenter)
		# 设置颜色
		pe = QtGui.QPalette() 
		pe.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,255,255,255))#设置字体颜色 
		tempLabel.setPalette(pe)

		tempLabel.show()

		self.labelNum += 1
		self.label += [tempLabel]

		self.adjustSize()

class Servers(SRH):  
    def handle(self):  
        print 'got connection from ',self.client_address  
        self.wfile.write('connection %s:%s at %s succeed!' % (host,port,ctime()))  
        while True:  
            data = self.request.recv(1024)  
            if not data:   
                break  
            print data  
            print "RECV from ", self.client_address[0]  
            transMessage = data
            # trans.insertMessage(data)
            # self.request.send(data)
		
app = QtGui.QApplication(sys.argv)
trans = Example()
server = SocketServer.ThreadingTCPServer(addr,Servers) 
# Start a thread with the server -- that thread will then start one
# more thread for each request
server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print "Server loop running in thread:", server_thread.name

sys.exit(app.exec_())