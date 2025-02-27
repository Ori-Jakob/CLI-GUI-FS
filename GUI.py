import os, psutil
from enum import Enum

TERMINAL_OFFSET = 4

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'

class Action(Enum):
    FILE_SYSTEM = 0
    CHANGE_DRIVE = 1

class FSType(Enum):
    FILE = 1
    DIRECTORY = 2
    DRIVE = 3
    OTHER = 4

class Structure:
    def __init__(self, path):
        self.dir = path
        self.root = list()
        self.position = 0
        self.marked = {}
        self.stack = list()
        self.current_window_lines = os.get_terminal_size().lines
        self.not_all_marked = True
        self.current_action = Action.FILE_SYSTEM

    def move_cursor(self, direction):
        value = self.position + direction
        if value < 0:
            if direction < -1 and self.position != 0:
                value = 0
            else:
                value = len(self.root) - 1
        elif value > len(self.root) - 1:
            if direction > 1 and self.position != len(self.root) - 1:
                value = len(self.root) - 1
            else:    
                value = 0

        self.position = value
        self.print_dir()

    def mark(self, pos=-1):

        if pos == -1 and self.position == 0: return # don't allow marking ".." (going up a dir)

        temp = self.root[self.position] if pos == -1 else self.root[pos]

        #TO-DO: Folder marking
        #we will not allow folder marking until I can come up with an implementation
        if temp.type == FSType.DIRECTORY: return

        if len(temp.path) == 0: return #don't allow makring if there is nothing in the folder

        if not temp in self.marked.get(self.dir, []):
            temp.is_marked = True
            items = self.marked.get(self.dir, -1)
            if items != -1:
                items.append(temp)
            else:
                self.marked[self.dir] = list()
                self.marked[self.dir].append(temp)
        else:
            if pos == -1: self.not_all_marked = True
            temp.is_marked = False
            items = self.marked.get(self.dir, -1)
            if items != -1:
                items.pop(items.index(temp))

        if pos == -1: self.print_dir() #only update imediately if we aren't marking all


    def mark_all(self):
        for i in range(len(self.root)):
            #TO-DO: Allow folder marking
            if self.root[i].type == FSType.FILE:
                if self.root[i].is_marked != self.not_all_marked: self.mark(pos=i)

        self.not_all_marked = not self.not_all_marked
        self.print_dir()

    def change_drive(self):
        self.current_action = Action.CHANGE_DRIVE
        self.__track__()
        disks = psutil.disk_partitions()
        dir = list()
        for x in range(len(disks)):
            dir.append(Node(disks[x][0], disks[x][1], x, FSType.DRIVE))
        self.dir = ""
        self.root = dir
        self.position = 0
        self.print_dir()

    def update_dir(self, path: str = None, pos: int = -1, restore=False):

        
        if self.dir != "" and not restore and self.dir != path: self.__track__()
        if self.dir != "" and not os.path.isdir(self.dir): return
        if not path == None:
            self.dir = path if path.count('\\') > 0 else path + "\\"

        self.current_action = Action.FILE_SYSTEM
        self.position = 0 if pos == -1 else pos
        new_dir = self.__path_join__(self.dir.split("\\"), "\\")
        self.root = [Node(new_dir, "..", 0, None if new_dir != "" else FSType.OTHER)]
        
        items = self.marked.get(self.dir, -1)

        for key, root in enumerate(os.listdir(self.dir)):
            try:
                path = os.path.join(self.dir, root)
                if os.path.isdir(path): os.listdir(path) #throw an error if no acccess to folder
                
                if items != -1:
                    found_pos = self.__find_marked__(key + 1)
                    if found_pos > -1:
                        self.root.append(self.marked[self.dir][found_pos])
                    else:
                        self.root.append(Node(path, root, key + 1))
                else:
                    self.root.append(Node(path, root, key + 1))
            except Exception:
                pass

        self.print_dir()

    def print_dir(self):

        os.system('cls')
        self.__instructions__()
        terminal_size = os.get_terminal_size().lines - TERMINAL_OFFSET

        start = self.position - terminal_size if self.position > terminal_size else 0
        loop_amount = len(self.root) if len(self.root) < terminal_size else terminal_size + start + 1

        for i in range(start, loop_amount):

            item = self.root[i]
            #TO-DO: Folder marking
            #we will not allow folder marking until I come up with a way to implement it
            #if i == 0 or self.root[i].file_count == 0: string = ""
            if item.type != FSType.FILE or item.type == FSType.OTHER: string = "" 
            else:
                if item.type == FSType.DIRECTORY:
                    temp = len(self.marked.get(item.path, []))
                    try:
                        dir_len = len(os.listdir(item.path))
                        if dir_len != 0 and temp == dir_len: value = "X"
                        elif temp > 0: value = "-"
                        else: value = " "
                    except Exception:
                        value = " "
                else:
                    if item.is_marked:
                        value = "X"
                    else:
                        value = " "
                string = "[{0}] ".format(value)
            if i == self.position:
                self.__color_print__(string, color=Colors.GREEN, end="")
            else:
                self.__color_print__(string, color=Colors.WHITE, end="")

            if item.type != FSType.FILE:
                print(' ├─', end='')    

            print(item.name)

    def undo(self):
        if len(self.stack) == 0: return 
        state = self.stack.pop()
        self.dir = state[0]
        self.update_dir(pos=state[1], restore=True)

    def __instructions__(self):
        self.__color_print__(u"[\u2191/\u2193]=UP/DOWN | [\u2190/\u2192]=PAGE UP/DOWN | [ENTER]=OPEN\
 | [BACKSPACE]=.. | [<]=UNDO" + f"({len(self.stack)}) | [CTRL+A]=UN/MARK ALL | [CTRL+D]=CHANGE DRIVE", color=Colors.YELLOW)
        match(self.current_action):
            case Action.CHANGE_DRIVE:
                self.__color_print__("Select a drive:", Colors.BLUE)
            case Action.FILE_SYSTEM:
                self.__color_print__("Directory: " + self.dir, Colors.BLUE)

    def __find_marked__(self, position):
        items = self.marked.get(self.dir, -1)
        if items == -1: return -1

        for x in range(len(items)):
            if items[x].position == position:
                return x

        return -1    

    def __path_join__(self, path: list, str_join: str):
        string = str()
        if len(path) > 2: string = str_join.join(path[:-1])
        elif len(path) == 2: string = path[0] + str_join
        if string == self.dir: string = ""
        return string
    
    def __track__(self):
        if len(self.stack) > 9: return
        state = [self.dir, self.position]
        self.stack.append(state)

    def __color_print__(self, string, color=Colors.WHITE, end="\n"):
        print(color+string, end=end)
    
class Node:
    def __init__(self, path, name, pos, type=None):  
        self.path = path
        self.name = name
        self.position = pos
        self.type = type if type != None else FSType.DIRECTORY if os.path.isdir(path) else FSType.FILE
        self.file_count = len(os.listdir(path)) if self.type == FSType.DIRECTORY else -1
        self.is_marked = False
