import os,sys,enum,time,subprocess,platform
PLATFORM = platform.system()

try:
    import keyboard
except ImportError as e:
    print(e)
    sys.exit(1)
  
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

    def move(self, direction):
        value = self.position + direction
        if value < 0:
            value = len(self.root) - 1
        elif value > len(self.root) - 1:
            value = 0

        self.position = value
        self.print_dir()

    def update_dir(self, path: str = None):

        if not path == None:
            self.dir = path if len(path) > 2 else path + "\\"

        self.position = 0
        if not os.path.isdir(self.dir):
            return
        self.root = [Node('\\'.join(self.dir.split("\\")[:-1]), "..")]
        
        for root in os.listdir(self.dir):
            self.root.append(Node(self.dir + '\\' + root, root))
        self.print_dir()

    def print_dir(self):

        os.system('cls')
        print(Colors.BLUE + "Directory: " + self.dir + Colors.WHITE)
        terminal_size = os.get_terminal_size().lines - 3



        start = self.position - terminal_size if self.position > terminal_size else 0
        loop_amount = len(self.root) if len(self.root) < terminal_size else terminal_size + start + 1



        for i in range(start, loop_amount):

            if i == self.position:
                print(Colors.GREEN + '> ', end="")
            else:
                print(Colors.WHITE, end='')

            if self.root[i].type == FSType.DIRECTORY:
                print('├ ', end='')    

            print(self.root[i].name)
    
class Node:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.type = FSType.DIRECTORY if os.path.isdir(path) else FSType.FILE

def main():

    directory = Structure( 
        os.getcwd() )
    directory.update_dir()

    while True:

        match(keyboard.read_key()):
            case "up":
                directory.move(-1)
            case "down":
                directory.move(1)
            case "right" | "enter":
                item = directory.root[directory.position]
                if directory.root[directory.position].type == FSType.DIRECTORY:
                    directory.update_dir(item.path)
                else:
                    try:
                        if PLATFORM == 'Darwin':
                            subprocess.call(('open', item.path))
                        elif PLATFORM == 'Windows':
                            os.startfile(item.path)
                        else:
                            subprocess.call(('xdg-open', item.path))
                    except Exception:
                        print(f"{Colors.RED}ERROR: Could not open file '{item.name}'{Colors.WHITE}")
            case "left" | "backspace":
                directory.update_dir(directory.root[0].path)
            case "esc":
                print(Colors.YELLOW + "\nGoodbye!" + Colors.WHITE)
                time.sleep(0.5)
                sys.exit(1)

        time.sleep(0.125)
        

if __name__ == "__main__":
    main()