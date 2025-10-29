from src.utils.net_deck_builder import cyberdeck
from src.utils.hitpoints import health
from src.utils.roll import roll
import math

NET_ACTIONS = ['jack_in',
               'jack_out',
               'move',
               'scanner',
               'backdoor',
               'cloak',
               'control',
               'eyedee',
               'pathfinder',
               'slide',
               'virus',
               'zap',
               'rez_program']

class netrunner():

    def __init__(self):
        self.cyberdeck = cyberdeck()
        self.health = health()
        self.set_interface_rank()
        self.speed_bonus = 0
        self.scanner_bonus = 0
        self.backdoor_bonus = 0
        self.cloak_bonus = 0
        self.control_bonus = 0
        self.eyedee_bonus = 0
        self.pathfinder_bonus = 0

    def set_interface_rank(self, rank:int=1):
        self.interface = rank

    def net_action(self, action:str, modifier:int=0):
        action = action.lower()


        roll_result = roll() + self.interface
        match action:
            case 'jack_in':
                return self.jack_in()
            case 'jack_out':
                return self.jack_out()
            case 'move':
                return self.move()
            case 'scanner':
                return self.scanner()
            case 'backdoor':
                return self.backdoor()
            case 'cloak':
                return self.cloak()
            case 'control':
                return self.control()
            case 'eyedee':
                return self.eyedee()
            case 'pathfinder':
                return self.pathfinder()
            case 'slide':
                return self.slide()
            case 'virus':
                return self.virus()
            case 'zap':
                return self.zap()
            case _:
                print(f"Action '{action}' not recognized. Valid actions are: {NET_ACTIONS}")
                return None
    # def jack_in():
    #     pass

    # def jack_out():
    #     pass

    # def move(self):
    #     pass
    
    # def scanner(self):
    #     scanner_roll = roll() + self.INTERFACE_RANK + self.scanner_bonus
    #     return scanner_roll

    # def backdoor(self):
    #     pass

    # def cloak(self):
    #     pass

    # def control(self):
    #     pass

    # def eyedee(self):
    #     pass

    # def pathfinder(self):
    #     pass

    # def slide(self):
    #     pass

    # def virus(self):
    #     pass

    # def zap(self):
    #     pass
    pass