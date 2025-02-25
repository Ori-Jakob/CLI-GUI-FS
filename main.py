import sys,os,time,subprocess,platform,GUI

try:
    import keyboard
except ImportError as e:
    print(e)
    sys.exit(1)
  
PLATFORM = platform.system()

def main():

    directory = GUI.Structure( 
        os.getcwd() )
    directory.update_dir()

    while True:

        match(keyboard.read_key()):
            case "up":
                directory.move(-1)
            case "down":
                directory.move(1)
            case  "right":
                directory.move(os.get_terminal_size().lines - GUI.TERMINAL_OFFSET)
            case "left":
                directory.move(-1 * (os.get_terminal_size().lines - GUI.TERMINAL_OFFSET))
            case "space":
                directory.mark()
            case"enter":
                item = directory.root[directory.position]
                prior_path = directory.dir
                if directory.root[directory.position].type == GUI.FSType.DIRECTORY:
                    try:
                        directory.update_dir(item.path)
                    except Exception as e:
                        print(e)
                        print(GUI.Colors.RED + "Error: Access to directory is denied.")
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
                        print(f"{GUI.Colors.RED}ERROR: Could not open file '{item.name}'{GUI.Colors.WHITE}")
            case "backspace":
                directory.update_dir(directory.root[0].path)
            case "esc":
                print(GUI.Colors.YELLOW + "\nGoodbye!" + GUI.Colors.WHITE)
                time.sleep(0.5)
                sys.exit(1)

        time.sleep(0.13)
        

if __name__ == "__main__":
    main()