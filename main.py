import os,sys,enum,time,subprocess,platform
PLATFORM = platform.system()
try:

    import keyboard
except Exception as e:
    print(e)
    sys.exit(1)
    

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class FSType(enum.Enum):
    FILE = 1
    DIRECTORY = 2
    LINK = 3
    OTHER = 4

class Structure:
    def __init__(self):
        self.root = list()
        self.position = 0

    def move(self, direction):
        value = self.position + direction
        if value < 0:
            value = len(self.root) - 1
        elif value > len(self.root) - 1:
            value = 0

        self.position = value
        self.print_dir()

    def update_dir(self, path):
        self.position = 0
        if not os.path.isdir(path):
            return
        self.root = [Node('\\'.join(path.split("\\")[:-1]), "...")]
        
        for root in os.listdir(path):
            self.root.append(Node(path + '\\' + root, root))
        self.print_dir()

    def print_dir(self):

        os.system('cls')
        terminal_size = os.get_terminal_size().lines - 3



        start = self.position - terminal_size if self.position > terminal_size else 0
        loop_amount = len(self.root) if len(self.root) < terminal_size else terminal_size + start + 1



        for i in range(start, loop_amount):

            if i == self.position:
                print(bcolors.OKGREEN + '> ', end="")


            else:
                print(bcolors.ENDC, end='')

            if self.root[i].type == FSType.DIRECTORY:
                print('/', end='')    

            print(self.root[i].name)
    
class Node:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.type = FSType.DIRECTORY if os.path.isdir(path) else FSType.FILE

def main():

    directory = Structure()
    directory.update_dir( os.getcwd() )

    while True:
        match(keyboard.read_key()):

            case "up":
                directory.move(-1)
            case "down":
                directory.move(1)
            case "right" | "enter":
                path = directory.root[directory.position].path
                if directory.root[directory.position].type == FSType.DIRECTORY:
                    directory.update_dir(path)
                else:
                    if platform.system() == 'Darwin':
                        subprocess.call(('open', path))
                    elif platform.system() == 'Windows':
                        os.startfile(path)
                    else:
                        subprocess.call(('xdg-open', path))
            case "left" | "backspace":
                directory.update_dir(directory.root[0].path)

        time.sleep(0.125)
        

if __name__ == "__main__":
    main()