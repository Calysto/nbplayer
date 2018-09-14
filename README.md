# nbplayer

A console notebook player

Ths is a console/terminal program for running a Jupyter notebook.

You start it up by specifying a notebook file:

```bash
$ nbplayer conx-notebooks/MNIST.ipynb 
nbplayer 0.0.0: type `help` or `?` to see commands
```

The first cell of the notebook will show in the In[0] area, followed by the nbviewer prompt:

```shell
Viewing: conx-notebooks/MNIST.ipynb
--------------------------------------------------------

In [0]:

| # The MNIST Dataset
| 
| In this notebook, we will create a neural network to recognize handwritt
| 
| We will experiment with two different networks for this task. The first 
| 
| Let's begin by reading in the MNIST dataset and printing a short descrip

MNIST.ipynb [0/84] > 
```

If you press enter, then you will execute that cell (if it is code) and then go to the next cell.

```bash
In [1]:

>>> import conx as cx

MNIST.ipynb [1/84] > 
```

At the prompt, you can enter any of the following:

* empty line - execute current cell and advance
* n - goto next cell (skip this cell)
* p - goto previous cell
* NUMBER - goto cell #
* +AMOUNT - goto cell ahead, relative movement
* -AMOUNT - goto cell previous, relative movement
* --POSITION - from end
* ! shell command - execute command at the operating system (client side)
* q or ^d - quit nbplayer

Possible future options:

* re search forward/reverse for cell with next match
* run all code cells up to here
* i - insert cell
* d - delete cell
* u - undo operation in stack
* r - redo operation in stack
* code - show only code (toggles on/off)
