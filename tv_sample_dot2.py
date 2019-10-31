import pyxel
import time

on = False
channel = [1,2,4,5,6,7,8,9]
now = 0
vol = 10
volcon = 0

#pyxel.load('tv_resource.pyxres')
pyxel.init(60, 45)

def changechannel(now,x):
    if x == 1:
        now+=1
    if x == -1:
        now-=1
    return now%8


def channelToImage(c):
    if c == 1:
        return 8
    if c == 2:
        return 3
    if c == 3:
        return 8
    if c == 4:
        return 9
    if c == 5:
        return 14
    if c == 6:
        return 12
    if c == 7:
        return 10
    if c == 8:
        return 6
    if c == 9:
        return 2
def volumeChange(vol,x):
    if x == 1:
        if vol<30:
            vol += 1

    if x == -1:
        if 0<vol:
            vol -= 1

    return vol


while True:

    if on:
        pyxel.cls(channelToImage(channel[now]))
        pyxel.text(5, 5, str(channel[now]), 0)

        if volcon > 0:
            pyxel.text(int(pyxel.width/2), int(pyxel.height)-5, "vol:{}".format(vol), 0)
            volcon -= 1

        #pyxel.flip()


        if pyxel.btnr(pyxel.KEY_RIGHT):
            now = changechannel(now,1)
        if pyxel.btnr(pyxel.KEY_LEFT):
            now = changechannel(now,-1)
        if pyxel.btnr(pyxel.KEY_UP):
            pyxel.cls(channelToImage(channel[now]))
            pyxel.text(int(pyxel.width)-5, 5, str(channel[now]), 0)
            vol = volumeChange(vol,1)
            volcon = 50


        if pyxel.btnr(pyxel.KEY_DOWN):
            pyxel.cls(channelToImage(channel[now]))
            pyxel.text(int(pyxel.width)-5, 5, str(channel[now]), 0)
            vol = volumeChange(vol,-1)
            volcon = 50


    else:
        pyxel.cls(0)
        #pyxel.flip()


    if pyxel.btnr(pyxel.KEY_O) and on==False:
        for i in range(0,int(pyxel.height/2),10):
            pyxel.cls(0)
            pyxel.rect(0, int(pyxel.height/2)-i, pyxel.width, i*2, 7)
            #pyxel.flip()
        on = True
        pyxel.cls(7)
        #pyxel.flip()
        time.sleep(0.1)


    if pyxel.btnr(pyxel.KEY_O) and on==True:
        for i in range(int(pyxel.height/2)-1,-1,-10):
            pyxel.cls(0)
            pyxel.rect(0, int(pyxel.height/2)-i, pyxel.width, i*2, 7)
            #pyxel.flip()
        on = False
        volcon = 0
