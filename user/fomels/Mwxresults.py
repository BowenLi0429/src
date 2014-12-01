#!/usr/bin/env python
'Explore project results'

##   Copyright (C) 2010 University of Texas at Austin
##  
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 2 of the License, or
##   (at your option) any later version.
##  
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.
##  
##   You should have received a copy of the GNU General Public License
##   along with this program; if not, write to the Free Software
##   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import sys

try:
    import wx
except:
    sys.stderr.write('Please install wx!\n\n')
    sys.exit(1)
    
from signal import *
import os, commands

class TestFrame(wx.Frame):
    def __init__(self):
        cwd = os.getcwd()
        proj = os.path.join(
            os.path.basename(os.path.dirname(os.path.dirname(cwd))),
            os.path.basename(os.path.dirname(cwd)),
            os.path.basename(cwd))
        wx.Frame.__init__(self,None,-1,proj)
        self.pid = 0
        self.results = []
        self.flip = {}

        signal(SIGINT,self.handler)

    def handler(self,signum,frame):
        sys.stdout.write("\n%s: aborting...\n" % sys.argv[0])
        if self.pid:
            os.kill(self.pid,SIGINT)
        sys.exit(1)

    def showall(self):
        self.pid = os.fork()
        if not self.pid:
            for fig in results:
                os.system ("scons %s.view" % fig)
        sys.exit()

    def flipit(self):
        figs = map(lambda x: 'Fig/%s.vpl' % x,
                   filter(lambda y: self.flip[y].get(),results))
        if figs:
            self.pid = os.fork()
            if not self.pid:
                command = "sfpen %s" % ' '.join(figs)
                sys.stderr.write(command+'\n')
                os.system (command)
                sys.exit()

#quit = Button(frame,text="Quit",background="red",command=sys.exit)
#quit.pack(side=LEFT)

#fbut = Button(frame,text="Flip",background="green",command=flipit)
#fbut.pack(side=RIGHT)

#cycle = Button(frame,text="Cycle",background="yellow",command=showall)
#cycle.pack(side=RIGHT)

#results = commands.getoutput("scons -s results").split()
#c = results[-1:][0]
#if (c < 'A' or c > 'z'): 
#    results.pop() # remove scons junk
#length = max(map(len,results))

#def show(fig):
#    def showfig():
#        os.system("scons %s.view" % fig)
#    return showfig

#flip = {}
#r=0
#frame = Frame(root)
#for fig in results:
#    flip[fig] = IntVar()
#    Checkbutton(frame,variable=flip[fig]).grid(row=r,column=0)
#    Button(frame,text=fig,cursor='hand2',command=show(fig),width=length).grid(row=r,column=1)
#    r += 1
#frame.pack()

if __name__=='__main__':
    app = wx.App()
    frame = TestFrame()
    frame.Show()

    app.MainLoop()
