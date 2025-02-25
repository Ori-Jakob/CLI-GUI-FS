import os,time,platform,sys,subprocess
from GUI import FSType,Structure,TERMINAL_OFFSET,Colors

try:
    import keyboard
except ImportError as e:
    print(e)
    sys.exit(1)

PLATFORM = platform.system()
SHOULD_EXIT = False

def do_enter(directory: Structure):
    item = directory.root[directory.position]
    prior_path, prior_pos = directory.dir, directory.position

    if directory.root[directory.position].type == FSType.DIRECTORY:
        try:
            directory.update_dir(item.path)
        except Exception as e:
            print(e)
            print(Colors.RED + "Error: Access to directory is denied.")
            time.sleep(1)
            directory.update_dir(prior_path, prior_pos)
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

def do_esc(directory: Structure):
    global SHOULD_EXIT
    print(Colors.YELLOW + "\nGoodbye!" + Colors.WHITE)
    time.sleep(0.5)
    SHOULD_EXIT = True
    sys.exit(1)
    
def setup_hotkeys(directory: Structure):
    keyboard.add_hotkey("up", lambda: directory.move(-1))
    keyboard.add_hotkey("down", lambda: directory.move(1))
    keyboard.add_hotkey("right", lambda: directory.move(os.get_terminal_size().lines - TERMINAL_OFFSET))
    keyboard.add_hotkey("left", lambda: directory.move(-1 * (os.get_terminal_size().lines - TERMINAL_OFFSET)))
    keyboard.add_hotkey("space", lambda: directory.mark())
    keyboard.add_hotkey(",", lambda: directory.undo())
    keyboard.add_hotkey("backspace", lambda: directory.update_dir(directory.root[0].path))
    keyboard.add_hotkey("enter", lambda: do_enter(directory))
    keyboard.add_hotkey("esc", lambda: do_esc(directory))
    keyboard.add_hotkey("ctrl+a", lambda: directory.mark_all())