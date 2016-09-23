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
port = 8080
addr = (host,port)

OriginRoomId = [226, 83264, 17111, 157901, 17770, 1267341, 98612, 60470, 57119, 36613, 323467, 39019, 44055, 37755, 32055, 17784, 226, 30507, 5299]
 
roomid = -1
roomStatus = -1
recentResult = ""

class Servers(SRH):  
    def handle(self):
        global recentResult  
        print 'got connection from ',self.client_address  
        # self.wfile.write('connection %s:%s at %s succeed!' % (host,port,ctime()))  
        while True:  
            data = self.request.recv(1024)  
            if not data:   
                break  
            print data  
            print "RECV from ", self.client_address[0]
            if recentResult != "":
                self.request.send(recentResult[:-1])
                recentResult = ""
            else:
                self.request.send("-1")

def checkRoomInfo(RoomId):
    req = urllib2.Request('http://live.bilibili.com/live/getInfo?roomid=' + str(RoomId))
    response = urllib2.urlopen(req)
    thepage = response.read().decode('utf-8')
    dictRes = json.loads(thepage)
    try:
        # print dictRes["data"]['_status']
        return dictRes
    except:
        return -1

def downloadVideo(RoomId):
    print 1

def updateText(id):
    req = urllib2.Request("http://live.bilibili.com/"+str(id))
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
        print "无法获取房间"+str(id)+"的真实ID！请手动检查！"

server = SocketServer.ThreadingTCPServer(addr,Servers) 


server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print "Server loop running in thread:", server_thread.name


trueRoomId = [0]*len(OriginRoomId)
temp = 0
for i in OriginRoomId:
    roomid = updateText(i)
    trueRoomId[temp] = roomid
    if roomid == -1:
        recentResult += "未找到房间" + str(i) + "的真实ID。\n"
    else:
        recentResult += "找到房间" + str(i) + "的真实ID"+ str(roomid) + "。\n"
    
    temp += 1  
    time.sleep(1)

while 1:
    temp = 0
    for i in trueRoomId:
        if i != -1:
            roomStatus = checkRoomInfo(i)
            if roomStatus != -1:
                recentResult += dictRes["data"]['ANCHOR_NICK_NAME'].encode("utf-8")+"的房间"+str(OriginRoomId[temp])+"的状态为:"+dictRes["data"]['_status'].encode("utf-8")+".\n"
            else:
                recentResult += "房间"+str(OriginRoomId[temp])+"的状态出错!\n"
        
        temp += 1
        time.sleep(1)
    time.sleep(60)





