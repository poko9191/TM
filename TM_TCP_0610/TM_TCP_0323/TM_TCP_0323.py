#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import socket
import tkinter as tk
import binascii

HOST = '192.168.0.70'
PORT = 5890

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


while True:
    outdata = input('please input message: ')

    # 只是print出寄了什麼東西，可刪掉
    print('send: '  + outdata)  

    #計算DATA長度，+2是因為從逗點開始計算，前後都有逗點，有+2就可以不用打逗點
    datalength = len(outdata) + 2

    # 把固定的str寫死加到指令裡面
    packet = str('TMSCT,') + str(datalength) + str(',1,') + outdata + str(',')
    print(packet)

    # ======計算校驗碼(CS)======
    # 用XOR方式計算
    xor = 0
    i = 0
    while i < len(packet):
        xor = xor ^ ord(packet[i])
        i += 1

    CS = hex(xor)[2:]
    print(CS)

    #把指令整理好
    tmp = str('$').encode() + packet.encode() + str('*').encode() + CS.encode()+ str('\r\n').encode()
   
    #印出指令並送出
    print(tmp)
    s.send(tmp)
    
    #收指令並印出
    indata = s.recv(1024)
    print(type(indata))
    if len(indata) == 0:  # connection closed
        s.close()
        print('server closed connection.')
        break
    print('recv: ' + indata.decode())
    break


# =================================================程式打法=====================================================
# 直接打 PTP("JPP",0,0,0,0,90,0,10,200,0,false)
# 送出，收到 $TMSCT,x,x,OK,*xx (x會變動) 表示指令正確，手臂會開始動，沒有開始動就跟成哥講，打給TM






    # 確定可用指令
    # =====程式內部指令=====
    # TMSCT,40,1,PTP("JPP",0,0,0,0,90,0,10,200,0,false),
    
    # =====TM原生指令打法=====
    # $TMSCT,40,1,PTP("JPP",0,0,0,0,90,0,10,200,0,false),*30
    
    # =====指令說明=====
    # $TMSCT(固定Title不變),40(data長度從id後面逗點開始算),1(ID),PTP("JPP",0,0,0,0,90,0,10,200,0,false),*30(校驗碼)


    # ==================TM說明書上的指令==================
"""  $TMSCT,,1,PTP("JPP",-90,0,90,0,90,0,20,200,0,false)
PTP("JPP",0,0,90,0,90,0,20,200,0,false)
PTP(“JPP”,90,0,90,0,90,0,20,200,0,false),*2C(換行) """

"""$TMSCT,,1,PTP("JPP",-90,0,90,0,90,0,20,200,0,false)
PTP("JPP",0,0,90,0,90,0,20,200,100,false)
PTP("JPP",90,0,90,0,90,0,20,200,0,false),*22 (換行)"""

""" $TMSCT,44,1,PTP("JPP",90,0,90,0,90,0,10,200,0,false),*33 """
    # ====================================================
