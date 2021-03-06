"""
A Jupyter notebook console executer.

"""

from IPython.utils.capture import capture_output
import jupyter_client
import nbformat
import cmd
import sys
import os

TIMEOUT = 30

help_text = """
nbplayer
========

A simple terminal player for Jupyter notebooks

* empty line - execute current cell and advance
* n - next cell (skip this one)
* p - previous cell
* NUMBER - goto cell
* +AMOUNT - goto cell ahead, relative movement
* -AMOUNT - goto cell previous, relative movement
* --POSITION - from end
* ! shell command - execute command at the operating system
* q or ^d - quit nbplayer

Possible future options:

* re search forward/reverse for cell with next match
* run all code cells up to here
* i - insert cell
* d - delete cell
* u - undo operation in stack
* r - redo operation in stack
* code - show only code (toggles on/off)
"""

class TerminalNBPlayer(cmd.Cmd):
    intro = ''

    def __init__(self, filename, goto=0):
        super().__init__()
        self.filename = filename
        self.current_cell = int(goto)
        self.environment = {}
        self.goto = None
        self.max_col_width = 72
        self.max_rows = 40
        self.nb = nbformat.read(filename, as_version=4)
        kernel_name = self.nb["metadata"]["kernelspec"]["name"]
        self.manager, self.client = jupyter_client.manager.start_new_kernel(kernel_name=kernel_name)

    @property
    def prompt(self):
        filename = os.path.basename(self.filename)
        return "%s [%s/%s] > " % (filename, self.current_cell, len(self.nb.cells))

    def preloop(self):
        from ._version import __version__
        print('nbplayer %s: type `help` or `?` to see commands\n' % __version__)
        print("Viewing: %s" % self.filename)
        print("--------------------------------------------------------\n")
        self.show_current_cell()
    
    def show_current_cell(self):
        print("In [%s]:" % self.current_cell)
        print()
        cell = self.nb.cells[self.current_cell]
        self.show_cell(cell)

    def postcmd(self, stop, line):
        if stop:
            return True
        if self.goto is not None:
            ## Handle goto's here
            self.current_cell = self.goto
            self.goto = None
            self.show_current_cell()
            return
        if self.nb.cells[self.current_cell]["cell_type"] == "code":
            ## Execute the current cell
            results = self.execute_code(self.nb.cells[self.current_cell]["source"])
            if results is not None:
                print("Out [%s]:" % self.current_cell, repr(results))
            print()
        ## advance to next
        self.current_cell += 1
        self.show_current_cell()

    def execute_code(self, source):
        with capture_output() as io:
            reply = self.client.execute_interactive(source, timeout=TIMEOUT)
        print(io.stdout, file=sys.stdout)
        sys.stdout.flush()
        print(io.stderr, file=sys.stderr)
        sys.stderr.flush()
        # reply['content']['status'] == 'ok'
        results = None ## FIXME: how to get output from capture_output()?
        return results
        
    def emptyline(self): ## this is needed to override default behavior
        pass 
    
    def do_shell(self, s):
        os.system(s)
        print()

    def default(self, line):
        ## when the grammar doesn't match, default to this
        if line.isdigit():
            self.goto = int(line)
        elif line.startswith("+"):
            self.goto = self.current_cell + int(line[1:])
        elif line.startswith("--"):
            self.goto = len(self.nb.cells) - int(line[2:])
        elif line.startswith("-"):
            self.goto = self.current_cell - int(line[1:])
        else: ## random python?
            results = self.execute_code(line)
            if results:
                print(results)
                print()
            self.goto = self.current_cell
        
    def format_cell(self, cell):
        source = [line[:self.max_col_width]
                  for line in
                  cell["source"].split("\n")[:self.max_rows]]
        if cell["cell_type"] == "code":
            prefix = ">>> "
        elif cell["cell_type"] == "markdown":
            prefix = "| "
        elif cell["cell_type"] == "raw":
            prefix = "} "
        return prefix + (("\n%s" % prefix).join(source))

    def show_cell(self, cell):
        print(self.format_cell(cell))
        print()
    
    # ----- commands -----
    def do_i(self, arg):
        """
        Insert a cell.
        """
        self.goto = self.current_cell

    def do_n(self, arg):
        self.goto = self.current_cell + 1

    def do_p(self, arg):
        self.goto = self.current_cell - 1

    def do_q(self, arg):
        self.client.stop_channels()
        self.manager.shutdown_kernel()
        print()
        print("To continue: nbplayer %s %s" % (self.filename, self.current_cell))
        return True
    
    do_EOF = do_q

    def do_help(self, arg):
        print(help_text)
        self.goto = self.current_cell

def main(filename, goto=0):
    nbp = TerminalNBPlayer(filename, goto)
    nbp.cmdloop()
