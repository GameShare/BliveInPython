#coding=utf-8
import SocketServer  
import threading
from SocketServer import StreamRequestHandler as SRH  
import urllib    
import urllib2 
import re
import json
import time

host = '133.130.116.215'  
port = 80
addr = (host,port)

OriginRoomId = 226
 
roomid = -1
roomStatus = -1
recentResult = ""
class Servers(SRH):  
    def handle(self):  
        print 'got connection from ',self.client_address  
        # self.wfile.write('connection %s:%s at %s succeed!' % (host,port,ctime()))  
        while True:  
            data = self.request.recv(1024)  
            if not data:   
                break  
            print data  
            print "RECV from ", self.client_address[0]  
            self.request.send(recentResult)

def checkRoomInfo(RoomId):
    req = urllib2.Request('http://live.bilibili.com/live/getInfo?roomid=' + str(RoomId))
    response = urllib2.urlopen(req)
    thepage = response.read().decode('utf-8')
    dictRes = json.loads(thepage)
    try:
        print dictRes["data"]['_status']
        return dictRes["data"]['_status']
    except:
        return -1

def downloadVideo(RoomId):
    print 1

def updateText():
    req = urllib2.Request("http://live.bilibili.com/"+str(OriginRoomId))
    response = urllib2.urlopen(req)
    thepage = response.read().decode('utf-8')
    pattern = re.compile(r'var ROOMID = \d*?;')
    matchRes = pattern.findall(thepage)
    if matchRes:
        print matchRes
        pattern = re.compile(r'\d+')
        matchRes = pattern.findall(matchRes[0])
        matchRes = matchRes[0]
        return matchRes
        # downloadVideo(matchRes)
    else:
        return -1
        print "无法获取房间的真实ID！"

server = SocketServer.ThreadingTCPServer(addr,Servers) 


server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print "Server loop running in thread:", server_thread.name

while 1:
    if roomid != -1:
        roomStatus = checkRoomInfo(roomid)
        if roomStatus != -1:
            recentResult = "房间状态"+roomStatus.encode("utf-8")
    else:
        roomid = updateText()

    if roomid == -1:
        recentResult = "无法获取房间的真实ID！"
    else:
        if roomStatus == -1:
            recentResult = "找到房间ID:"+str(roomid)

    time.sleep(10)





