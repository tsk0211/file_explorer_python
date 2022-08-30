from tkinter import Tk, Button, Label, Frame, PhotoImage, Checkbutton, IntVar
from getpass import getuser
from PIL import ImageTk, Image
import os

class MenuBar :
    def __init__(self, root, bg= "#F8F8F6", fg= "#272822", font= ["Cambria",11], depth= 0, directory= f"C:\\Users\\{getuser()}\\Desktop", var= "") :
        self.__root = root
        self.BG , self.FG = bg , fg
        self.FONT = font
        self.__D = depth
        self.ARROW = u"\U000025BC"
        self.DIR = directory
        self.__MENU_FRAME = Button(root)
        
        self.__MENUBAR = Frame(self.__root, bg= "#272822")

        # Images
        self.__CLOSE_IMG = ImageTk.PhotoImage(Image.open("Images\\MenuBar\\close.png").resize((16,16)))
        self.__CMD_IMG = PhotoImage(file= "Images\\MenuBar\\cmd.png")
        self.POWER_SHELL_IMG = PhotoImage(file= "Images\\MenuBar\\termi.png")
        self.__COPY_IMG = PhotoImage(file= "Images\\MenuBar\\copy.png")
        self.__CUT_IMG = PhotoImage(file= "Images\\MenuBar\\cut.png")
        self.__PST_IMG = PhotoImage(file= "Images\\MenuBar\\paste.png")
        self.__DELETE_IMG = PhotoImage(file= "Images\\MenuBar\\trash.png")
        self.__RENAME_IMG = PhotoImage(file= "Images\\MenuBar\\rename.png")
        self.__FOLDER_IMG = PhotoImage(file= "Images\\MenuBar\\27.png")
        self.__NEW_FILE = PhotoImage(file= "Images\\MenuBar\\32.png")


        self.__BUTTON_FRAME = Frame(self.__MENUBAR, bg= self.BG)
        self.__FILES = Button(self.__BUTTON_FRAME, text= "Files", width= 9, name= "file", fg= "#F8F8F6",
                        bg= "#0063B1", activebackground= "#0063B8", relief= 'flat')
        self.HOME = Label(self.__BUTTON_FRAME, text= "Home", name= "home", bg= self.BG, fg= self.FG, width= 8)
        self.VIEW = Label(self.__BUTTON_FRAME, text= "View", name= "view", bg= self.BG, fg= self.FG, width= 8)


        self.MAIN_FRAME = Frame(self.__MENUBAR, bg= self.BG, bd= 2, borderwidth= 2, relief= 'groove')

        self.__FILES.bind("<Button-1>", self.popup_frame)
        self.HOME.bind("<Button-1>", self.view_in_frame)
        self.VIEW.bind("<Button-1>", self.view_in_frame)


        self.__MENUBAR.pack(side= "top", fill= 'x')
        self.__BUTTON_FRAME.pack(side= 'top', fill= 'x')
        self.__FILES.pack(side= 'left')
        self.HOME.pack(side='left')
        self.VIEW.pack(side= 'left')
        self.MAIN_FRAME.pack(fill= 'x', side= 'top')

        self.home_frame()


    def popup_frame(self, event) :
        self.__MENU_FRAME = Frame(self.__root, bg= "#F8F8F6", borderwidth= 1, highlightcolor= "red")
        self.__MENU_FRAME.place(x= 0, y= event.widget.winfo_depth() + self.__D)

        self.CMD_WIN = Label(self.__MENU_FRAME, image= self.__CMD_IMG, compound= 'left', text= "Command Prompt",
                            bg= self.BG, fg= self.FG, font= self.FONT, justify= 'left', anchor= 'w', padx= 10)
        self.POWER_SHELL = Label(self.__MENU_FRAME, image= self.POWER_SHELL_IMG, compound= 'left', text= "Power Shell",
                            bg= self.BG, fg= self.FG, font= self.FONT, justify= 'left', anchor= 'w', padx= 10)
        self.__CLOSE = Label(self.__MENU_FRAME, image= self.__CLOSE_IMG, compound= 'left', text= "Close",
                            bg= self.BG, fg= self.FG, font= self.FONT, justify= 'left', anchor= 'w', padx= 10)

        self.CMD_WIN.bind("<Button-1>", self.cmd)
        self.POWER_SHELL.bind("<Button-1>", self.powershell)
        self.__CLOSE.bind("<Button-1>", lambda e : self.__root.quit())

        self.CMD_WIN.pack(fill= 'x')
        self.POWER_SHELL.pack(fill= 'x')
        self.__CLOSE.pack(fill= 'x')

        self.__FILES.bind("<Button-1>" , lambda e :self.delete_popup())

    def delete_popup(self) :
        self.__MENU_FRAME.destroy()
        self.__FILES.bind("<Button-1>", self.popup_frame)

    def home_frame(self) :
        self.HOME.configure(relief= 'groove')
        self.VIEW.configure(relief= 'flat')
        for x in self.MAIN_FRAME.winfo_children() :
            x.pack_forget()
        
        # Frames
        self.__CUT_COPY_FRAME = Frame(self.MAIN_FRAME, bg= self.BG, borderwidth= 2, bd= 2, relief= 'groove')
        self.__DEL_REN_FRAME = Frame(self.MAIN_FRAME, bg= self.BG, borderwidth= 2, bd= 2, relief= 'groove')
        self.__NEW_FOL_FRAME = Frame(self.MAIN_FRAME, bg= self.BG, borderwidth= 2, bd= 2, relief= 'groove')
        self.__OPEN_FRAME = Frame(self.MAIN_FRAME, bg= self.BG, borderwidth= 2, bd= 2, relief= 'groove')
        self.__SELECT_FRAME = Frame(self.MAIN_FRAME, bg= self.BG, borderwidth= 2, bd= 2, relief= 'groove')

        self.__CUT_COPY_FRAME.pack(side= 'left', fill= 'y')
        self.__DEL_REN_FRAME.pack(side= 'left', fill= 'y')
        self.__NEW_FOL_FRAME.pack(side= 'left', fill= 'y')
        self.__OPEN_FRAME.pack(side= 'left', fill= 'y')
        self.__SELECT_FRAME.pack(side= 'left', fill= 'y')


        # Copy & Cut Frame
        self.COPY_BTN = Button(self.__CUT_COPY_FRAME, image=  self.__COPY_IMG, text= "Copy", relief= 'flat',
                                bg= self.BG, fg= self.FG,font= self.FONT, compound= 'top', state= 'disabled')
        self.CUT_BTN = Button(self.__CUT_COPY_FRAME, image= self.__CUT_IMG, text= "Cut", relief= 'flat',
                                bg= self.BG, fg= self.FG,font= self.FONT, compound= 'top', state= 'disabled')
        self.PST_BTN = Button(self.__CUT_COPY_FRAME, image= self.__PST_IMG, text= "Paste", relief= 'flat',
                                bg= self.BG, fg= self.FG,font= self.FONT, compound= 'top', state= 'disabled')
        self.__COPY_FRAME_LAB = Label(self.__CUT_COPY_FRAME, bg= self.BG, fg= self.FG, text= "Clip Board", font= ("Cambria",10))

        self.__COPY_FRAME_LAB.pack(side= 'bottom', fill= 'x')
        self.COPY_BTN.pack(side= 'left', fill= 'y', padx= (0,7))
        self.CUT_BTN.pack(side= 'left', fill= 'y', padx= 7)
        self.PST_BTN.pack(side= 'left', fill= 'y', padx= 7)


        # Delete & Rename Frame
        self.MOVE_TO_BTN = Button(self.__DEL_REN_FRAME, image= self.__DELETE_IMG, text= "Move", state= 'disabled',
                            bg= self.BG, relief= 'flat', fg= self.FG, compound= 'top', activebackground= self.BG) 
        self.DELETE_BTN = Button(self.__DEL_REN_FRAME, image= self.__DELETE_IMG, text= "Delete", state= 'disabled',
                            bg= self.BG, relief= 'flat', fg= self.FG, compound= 'top', activebackground= self.BG)
        self.RENAME_BTN = Button(self.__DEL_REN_FRAME, image= self.__RENAME_IMG, text= "Rename", state= 'disabled',
                            bg= self.BG, relief= 'flat', fg= self.FG, compound= 'top', activebackground= self.BG)
        self.__DEL_FRAME_LAB = Label(self.__DEL_REN_FRAME, bg= self.BG, fg= self.FG, text= "Organize", font= ("Cambria",10))

        self.__DEL_FRAME_LAB.pack(side= 'bottom', fill= 'x')
        self.MOVE_TO_BTN.pack(side= 'left', padx= (10,0), fill= 'y')
        self.DELETE_BTN.pack(side= 'left', padx= 7,fill= 'y')
        self.RENAME_BTN.pack(side= 'left', padx= 7,fill= 'y')


        # New Folder & File Section
        self.__NEW_FRAME_LAB = Label(self.__NEW_FOL_FRAME, bg= self.BG, fg= self.FG, text= "New", font= ("Cambria",10))
        self.NEW_FOL_BTN = Button(self.__NEW_FOL_FRAME, image= self.__FOLDER_IMG, text= "New Folder", state= 'disabled',
                            bg= self.BG, relief= 'flat', fg= self.FG, compound= 'top', activebackground= self.BG)
        self.NEW_FILE_BTN = Button(self.__NEW_FOL_FRAME, image= self.__NEW_FILE, text= "New Item ", state= 'disabled',
                            bg= self.BG, relief= 'flat', fg= self.FG, compound= 'left', activebackground= self.BG)

        self.NEW_FILE_BTN.bind("<Button-1>",self.new_file_func)

        self.__NEW_FRAME_LAB.pack(side= 'bottom', fill= 'x')
        self.NEW_FOL_BTN.pack(side= 'left', fill= 'y')
        self.NEW_FILE_BTN.pack(side= 'left', fill= 'y')

        # Open Frame
        self.__OPEN_LAB = Label(self.__OPEN_FRAME, bg= self.BG, fg= self.FG, text= "Open", font= ("Cambria",10))
        self.OPEN_BTN = Button(self.__OPEN_FRAME, image= self.__FOLDER_IMG, text= f"Open {self.ARROW}", state= 'disabled',
                            bg= self.BG, relief= 'flat', fg= self.FG, compound= 'top', activebackground= self.BG)
        self.PROP_BTN = Button(self.__OPEN_FRAME, image= self.__FOLDER_IMG, text= "Properties", state= 'disabled',
                            bg= self.BG, relief= 'flat', fg= self.FG, compound= 'top', activebackground= self.BG)

        self.__OPEN_LAB.pack(fill= 'x', side= "bottom")
        self.PROP_BTN.pack(side= 'left', fill= 'y')
        self.OPEN_BTN.pack(side= 'left', fill= 'y')

        # Select Frame
        self.__SELECT_LAB = Label(self.__SELECT_FRAME, bg= self.BG, fg= self.FG, text= "Select", font= ("Cambria",10))
        self.SELECT_ALL_BTN = Button(self.__SELECT_FRAME, text= "Select All", font= ("Cambria", 10),
                            bg= self.BG, relief= 'flat', fg= self.FG, activebackground= self.BG)
        self.SELECT_INVT_BTN = Button(self.__SELECT_FRAME, text= "Select Inverted", font= ("Cambria", 10),
                            bg= self.BG, relief= 'flat', fg= self.FG, activebackground= self.BG)


        self.__SELECT_LAB.pack(side= 'bottom', fill= 'x')
        self.SELECT_ALL_BTN.pack()
        self.SELECT_INVT_BTN.pack()

    def cmd(self, event) :
        os.chdir(self.DIR.get())
        os.startfile("cmd.exe")
        if self.__MENU_FRAME.winfo_exists() :
            self.__MENU_FRAME.place_forget()

    def view_frame(self) :
        for x in self.MAIN_FRAME.winfo_children() :
                x.pack_forget()
        self.HOME.configure(relief= 'flat')
        self.VIEW.configure(relief= 'groove')
        
        # Details Button
        self.DETAILS_BTN = Button(self.MAIN_FRAME, text= "Details Panal", bg= self.BG, fg= self.FG, relief= "groove")
        self.DETAILS_BTN.pack(side= 'left', fill= 'y')

        # Type Selection Frames
        self._TYPE_FRAME = Frame(self.MAIN_FRAME, relief= 'groove',bg= self.BG, bd= 5)
        self._TYPE_FRAME.pack(side='left', fill= 'y')

        self._TYPE1 = Frame(self._TYPE_FRAME, bg= self.BG)
        self._TYPE2 = Frame(self._TYPE_FRAME, bg= self.BG)
        self._TYPE3 = Frame(self._TYPE_FRAME, bg= self.BG)
        self.LAYOUT = Label(self._TYPE_FRAME, text= "Layout", fg= self.FG, bg= self.BG, relief= 'groove')

        self.EXTRA_BIG = Button(self._TYPE1, text= "Extra Large Icons", bg= self.BG, fg= self.FG, activebackground= self.BG, relief= 'flat')
        self.MEDIUM_BIG = Button(self._TYPE1, text= "Medium Icons", bg= self.BG, fg= self.FG, activebackground= self.BG, relief= 'raised')
        self.SMALL_BIG = Button(self._TYPE2, text= "Small Icons", bg= self.BG, fg= self.FG, activebackground= self.BG, relief= 'flat')
        self.LARGE_BIG = Button(self._TYPE2, text= "Large Icons", bg= self.BG, fg= self.FG, activebackground= self.BG, relief= 'flat')
        self.LIST_BIG = Button(self._TYPE3, text= "List Icons", bg= self.BG, fg= self.FG, activebackground= self.BG, relief= 'flat')
        self.TILES_BIG = Button(self._TYPE3, text= "Tiles Icons", bg= self.BG, fg= self.FG, activebackground= self.BG, relief= 'flat')

        self.EXTRA_BIG.pack(fill= 'x', padx= 5)
        self.MEDIUM_BIG.pack(fill= 'x', padx= 5)
        self.SMALL_BIG.pack(fill= 'x', padx= 5)
        self.LARGE_BIG.pack(fill= 'x', padx= 5)
        self.LIST_BIG.pack(fill= 'x', padx= 5)
        self.TILES_BIG.pack(fill= 'x', padx= 5)

        # Sort File Frame
        self.SORT_FRAME = Button(self.MAIN_FRAME, text= f"Sort By \n  {self.ARROW}", fg= self.FG, bg= self.BG, relief= 'groove')
        self.SORT_FRAME.pack(side= 'left', fill= 'y')

        # Show Files Frame
        self.SHOW_FILES = Frame(self.MAIN_FRAME, bg= self.BG, relief= 'groove', bd= 5)
        self.SHOW_FILES.pack(side= 'left', fill= 'y')
        self.SHOW_LAB = Label(self.SHOW_FILES, text= "Show/Hide", relief= "groove", bg= self.BG, fg= self.FG)

        self.HIDEN_FILE = IntVar()
        self.HIDEN_EXTN = IntVar()

        self.CHECK_BTN1 = Checkbutton(self.SHOW_FILES, bg= self.BG, fg= self.FG, selectcolor= self.BG, text= "Hidden Files",
            variable= self.HIDEN_FILE, onvalue= 1, offvalue= 0)
        self.CHECK_BTN2 = Checkbutton(self.SHOW_FILES, bg= self.BG, fg= self.FG, selectcolor= self.BG, text= "Show Extensions",
            variable= self.HIDEN_EXTN, onvalue= 1, offvalue= 0)

        self.SHOW_LAB.pack(side= 'bottom', fill= 'x')
        self.CHECK_BTN1.pack(expand= 1, fill= 'x')
        self.CHECK_BTN2.pack(expand= 1, fill= 'x')


        self.LAYOUT.pack(side= 'bottom', fill= 'x')
        self._TYPE1.pack(fill= 'y', side= 'left')
        self._TYPE2.pack(fill= 'y', side= 'right')
        self._TYPE3.pack(fill= 'y', side= 'right')

    def view_in_frame(self, event) :
        if event.widget.winfo_name() == 'home' :
            self.home_frame()
            self.home_functions()
        if event.widget.winfo_name() == 'view' :
            self.view_frame()
            self.view_functions()
        else :
            self.home_frame()
            self.home_functions()

    def home_functions(self) :
        pass

    def view_functions(self) :
        pass

    def powershell(self, event) :
        os.chdir(self.DIR.get())
        os.startfile("powershell.exe")
        if self.__MENU_FRAME.winfo_exists() :
            self.__MENU_FRAME.place_forget()

    def new_file_func(self, event) :
        pass

if __name__ == "__main__" :
    win = Tk()
    win.geometry("800x600")
    MenuBar(win, bg= "#272822", fg= "#F8F8F6")
    win.mainloop()