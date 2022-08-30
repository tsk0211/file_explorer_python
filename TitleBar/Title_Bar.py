from tkinter import Tk, Button, Label, Frame, PhotoImage, Menu
from win32api import GetSystemMetrics

class TitleBar :
    def __init__(self, root, bg= "#000", fg= "#F8F8F6", font= ["Cambria",10], bold= False, italic= False) :
        self.__ROOT = root

        self.BG , self.FG = bg , fg
        font_items = []
        self.x_val, self.y_val = 0 , 0
        self.minimized = True
        self.GEOMETRY = "800x650"
        self.MAX_W , self.MAX_H = GetSystemMetrics(0) , GetSystemMetrics(1)

        for item in font :
            font_items.append(item)

        if (bold == True and ("bold" not in font_items)) : font_items.append("bold")
        if (italic == True and ("italic" not in font_items)) : font_items.append("italic")

        self.FONT = font_items
        self.__ICON = None
        self.TITLE = "The Tkinter Window"
        self.__ROOT.title(self.TITLE)

        # Title Bar / Frame
        self.__TITLE_BAR = Frame(self.__ROOT, bg= self.BG)
        self.__TITLE_BAR.pack(fill= 'x', side= 'top')

        # Images
        self.__CLOSE_IMG = PhotoImage(file= "Images\\TitleBar\\close.png")
        self.__MIN1 = PhotoImage(file= "Images\\TitleBar\\min1.png")
        self.__MIN2 = PhotoImage(file= "Images\\TitleBar\\min2.png")
        self.__MINI = PhotoImage(file= "Images\\TitleBar\\delbtn.png")
        self.__ICON_IMG = PhotoImage(file= "Images\\TitleBar\\fileexp.png")

        # Title Frame Stuff
        self.ICON = Label(self.__TITLE_BAR,image= self.__ICON_IMG, bg= self.BG)
        self.__TITLE = Label(self.__TITLE_BAR, text= self.TITLE, bg= self.BG, fg= self.FG, font= self.FONT)
        self.__CLOSE = Button(self.__TITLE_BAR, image= self.__CLOSE_IMG, bg= self.BG, borderwidth= 0,
                            command= self.__ROOT.quit, activebackground= self.BG, height= 32, width= 42)
        self.MINIMIZE = Button(self.__TITLE_BAR, image= self.__MIN1, bg= self.BG, borderwidth= 0,
                            command= self.minimize_func, activebackground= self.BG, width= 42, height= 32)
        self.__HIDE = Button(self.__TITLE_BAR, image= self.__MINI, bg= self.BG, borderwidth= 0,
                            command= self.hide_win, activebackground= self.BG, width= 42, height= 32)

        self.ICON.pack(side= 'left', padx= 5)
        self.__TITLE.pack(side= 'left', pady= 7)
        self.__CLOSE.pack(side= 'right', padx= (6,0))
        self.MINIMIZE.pack(side= 'right', padx= 0)
        self.__HIDE.pack(side= 'right', padx= 0)

        self.D = self.__TITLE_BAR.winfo_depth()

        # Bindings Of Buttons And Title Frame
        self.__TITLE_BAR.bind("<Button-1>", self.get_x_y_titlebar)
        self.__TITLE_BAR.bind("<Double-ButtonRelease-1>", lambda e : self.double_tap())
        self.__TITLE.bind("<Button-1>", self.get_x_y_titlebar)
        self.__TITLE_BAR.bind("<B1-Motion>", self.move_title_bar)
        self.ICON.bind("<Button-1>", self.get_x_y_titlebar)
        self.ICON.bind("<B1-Motion>", self.move_title_bar)
        self.__TITLE.bind("<B1-Motion>", self.move_title_bar)
        self.__TITLE_BAR.bind("<Map>",lambda e : self.frame_mapped())

        # Hovering Animation
        self.__CLOSE.bind("<Enter>", lambda e : self.__CLOSE.configure(bg= "#263F53"))
        self.__CLOSE.bind("<Leave>", lambda e : self.__CLOSE.configure(bg= self.BG))
        self.MINIMIZE.bind("<Enter>", lambda e : self.MINIMIZE.configure(bg= "#263F53"))
        self.MINIMIZE.bind("<Leave>", lambda e : self.MINIMIZE.configure(bg= self.BG))
        self.__HIDE.bind("<Enter>", lambda e : self.__HIDE.configure(bg= "#263F53"))
        self.__HIDE.bind("<Leave>", lambda e : self.__HIDE.configure(bg= self.BG))


        # Pop Up Menu
        self.__MENU = Menu(self.__TITLE_BAR, bg= self.BG, fg= self.FG, activebackground= self.BG, tearoff= False,
                            cursor= 'hand2', title= "ICON MENU")
        
        self.__MENU.add_command(label= "Minimize", command= self.minimize_func, image= self.__MIN1, compound= 'left')
        self.__MENU.add_command(label= "Hide", command= self.hide_win, image= self.__MINI, compound= 'left')
        self.__MENU.add_command(label= "Close", command= self.__ROOT.quit, image= self.__CLOSE_IMG, compound= 'left')

        self.ICON.bind("<Button-3>" , self.popup_menu)


    def popup_menu(self,event) :
        self.__MENU.tk_popup(event.x_root , event.y_root)        

    def move_title_bar(self, event) :
        if self.minimized == False :
            self.minimize_func()
        self.__ROOT.geometry(f"+{event.x_root - self.x_val}+{event.y_root - self.y_val}")

    def get_x_y_titlebar(self, e) :
        self.x_val , self.y_val = e.x , e.y

    def minimize_func(self) :
        if self.minimized == True :
            self.__ROOT.geometry(f"{self.MAX_W}x{self.MAX_H}+0+2")
            self.MINIMIZE.configure(image= self.__MIN2)
            self.__MENU.entryconfig("Minimize", label= "Maximize", image= self.__MIN2)
            self.minimized = False

        elif self.minimized == False :
            self.__ROOT.geometry(f"{self.GEOMETRY}+100+100")
            self.MINIMIZE.configure(image= self.__MIN1)
            self.__MENU.entryconfig("Maximize", label= "Minimize", image= self.__MIN1)
            self.minimized = True

    def setIcon(self, icon_image) :
        self.__ICON = icon_image
        self.ICON.configure(image= self.__ICON)
    
    def setTitle(self, string) :
        self.__TITLE.config(text= string)

    def hide_win(self) :
        self.__ROOT.overrideredirect(False)
        self.__ROOT.state("iconic")
        self.__ROOT.update_idletasks()

    def frame_mapped(self) :
        self.__ROOT.overrideredirect(True)
        self.__ROOT.state('normal')

    def double_tap(self) :
        print("Taps")

    def setTitle(self, title) :
        self.__TITLE.configure(text= title)
        self.__ROOT.title(title)

if __name__ == "__main__" :
    win = Tk()
    win.geometry("600x500+100+100")
    win.overrideredirect(True)
    TitleBar(win)
    win.mainloop()