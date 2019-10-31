import pyxel
import time




#pyxel.load('tv_resource.pyxres')


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

class TV:
    def __init__(self):
        self.onoff = False
        self.channel = [1,2,4,5,6,7,8,9]
        self.now = 0
        self.vol = 10
        self.volcon = 0
        self.range = 0
        pyxel.init(60, 45)
        pyxel.run(self.update,self.draw)

    def update(self):

        if self.onoff:

            if pyxel.btnr(pyxel.KEY_RIGHT):
                self.now = changechannel(self.now,1)
            if pyxel.btnr(pyxel.KEY_LEFT):
                self.now = changechannel(self.now,-1)
            if pyxel.btnr(pyxel.KEY_UP):
                pyxel.cls(channelToImage(self.channel[self.now]))
                pyxel.text(int(pyxel.width)-5, 5, str(self.channel[self.now]), 0)
                self.vol = volumeChange(self.vol,1)
                self.volcon = 50


            if pyxel.btnr(pyxel.KEY_DOWN):
                pyxel.cls(channelToImage(self.channel[self.now]))
                pyxel.text(int(pyxel.width)-5, 5, str(self.channel[self.now]), 0)
                self.vol = volumeChange(self.vol,-1)
                self.volcon = 50

        if pyxel.btnr(pyxel.KEY_O) and self.onoff==True:
            self.onoff = False
            self.range = int(pyxel.height/2)
            self.volcon = 0

        if pyxel.btnr(pyxel.KEY_I) and self.onoff==False:
            self.onoff = True
            self.range = 0
            print(self.onoff)


    def draw(self):

        if self.onoff:
            pyxel.cls(channelToImage(self.channel[self.now]))
            if self.range < int(pyxel.height/2):
                pyxel.rect(0, int(pyxel.height/2)-self.range, pyxel.width, self.range*2, 7)
                self.range += 5
            pyxel.text(5, 5, str(self.channel[self.now]), 0)

        else:
            pyxel.cls(0)
            if 0 < self.range:
                pyxel.rect(0, int(pyxel.height/2)-self.range, pyxel.width, self.range*2, 7)
                self.range -= 5


        if self.volcon > 0:
            pyxel.text(int(pyxel.width/2), int(pyxel.height)-5, "vol:{}".format(self.vol), 0)
            self.volcon -= 1

TV()
