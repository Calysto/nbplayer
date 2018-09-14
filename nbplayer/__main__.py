
from .nbplayer import TerminalNBPlayer, main
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    if len(sys.argv) > 2:
        goto = sys.argv[2]
    else:
        goto = 0
    main(filename, goto)
