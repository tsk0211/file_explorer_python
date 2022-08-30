from tkinter import Tk, PanedWindow, Label, Frame, Scrollbar, Canvas, Button

class SideFrame :
    def __init__(self, root, bg= "#272822", fg= "#F8F8F6", font= ("Seoge UI", 10)) :
        self.__ROOT = root
        self.BG , self.FG , self.FONT = bg , fg , font
        
        self.PANEWINDOW = PanedWindow(self.__ROOT, bg= self.BG, orient= 'vertical')
        self.PANEWINDOW.pack(fill= 'both', expand= True)

        self.QUICK_ACCESS = ScrollableFrame(self.PANEWINDOW, bg= self.BG)
        self.PANEWINDOW.add(self.QUICK_ACCESS.MAIN_FRAME)

        self.FOLDER_TREE = ScrollableFrame(self.PANEWINDOW, bg= self.BG)
        self.PANEWINDOW.add(self.FOLDER_TREE.MAIN_FRAME)






class ScrollableFrame :
    def __init__(self, root, bg= "#272822", fg= "#F8F8F6", fill_= "both", expand_= 0, width_= 0) :
        self.__ROOT = root
        self.BG , self.FG = bg , fg
        self.__FILL = fill_
        self.__EXPAND = expand_

        # Main Frame
        self.MAIN_FRAME = Frame(self.__ROOT, bg= self.BG)
        self.MAIN_FRAME.pack(fill= self.__FILL, expand= self.__EXPAND)

        # Optional Width Parameter
        if width_ != 0:
            self.MAIN_FRAME.pack_configure(ipadx= width_)

        # Main Canvas & Scrollbar
        self.SCROLL_BAR = Scrollbar(self.MAIN_FRAME, bg= self.BG, width= 10, activebackground= self.BG,
                                highlightbackground= "red", activerelief= "raised", highlightcolor= "blue",
                                troughcolor= "green", relief= "groove", highlightthickness= 5)
        self.CANVAS = Canvas(self.MAIN_FRAME, bg= self.BG)
        self.FRAME = Frame(self.CANVAS, bg= self.BG)


        # Set Up Canvas & Scrollbar & Frame
        self.SCROLL_BAR.configure(command= self.CANVAS.yview)
        self.CANVAS.configure(yscrollcommand= self.SCROLL_BAR.set)

        self.CANVAS.bind("<Enter>", self._bound_MouseWheel)
        self.CANVAS.bind("<Leave>", self._unbound_MouseWheel)


        self.SCROLL_BAR.bind("<Configure>" , lambda e : self.CANVAS.configure(scrollregion= self.CANVAS.bbox('all')))
        self.CANVAS.create_window((0,0), window= self.FRAME, anchor= 'nw' )

        # Pack All On Screen
        self.SCROLL_BAR.pack(side= 'right', fill= 'y')
        self.CANVAS.pack(fill= 'both', expand= True)

        self.animation()

    # Scroll Bar Animation
    def animation(self):
        self.SCROLL_BAR.bind("<Enter>" , lambda e : self.SCROLL_BAR.configure(width= 15))
        self.SCROLL_BAR.bind("<Leave>" , lambda e : self.SCROLL_BAR.configure(width= 10))


    def setPosition(self, start= 0, end= 0):
        self.SCROLL_BAR.set(start,end)

    def _bound_MouseWheel(self, event) :
        self.CANVAS.bind_all("<MouseWheel>" , self._on_mousewheel)
    
    def _unbound_MouseWheel(self, event) :
        self.CANVAS.unbind_all("<MouseWheel>")
    
    def _on_mousewheel(self, event) :
        self.CANVAS.yview_scroll(int(-1 *(event.delta / 120)), "units")

if __name__ == "__main__" :
    win = Tk()
    win.geometry("700x600")

    sb = ScrollableFrame(win)

    for i in range(45) :
        Button(sb.FRAME, text= str(i*i).center(25), command= lambda : print(i)).pack()

    win.mainloop()