import sys,os,time
from GUI import Structure
import hotkeys as h


def main():
    directory = Structure( os.getcwd() )
    directory.update_dir(restore=True)
    h.setup_hotkeys(directory)

    while True:
        if os.get_terminal_size().lines != directory.current_window_lines: 
            directory.current_window_lines = os.get_terminal_size().lines
            directory.print_dir()
        if h.SHOULD_EXIT:
            sys.exit(1)

        time.sleep(0.15)
        
if __name__ == "__main__":
    main()