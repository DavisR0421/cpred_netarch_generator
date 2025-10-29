from math import round

class health():
    def __init__(self):
        self.set_hitpoints()
        self.set_enable_woundstate()
        self.set_enable_deathsaves()
        self.check_pulse()

    def check_pulse(self):
        if self.enable_deathsaves and self.deathsavefailed:
            self.alive = False
        elif not self.enable_deathsaves and self.hp == 0:
            self.alive = False
        else:
            self.alive=True

    def set_enable_woundstate(self, enable:bool=True):
        self.enable_woundstate = enable

    def set_enable_deathsaves(self, enable:bool=True):
        self.enable_deathsaves = enable
        if self.enable_deathsaves:
            self.deathsavefailed = False

    def set_hitpoints(self, hitpoints:int=10):
        self.hp = hitpoints
        self.hpmax = hitpoints
        self.woundthreshold = round(hitpoints/2)

    def get_hitpoints(self):
        return self.hp
    
    def get_maxhitpoints(self):
        return self.hpmax
    
    def take_damage(self, damage:int):
        self.hp = max(self.hp-damage,0)
        if self.enable_woundstate:
            self.set_woundstate()
        return self.hp
    
    def set_woundstate(self):
        if self.hp >= self.woundthreshold:
            self.woundedpenalty = 0
        elif 0 < self.hp < self.woundthreshold:
            self.woundedpenalty = -2
        else:
            self.woundedpenalty = -4

    def get_woundstate(self):
        w_pen = self.woundedpenalty
        if w_pen == 0 and self.hp < self.hpmax:
            return {"state":"Lightly Wounded","penalty":0}
        elif w_pen == -2:
            return {"state":"Seriously Wounded","penalty":-2}
        elif w_pen == -4:
            return {"state":"Mortally Wounded","penalty":-4}
        else:
            return {"state":"Not Wounded","penalty":0}
        
