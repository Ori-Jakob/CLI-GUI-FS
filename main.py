import os,sys,enum,time,subprocess,platform
PLATFORM = platform.system()
TERMINAL_OFFSET = 4

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

    def update_dir(self, path: str = None):

        if not path == None:
            self.dir = path if path.count('\\') > 0 else path + "\\"

        self.position = 0
        if not os.path.isdir(self.dir):
            return
        self.root = [Node('\\'.join(self.dir.split("\\")[:-1]), "..")]
        
        for root in os.listdir(self.dir):
            self.root.append(Node(self.dir + '\\' + root, root))
        self.print_dir()
    def __instructions__(self):
        print(Colors.YELLOW + "UP/DOWN=Move up/down, LEFT/RIGHT=Move up/down page, ENTER=Open folder/file,  BACKSPACE=Move up directory" + Colors.BLUE)
        print("Directory: " + self.dir + Colors.WHITE)

    def print_dir(self):

        os.system('cls')
        self.__instructions__()
        terminal_size = os.get_terminal_size().lines - TERMINAL_OFFSET



        start = self.position - terminal_size if self.position > terminal_size else 0
        loop_amount = len(self.root) if len(self.root) < terminal_size else terminal_size + start + 1



        for i in range(start, loop_amount):

            if i == self.position:
                print(Colors.GREEN + '> ', end="")
            else:
                print(Colors.WHITE, end='')

            if self.root[i].type == FSType.DIRECTORY:
                print('├─', end='')    

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
            case  "right":
                directory.move(os.get_terminal_size().lines - TERMINAL_OFFSET)
            case "left":
                directory.move(-1 * (os.get_terminal_size().lines - TERMINAL_OFFSET))
            case"enter":
                item = directory.root[directory.position]
                prior_path = directory.dir
                if directory.root[directory.position].type == FSType.DIRECTORY:
                    try:
                        directory.update_dir(item.path)
                    except Exception as e:
                        print(Colors.RED + "Error: Access to directory is denied.")
                        time.sleep(1)
                        directory.update_dir(prior_path)
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
            case "backspace":
                directory.update_dir(directory.root[0].path)
            case "esc":
                print(Colors.YELLOW + "\nGoodbye!" + Colors.WHITE)
                time.sleep(0.5)
                sys.exit(1)

        time.sleep(0.13)
        

if __name__ == "__main__":
    main()