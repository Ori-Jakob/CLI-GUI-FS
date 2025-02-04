import os,sys,enum

class FSType(enum.Enum):
    FILE = 1
    DIRECTORY = 2
    LINK = 3
    OTHER = 4

class Structure:
    def __init__(self):
        self.root = ["..."]
        return self
    def update_dir(self, path):
        if not os.path.isdir(path):
            return
        self.root = ["..."]
        for root, dirs, files in os.walk(path):
            for name in files:
                self.root.append(Node(os.path.join(root, name), name))
            for name in dirs:
                self.root.append(Node(os.path.join(root, name), name))
    
class Node:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.type = FSType.FOLDER if os.path.isdir(path) else FSType.FILE

def main():
    working_dir = os.getcwd()
    onlyfiles = [f for f in os.listdir(working_dir) if os.isfile(os.path.join(working_dir, f))]
    print(onlyfiles)

if "__name__" == "__main__":
    main()