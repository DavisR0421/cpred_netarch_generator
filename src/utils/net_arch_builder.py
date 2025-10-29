import pprint
import random
import datetime as dt
class Floor:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class BranchingFloor:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next1 = None
        self.next2 = None

class NetArchitecture:
    def __init__(self):
        self.head = None
        self.root_floor = ''
        self.branches = 0
        self.floorlevels = {}
        self.validroot = False
        self.name = f'net_architecture_{dt.datetime.today().date().strftime('%y%m%d')}'
        # Initialize the class with an empty head

    def _track_root(self, floor_name):
        self.root = floor_name

    def _get_level(self,floor_name):
        # print(f"floor name: {floor_name}\nfloor level:{floor_name[13:]}")
        return int(floor_name[13:])
    
    def _track_levels(self, floor_name):
        level = self._get_level(floor_name)

        if self.floorlevels.get(level) is not None:
            nfloors = self.floorlevels.get(level)+1
            self.floorlevels.update({level:nfloors})
        else:
            self.floorlevels[level] = 1
        
        rootfloor = max(self.floorlevels.keys())
        if self.floorlevels[rootfloor] > 1:
            self.validroot = False
        else:
            self.validroot = True
    
    def set_name(self,newname:str=None):
        if not newname:
            self.name = input("> Choose a name for this net architecture: ")
        else: 
            self.name = newname
        print(f" Architecture Name set as [{self.name}]")

    def get_name(self)->str:
        return self.name

    def validate_root(self)->bool:
        return self.validroot

    def get_root_identity(self)->str:
        print(f"\nthe root floor is {self.root}\n")
        return self.root

    # visualize an inchworm: The tail ('last') moves up to the body ('current') defore pushing the body ('current') to the next spot 'next').
    def append(self, data:dict, branching:bool=False, control_branching:bool=False)->None:
        floor_num = data.get('floor_id')
        if floor_num < 2:
            data['branch'] = 0
            data['floor_name']=f"b.000.{data['branch']}::f.0.{floor_num+1}"
            data['floor_path'] = f"{'' if floor_num == 0 else f"b.000.{data['branch']}::f.0.{floor_num}"}////{data['floor_name']}"

        if branching:
            new_node = BranchingFloor(data)
        else:
            new_node = Floor(data)
        
        if not self.head:
            self.head = new_node
            # pprint.pprint(new_node.data)
            self._track_root(new_node.data.get('floor_name'))
            self._track_levels(new_node.data.get('floor_name'))
            return

        last = self.head
        while True:
            if isinstance(last, BranchingFloor):
                if last.next1 is None:
                    last.next1 = new_node
                    new_node.prev = last
                    new_node.data['branch'] = last.data['branch']
                    new_node.data['floor_name'] = f"b.000.{new_node.data['branch']}::f.0.{int(last.data['floor_name'][13:])+1}"
                    new_node.data['floor_path'] = f"{last.data['floor_path']}//{new_node.data['floor_name']}"
                    self._track_root(new_node.data.get('floor_name'))
                    self._track_levels(new_node.data.get('floor_name'))
                    # pprint.pprint(new_node.data)
                    return
                elif last.next2 is None:
                    last.next2 = new_node
                    new_node.prev = last
                    new_node.data['branch'] = last.data['branch'] + self.branches
                    self.branches += 1
                    new_node.data['floor_name'] = f"b.000.{new_node.data['branch']}::f.0.{int(last.data['floor_name'][13:])+1}"
                    new_node.data['floor_path'] = f"{last.data['floor_path']}//{new_node.data['floor_name']}"
                    self._track_root(new_node.data.get('floor_name'))
                    self._track_levels(new_node.data.get('floor_name'))
                    # pprint.pprint(new_node.data)
                    return
                
                if control_branching:
                    whichway = None
                    # whichway_options = f"'1' : {last.next1.data['floor_name']}\n'2' : {last.next2.data['floor_name']}"
                    while whichway not in ['1','2']:
                        whichway = str(
                            input(
                                f"\n> branching at {last.data['floor_name']}"
                                f"\n> path: branch path {last.data['floor_path']}"
                                f"\n> '1' : {last.next1.data['floor_name']}"
                                f"\n> '2' : {last.next2.data['floor_name']}"
                                f"\n> choose '1' or '2' for branch to continue: "
                            )
                        )
                        if whichway == '1':
                            last = last.next1
                        elif whichway == '2':
                            last = last.next2
                        else:
                            print("\nthat's not one of the options laserbrain. try again.")
                else:
                    last = random.choice([last.next1, last.next2])
            else:
                if last.next is None:
                    last.next = new_node
                    new_node.prev = last
                    new_node.data['branch'] = last.data['branch']
                    new_node.data['floor_name'] = f"b.000.{new_node.data['branch']}::f.0.{int(last.data['floor_name'][13:])+1}"
                    new_node.data['floor_path'] = f"{last.data['floor_path']}//{new_node.data['floor_name']}"
                    self._track_root(new_node.data.get('floor_name'))
                    self._track_levels(new_node.data.get('floor_name'))
                    # pprint.pprint(new_node.data)
                    return
                last = last.next
            
            # print(pprint.pprint(last.data))


    def move_forward(self, steps=1):
        current = self.head
        count = 0
        while count<steps and (isinstance(current, Floor) and current.next ) or (isinstance(current, BranchingFloor) and current.next1):
            if isinstance(current, BranchingFloor) and (current.next1 and current.next2):
                whichway_options = [current.next1.data['floor_id'], current.next2.data['floor_id']]
                whichway = None
                while whichway not in whichway_options:
                    whichway = input(f"\n> network branch found\n> choose next branch\n> {whichway_options}: ")
                    if whichway == whichway_options[0]:
                        current = current.next1
                        count += 1
                    elif whichway == whichway_options[1]:
                        current = current.next2
                        count += 1
                    else:
                        print("\nthat's not one of the options laserbrain. try again.")
            elif isinstance(current, BranchingFloor) and current.next1:
                current = current.next1
            elif isinstance(current, Floor):
                current = current.next
            count += 1
        print(current)
        return current  # returns the node at the specified number of steps forward
    
    def move_backward(self, steps=1):
        current = self.head
        # Move to the end of the list first
        while current and current.next:
            current = current.next
        count = 0
        # Now move backwards the specified number of steps
        while current and count < steps:
            current = current.prev
            count += 1
        return current  # returns the node at the specified number of steps backward

    # def display(self):
    #     current = self.head
    #     while current:
    #         print(current.data, end="\n -> ")
    #         if current.next:
    #             current = current.next
    #         elif current.next1:
    #             current = current.next1
    #             print("showing branch 1 - will aff functionality to show all branches later")
    #     print("None")

    def display(self):
        def _dfs(node, visited):
            if node in visited:
                return
            visited.add(node)
            print(node.data, end="\n -> ")
            # Traverse all branches if they exist
            if hasattr(node, 'next') and node.next:
                _dfs(node.next, visited)
            if hasattr(node, 'next1') and node.next1:
                print("showing branch 1")
                _dfs(node.next1, visited)
            if hasattr(node, 'next2') and node.next2:
                print("showing branch 2")
                _dfs(node.next2, visited)
            # Add more branches as needed

        visited = set()
        _dfs(self.head, visited)
        print("None")