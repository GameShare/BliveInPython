#coding=utf-8
from configobj import ConfigObj

import SocketServer  
import threading
from SocketServer import StreamRequestHandler as SRH  
import urllib    
import urllib2 
import re
import json
import time

class Servers(SRH):  
    def handle(self):
        global recentResult  
        # print 'got connection from ',self.client_address  
        # self.wfile.write('connection %s:%s at %s succeed!' % (host,port,ctime()))  
        while True:  
            data = self.request.recv(1024)  
            if not data:   
                break  
            # print data  
            # print "RECV from ", self.client_address[0]
            if recentResult != []:
                self.request.send(recentResult[0][:-1])
                recentResult = recentResult[1:]
            else:
                self.request.send("-1")

def checkRoomInfo(RoomId):
    req = urllib2.Request('http://live.bilibili.com/live/getInfo?roomid=' + str(RoomId))
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
    try：
        response = urllib2.urlopen(req)
    except:
        return -1
    thepage = response.read().decode('utf-8')
    dictRes = json.loads(thepage)
    if dictRes["data"]['_status'] == "on" or dictRes["data"]['_status'] == "off":
        return dictRes
    else:
        return -1

def downloadVideo(RoomId):
    print 1

def updateText(id):
    req = urllib2.Request("http://live.bilibili.com/"+str(id))
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
    try:
        response = urllib2.urlopen(req)
    except:
        try:
            response = urllib2.urlopen(req)
        except:     
            return -1
            print "无法获取房间"+str(id)+"的真实ID！请手动检查！"
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


# server start
iniFilePath = "./setting.ini"
config = ConfigObj(iniFilePath,encoding='UTF8')
if not("parameter" in config):
    config["parameter"] = {}
    config["parameter"]["host"] = '0.0.0.0'
    config["parameter"]["port"] = '80'
    config["parameter"]["OriginRoomId"] = [1]
    print "请手动修改配置文件！"
else:
    host = config["parameter"]["host"]  
    port = int(config["parameter"]["port"])
    OriginRoomId = config["parameter"]["OriginRoomId"]
    addr = (host, port)
     
    roomid = -1
    roomStatus = [0]*len(OriginRoomId)
    trueRoomId = [0]*len(OriginRoomId)
    recentResult = []

    server = SocketServer.ThreadingTCPServer(addr,Servers) 
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name

    temp = 0
    print OriginRoomId
    for i in OriginRoomId:
        roomid = updateText(int(i))
        trueRoomId[temp] = roomid
        if roomid == -1:
            recentResult += ["未找到房间" + i.encode("utf-8") + "的真实ID。\n"]
        # else:
        #     recentResult += "找到房间" + i + "的真实ID"+ str(roomid) + "。\n"       
        temp += 1  
        time.sleep(1)

    while 1:
        temp = 0
        for i in trueRoomId:
            if i != -1:
                nowRoomStatus = checkRoomInfo(i)
                if nowRoomStatus != -1:
                    if nowRoomStatus["data"]['_status'] == 'off' and roomStatus[temp] == 1:
                        recentResult += [nowRoomStatus["data"]['ANCHOR_NICK_NAME'].encode("utf-8")+"的房间"+"关闭了！.\n"]
                        roomStatus[temp] = 0
                    else:
                        if nowRoomStatus["data"]['_status'] == 'on' and roomStatus[temp] == 0:
                            recentResult += [nowRoomStatus["data"]['ANCHOR_NICK_NAME'].encode("utf-8")+"的房间"+"开始直播了！.\n"]
                            roomStatus[temp] = 1
                else:
                    recentResult += ["房间"+OriginRoomId[temp]+"的状态出错!\n"]
            temp += 1
            time.sleep(1)
        time.sleep(60)





