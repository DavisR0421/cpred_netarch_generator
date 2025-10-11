import random

def roll(die_num:int=1, die_type:str='d10', inorder:bool=False, calledshot:bool=False, rollmod:int=0) -> int:

    diemax = int(die_type[1:])
    if calledshot and die_type == 'd10':
        rollmod-=8


    rolls = [{'roll':random.randint(1, diemax),'modifier':rollmod} for _ in range(die_num)]
    result = sum([r['roll'] + r['modifier'] for r in rolls])
    if inorder:
        return result, rolls
    else:
        return result
    
if __name__ == "__main__":
    result, rolls = roll(3, 'd10', True, True, 2)
    print(f"\nroll 3d10, in order, called shot, +2 situational modifier:\nresult:{result}\nrolls:{rolls}")

    result = roll(2, 'd10')
    print(f"\nroll 3d10\nresult:{result}")