#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sympy
import numpy
from matplotlib import pyplot

from IPython.display import display, HTML, Math, Markdown
from copy import deepcopy


# In[2]:


# pyplot default colors
dcolors = pyplot.rcParams['axes.prop_cycle'].by_key()['color']


# In[17]:


# markdown and html shortcut

def vspace(height=8):
    '''
    Create vertical space.
    '''
    display(HTML(f'<span style="display:block; height:{height}px;"></span>'))

def markdown(*args, sep='\n'):
    '''
    Display markdown
    '''
    
    parts = []
    
    for arg in args:
        
        # check if sympy
        if isinstance(arg, sympy.Basic):
            parts.append('$'+latex(arg, show=False)+'$')
        
        else:
            parts.append(str(arg))
    
    text = sep.join(parts)
    
    display(Markdown(text))

def html(content, show=True, tag='h2'):
    '''
    Displays HTML with tag.
    '''
    
    res = f'<{tag}>{content}</{tag}>'
    
    if show:
        display(HTML(res))
    else:
        return res


# function shortcuts
md = markdown


# In[4]:


def Plug(expr, elements):
    '''
    Quick replace sympy expression
    '''
    num = {e : numpy.random.rand() for i, e in enumerate(elements)}
    rev = {v : k for k, v in num.items()}
    
    return expr.subs(num).subs(rev)


# In[5]:


# print fonts

class Font:
    '''
    Print font container.
    '''
    
    # end font
    END = '\033[0m'
    
    # font colors
    GRAY = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT = '\033[37m'
    
    # highlights
    HGRAY = '\033[40m'
    HRED = '\033[41m'
    HGREEN = '\033[42m'
    HYELLOW = '\033[43m'
    HBLUE = '\033[44m'
    HMAGENTA = '\033[45m'
    HCYAN = '\033[46m'
    HLIGHT = '\033[47m'
    
    # font effects
    BOLD = '\033[1m' # bold
    UNDERLINE = '\033[4m' # underline
    FLIP = '\033[7m' # Highlight
        
    def showall():
        '''
        Show all available font colors
        '''
        for i in range(110):

            font = f'\033[{i}m'
            print(font+f"'\\033[{i}m'")

    def get(key):
        if key:
            if key in Font.__dict__.values():
                return key
            else:
                return Font.__dict__[key.upper()]
        else:
            return ''


# In[6]:


# quick bold underline formatting

def textbu(text, show=True, tag='b,u', color=''):
    '''
    Bold and underline markdown text, or change to other font types.
    '''
    beg, end = '', ''
    for t in tag.split(','):

        t = t.strip()

        beg += f'<{t}>'
        end = f'</{t}>' + end
    
    res = beg+str(text)+end
    
    i = res.index('>')
    
    res = res[:i] + f' style="color:{color}"' + res[i:]
    
    if show:
        markdown(res)
    else:
        return res

# print formatting
def printbu(text, show=True, u=True, color=''):
    '''
    Bold and underline text for markdown or print.
    '''

    # validate color
    c = Font.get(color)
    # add format beginning
    beg = c+Font.BOLD
    end = Font.END

    if u:
        beg += Font.UNDERLINE
    
    res = beg+str(text)+end
    
    # show / return
    if show:
        print(res)
    else:
        return res
    
# function shortcut
pbu = printbu
tbu = textbu


# In[7]:


# for jupyter lab rendering issues
#!pip install --upgrade sympy

class Latex:
    
    def __init__(self, *args, sep='=', simplify=False):
        '''
        Display math latex
        '''
        terms = []
        for arg in args:

            # if sympy object
            if isinstance(arg, (sympy.Basic, sympy.Matrix)):
                
                # convert to latex
                term = sympy.latex(sympy.simplify(arg) if simplify else arg)

            elif isinstance(arg, numpy.ndarray):
                term = Matrix(arg).str

            else:
                term = str(arg)

            terms.append(term)
        
        self.terms = terms
        
        # join text with separator
        self.str = f' {sep} '.join(self.terms)
        
        
    def __repr__(self):
        
        return self.str
    
    def _repr_html_(self):
        
        return r'$$\begin{align*} %s \end{align*}$$' % self.str
    
    def show(self, skip=0, skipp=1, end=r'\\'*2, center=True):
        
        # add leading spaces and ending (period)
        text = skip*r'\qquad ' + skipp*r'\quad ' + self.str + end
        
        text = r'$$\begin{align*} %s \end{align*}$$' % text
            
        if center:    
            display(HTML(text))
        else:
            display(Math(text))
        
    def __add__(self, other):
                
        res = deepcopy(self)
        res.str += str(other)
        
        return res
    
    def __radd__(self, other):
        
        res = deepcopy(self)
        res.str = str(other) + res.str
        
        return res
        
    def join(self, *args):
        
        res = deepcopy(self)
        
        res.str = res.str.join(' '+str(arg)+' ' for arg in args)
        
        return res
    
# shortcut
Lx = Latex


# In[8]:


# matrix latex

class Matrix(Latex):
    
    def __init__(self, arg, kind='bmatrix',
                 rsep='\n', csep=','
                ):
        '''
        Generate latex for matrices.
        '''
        # if type is numpy array, list, or tuple
        if isinstance(arg, numpy.ndarray):
            
            # index shape
            shape = arg.shape

            if len(shape) == 1:
                text = r'\\'.join([str(x) for x in arg])

            else:
                text = ''
                for row in arg:
                    text += ' & '.join([str(x) for x in row])
                    text += r'\\'
        else:
            text = str(arg)
            text = text.replace(rsep, r'\\')
            text = text.replace(csep, r'&')

            while text[0] == '\\':
                text = text[1:]

        # save matrix string
        self.mat_str = text
        
        # add latex matrix wrapper
        text = '\\begin{%s}%s\\end{%s}' % (kind, text, kind)
        
        super().__init__(text)
        
    def to_list(self):
        
        text = self.mat_str
        res = []
        
        for row in text.split(r'\\'):    
            
            v = []
            if row:
                for x in row.split('&'):

                    x = x.strip()
                    
                    if x.isnumeric():
                        if '.' in s:
                            v.append(float(x))
                        else:
                            v.append(int(x))    
                    else:
                        sx = sympy.Symbol(x)
                        v.append(sx)

                res.append(v)
            
        return res
    
    def to_numpy(self):
        
        return numpy.array(self.to_list())
    
    def to_sympy(self):
        
        return sympy.Matrix(self.to_list())
    
# shortcut
Mx = Matrix


# In[9]:



# plot vectors
def plot_vectors(origins, vectors, labels, figsize=(8, 6), margin=0.25):
    
    
    origins = numpy.array(origins)
    vectors = numpy.array(vectors)
    
    # init subplots
    fig, ax = pyplot.subplots(figsize=figsize)

    # legend handle
    handles = []

    # plot vectors
    for i, (og, v, label) in enumerate(zip(origins, vectors, labels)):

        q = ax.quiver(*og, *v, alpha=0.5,
                      color=dcolors[i], scale=1, 
                      width=0.0125, zorder=2,
                      angles='xy', scale_units='xy',
                      label=str(label))

        # add legend handle
        handles.append(q)

        ax.scatter(*og, s=100, alpha=0.75,
                   c=dcolors[i], zorder=1)

    # labels
    handles = handles[:3]
    labels = [x.get_label() for x in handles]

    
    X, Y = numpy.concatenate([origins, origins+vectors]).T
    
    ax.set_xlim(X.min()-margin, X.max()+margin)
    ax.set_ylim(Y.min()-margin, Y.max()+margin)

    ax.legend(handles, labels, fontsize=16, loc=4)

    return fig, ax, handles


# transpose list or tuple
def transpose(a):
    '''
    Transpose array (list or tuple).
    '''

    if not isinstance(a[0], (list, tuple)):
        a = [a]
        
    res = [[None for i in a] for j in a[0]]
    
    for i, row in enumerate(a):
        
        for j, x in enumerate(a[i]):    
            
            res[j][i] = a[i][j]
    
    return res


# In[10]:


# venn diagrams

venn_template = '''
```python
sets = {
    'A' : {'xy' : (-5,  2), 'size' : (9, 9), 'patch' : Ellipse, 'format' : {}},
    'B' : {'xy' : ( 5,  2), 'size' : (9, 9), 'patch' : Ellipse, 'format' : {}},
    'C' : {'xy' : ( 0, -2), 'size' : (9, 9), 'patch' : Ellipse, 'format' : {}},
}
pl
elements = {'a_1' : {'xy' : (-5 * 0.60, 2 * 0.00), 'format' : {}},
            'a_2' : {'xy' : (-5 * 1.50, 2 * 0.00), 'format' : {}},
            'a_3' : {'xy' : (-5 * 1.15, 2 * 1.50), 'format' : {}},
            'b_1' : {'xy' : ( 5 * 0.30, 2 * 0.00), 'format' : {}},
            'b_2' : {'xy' : ( 5 * 1.30, 2 * 0.00), 'format' : {}},
            'b_3' : {'xy' : ( 5 * 1.00, 2 * 1.50), 'format' : {}},
            'c_1' : {'xy' : ( 0, -2 * 2), 'format' : {}},
       }
```
'''

class VennDiagram:
    '''
    Class for drawing venn diagrams with matplotlib
    '''
    
    def __init__(self, sets_data=None, elements_data=None):
        
        '''
        Parameters
        ----
            sets_data : dict (default = None)
                 parameters for drawing sets
            
            elements_data : dict (default = None)
                 parameters for annotating elements
        '''
        
        if any(x==None for x in (sets_data, elements_data)):
            
            markdown('### Example Template')
            markdown('For sets and elements inputs:')
            
            markdown(venn_template)
            
        self.sets = sets_data
        self.elements = elements_data
        
        # formatting
        
        hatches = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
        self._hatches = [h*i for i in range(1, 3) for h in hatches]
        numpy.random.shuffle(self._hatches)
        
        self.subplots = None
        
        
    def __repr__(self):
        
        return "🟢 venn 🟠 dia 🟡 gram 🟣"
    
    
    def plot(self, figsize=(8, 5), subplots=None,
                 setformat=None, eformat=None, **kwargs
                ):
        
        if subplots==None:
            subplots = pyplot.subplots(figsize=figsize, **kwargs)
        
        # sets formatting
        dsetformat = dict(alpha=.15, fill=True, ec='black', lw=2)
        
        if setformat:
            dsetformat.update(setformat)
        
        # plot sets
        self._plot_sets(subplots, dsetformat)
        
        
        # elements formatting
        deformat = dict(alpha=0.6, fontsize=24, fontweight='heavy')
        
        if eformat:
            deformat.update(eformat)
            
        # plot elements
        self._plot_elements(subplots, deformat)
        
        
        # format figure
        self._format_figure(subplots, figsize)
        
        return subplots
    
    
    def _plot_sets(self, subplots, dformat):
        
        fig, ax = subplots
        sets = self.sets

        for i, (nm, S) in enumerate(sets.items()):
            
            xy = S['xy']
            size = S['size']
            
            if 'patch' in S:
                Patch = S['patch']
            else:
                Patch = Ellipse
            
            format_kwargs = dformat.copy()
            format_kwargs['hatch'] = self._hatches[i]
            format_kwargs['color'] = dcolors[i]
            
            # specifict format
            if 'format' in S:
                format_kwargs.update(S['format'])
            
            patch = Patch(xy, *size,
                          label=f'Set ${nm}$',
                          **format_kwargs,)
            
            ax.add_patch(patch)
            
            # replace patch
            self.sets[nm]['plot'] = patch
            
            
    def _plot_elements(self, subplots, dformat):
        
        fig, ax = subplots
        elements = self.elements
        
        for nm, e in elements.items():

            xy = e['xy']
            
            format_kwargs = dformat.copy()
            
            if 'format' in e:
                format_kwargs.update(e['format'])
            
            # add annotation
            self.elements[nm]['plot'] = ax.annotate(f'${nm}$', xy, **format_kwargs)
    
    
    def _format_figure(self, subplots, figsize):
        
        fig, ax = subplots
        
        y, x = figsize
        
        r = y / x
        if r >= 1:
            ax.set_xlim(-10*r, 10*r)
            ax.set_ylim(-10, 10)
        else:
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10*r, 10*r)
        
        # remove ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # remove spines
        for place in 'top, bottom, left, right'.split(', '):
            
            ax.spines[place].set_visible(False)

