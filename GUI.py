import os,enum
TERMINAL_OFFSET = 4

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'

class FSType(enum.Enum):
    FILE = 1
    DIRECTORY = 2
    LINK = 3
    OTHER = 4

class Structure:
    def __init__(self, path):
        self.dir = path
        self.root = list()
        self.position = 0
        self.marked = {}

    def move(self, direction):
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

    def mark(self):

        if self.position == 0: return

        temp = self.root[self.position]

        if not temp in self.marked:
            temp.is_marked = True
            items = self.marked.get(self.dir, -1)
            if items != -1:
                items.append(temp)
            else:
                self.marked[self.dir] = list()
                self.marked[self.dir].append(temp)
        else:
            temp.is_marked = False
            items = self.marked.get(self.dir, -1)
            if items != -1:
                items.pop(items.index(temp))
        self.print_dir()
        
    def update_dir(self, path: str = None):

        if not path == None:
            self.dir = path if path.count('\\') > 0 else path + "\\"

        self.position = 0
        if not os.path.isdir(self.dir):
            return
        self.root = [Node('\\'.join(self.dir.split("\\")[:-1]), "..", 0)]
        
        items = self.marked.get(self.dir, -1)
        for key, root in enumerate(os.listdir(self.dir)):
            if items != -1:
                found_pos = self.__find_marked__(key + 1)
                if found_pos > -1:
                    self.root.append(self.marked[self.dir][found_pos])
                else:
                    self.root.append(Node(self.dir + '\\' + root, root, key + 1))
            else:
                self.root.append(Node(self.dir + '\\' + root, root, key + 1))

        self.print_dir()

    def __instructions__(self):
        print(Colors.YELLOW + "UP/DOWN=Move up/down, LEFT/RIGHT=Move up/down page, ENTER=Open folder/file,  BACKSPACE=Move up directory" + Colors.BLUE)
        print("Directory: " + self.dir + Colors.WHITE)

    def __find_marked__(self, position):
        items = self.marked.get(self.dir, -1)
        if items == -1: return -1

        for x in range(len(items)):
            if items[x].position == position:
                return x

        return -1    

    def print_dir(self):

        os.system('cls')
        self.__instructions__()
        terminal_size = os.get_terminal_size().lines - TERMINAL_OFFSET



        start = self.position - terminal_size if self.position > terminal_size else 0
        loop_amount = len(self.root) if len(self.root) < terminal_size else terminal_size + start + 1



        for i in range(start, loop_amount):
            string = "[{0}] ".format("X" if self.root[i].is_marked else " ") if i != 0 else ""
            if i == self.position:
                print(Colors.GREEN + string, end="")
            else:
                print(Colors.WHITE + string, end='')

            if self.root[i].type == FSType.DIRECTORY:
                print('├─', end='')    

            print(self.root[i].name)
    
class Node:
    def __init__(self, path, name, pos):  
        self.path = path
        self.name = name
        self.position = pos
        self.type = FSType.DIRECTORY if os.path.isdir(path) else FSType.FILE
        self.is_marked = False
