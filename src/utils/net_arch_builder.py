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
        # Initialize the class with an empty head

    # visualize an inchworm: The tail ('last') moves up to the body ('current') defore pushing the body ('current') to the next spot 'next').
    def append(self, data:dict, branching:bool=False)->None:
        floor_num = data.get('floor_id')
        if floor_num < 2:
            data['branch'] = 0
            data['floor_name']=f"b.000.{data['branch']}::f.0.{floor_num+1}"
            data['floor_path'] = f"{'' if floor_num == 0 else f"b.000.{data['branch']}::f.0.{floor_num}"}/{data['floor_name']}"

        if branching:
            new_node = BranchingFloor(data)
        else:
            new_node = Floor(data)
        
        if not self.head:
            self.head = new_node
            return

        last = self.head
        while True:
            if isinstance(last, BranchingFloor):
                if last.next1 is None:
                    last.next1 = new_node
                    new_node.prev = last
                    new_node.data['branch'] = last.data['branch'] + 1 
                    new_node.data['floor_name'] = f"b.000.{new_node.data['branch']}::f.0.{int(last.data['floor_name'][13:])+1}"
                    new_node.data['floor_path'] = f"{last.data['floor_path']}/{new_node.data['floor_name']}"
                    return
                elif last.next2 is None:
                    last.next2 = new_node
                    new_node.prev = last
                    new_node.data['branch'] = last.data['branch'] + 2
                    new_node.data['floor_name'] = f"b.000.{new_node.data['branch']}::f.0.{int(last.data['floor_name'][13:])+1}"
                    new_node.data['floor_path'] = f"{last.data['floor_path']}/{new_node.data['floor_name']}"
                    return
                
                whichway = None
                whichway_options = {'1':last.next1.data['floor_name'],'2':last.next2.data['floor_name']}
                while whichway not in whichway_options or whichway_options.keys():
                    whichway = input(f"\n> branching at {last.data['floor_name']}\
                                    \nbranch path {last.data['floor_path']}\
                                    \n> choose '1' or '2' for branch to continue \
                                    \n> {whichway_options}: ")
                    if whichway == list(whichway_options.keys())[0] or whichway_options['1']:
                        last = last.next1
                    elif whichway == list(whichway_options.keys())[1] or whichway_options['2']:
                        last = last.next2
                    else:
                        print("\nthat's not one of the options laserbrain. try again.")
            else:
                if last.next is None:
                    last.next = new_node
                    new_node.prev = last
                    new_node.data['branch'] = last.data['branch']
                    new_node.data['floor_name'] = f"b.000.{new_node.data['branch']}::f.0.{int(last.data['floor_name'][13:])+1}"
                    new_node.data['floor_path'] = f"{last.data['floor_path']}/{new_node.data['floor_name']}"
                    return
                last = last.next


    def move_forward(self, steps=1):
        current = self.head
        count = 0
        while current and any(current.next,current.next1,current.next2):
            if current.next1 and current.next2:
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
            elif current.next1:
                current = current.next1
            else:
                current = current.next
            count += 1
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

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")