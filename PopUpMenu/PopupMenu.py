from tkinter import Menu, Tk, Frame, Label, PhotoImage
from os.path import isdir

class filePopUp :
    def __init__(self, window, bg= "#272822", fg= "#F8F8F6") :
        self.__ROOT = window
        self.BG , self.FG = bg , fg

        # Images
        self.COMMAND_IMG = PhotoImage(file= "Images\\PopUp\\command.png")
        self.COPY_IMG = PhotoImage(file= "Images\\PopUp\\copy.png")
        self.CUT_IMG = PhotoImage(file= "Images\\PopUp\\cut.png")
        self.DELETE_IMG = PhotoImage(file= "Images\\PopUp\\delete.png")
        self.FILEEX_IMG = PhotoImage(file= "Images\\PopUp\\fileexp.png")
        self.HTML_IMG = PhotoImage(file= "Images\\PopUp\\html.png")
        self.VSCODE_IMG = PhotoImage(file= "Images\\PopUp\\vscode.png")
        self.RENAME_IMG = PhotoImage(file= "Images\\PopUp\\rename.png")
        self.REFRSH_IMG = PhotoImage(file= "Images\\PopUp\\reload.png")
        self.SUB_IMG = PhotoImage(file= "Images\\PopUp\\sublime.png")


        self.MENU = Menu(self.__ROOT, bg= self.BG, fg= self.FG, tearoff= False)

        self.MENU.add_command(label= "Open".ljust(45), command= lambda : print("Open"), compound= 'left')
        self.MENU.add_command(label= "Open In New Window",image= self.FILEEX_IMG , command= lambda : print("Open In New Window"), compound= 'left')
        self.MENU.add_command(label= "Pin To Quick Access", command= lambda : print("Pin To Quick Access"), compound= 'left')
        self.MENU.add_separator()
        if isdir("C:\\Program Files\\Microsoft VS Code") :
            self.MENU.add_command(label= "Open With Code", image= self.VSCODE_IMG, command= self.open_with_code, compound= 'left')
        if isdir("C:\\Program Files\\Sublime Text 3") :
            self.MENU.add_command(label= "Open With Sublime Text", image= self.SUB_IMG, command= lambda : print("Open With Code"), compound= 'left')
        self.MENU.add_separator()
        self.MENU.add_command(label= "Cut", image= self.CUT_IMG, command= lambda : print("Cut"), compound= 'left')
        self.MENU.add_command(label= "Copy", image= self.COPY_IMG, command= lambda : print("Copy"), compound= 'left')
        self.MENU.add_separator()
        self.MENU.add_command(label= "Delete", image= self.DELETE_IMG, command= lambda : print("Delete"), compound= 'left')
        self.MENU.add_command(label= "Rename", image= self.RENAME_IMG, command= lambda : print("Rename"), compound= 'left')
        self.MENU.add_separator()
        self.MENU.add_command(label = "Properties" , command= lambda : print("Properties"), compound= 'left')

    def setPopUp(self, widget) :
        widget.bind("<Button-3>", self.popUp)

    def popUp(self, event) :
        self.MENU.tk_popup(event.x_root , event.y_root)
    
    def open_with_code(self) :
        print("Open With Code")

class framePopUp(filePopUp) :
    def __init__(self, window, bg= "#272822", fg= "#F8F8F6", font= ("Cambria", 10)) :
        self.__ROOT = window
        self.BG , self.FG = bg , fg
        self.FONT = font

        # Images
        self.REFRSH_IMG = PhotoImage(file= "Images\\PopUp\\reload.png")
        self.PASTE_IMG = PhotoImage(file= "Images\\PopUp\\paste.png")
        self.FOLDER_IMG = PhotoImage(file= "Images\\PopUp\\folder.png")
        self.XLSX_IMG = PhotoImage(file= "Images\\PopUp\\xlsx.png")
        self.WORD_IMG = PhotoImage(file= "Images\\PopUp\\word.png")
        self.PPTX_IMG = PhotoImage(file= "Images\\PopUp\\pptx.png")
        self.TERMI_IMG = PhotoImage(file= "Images\\PopUp\\term.png")
        self.VSCODE_IMG = PhotoImage(file= "Images\\PopUp\\vscode.png")

        self.MENU = Menu(self.__ROOT, bg= self.BG, fg= self.FG, tearoff= False)
        self.NEW = Menu(self.MENU, bg= self.BG, fg= self.FG, tearoff= False)

        self.MENU.add_command(label= "View".ljust(45), command= lambda : print("View"), compound= 'left')
        self.MENU.add_separator()
        self.MENU.add_command(label= "Refresh", image= self.REFRSH_IMG, command= lambda : print("Refresh"), compound= 'left')
        if isdir("C:\\Program Files\\Microsoft VS Code") :
            self.MENU.add_command(label= "Open With Code", image= self.VSCODE_IMG, command= lambda : print("Open With Code"), compound= 'left')
        self.MENU.add_command(label= "Open Command Prompt Here", image= self.TERMI_IMG, compound= 'left')
        self.MENU.add_command(label= "Paste", image= self.PASTE_IMG, compound= 'left', command= lambda : print("Paste"), state= 'disabled')
        self.MENU.add_separator()
        self.MENU.add_cascade(label= "New", menu= self.NEW, image= self.FOLDER_IMG, compound= "left")
        self.MENU.add_separator()
        self.MENU.add_command(label= "Properties", command= lambda : print("Properties"), compound= 'left')

        self.NEW.add_command(label= "New Folder".ljust(45), image= self.FOLDER_IMG, command= self.new_folder_func, compound= 'left')
        self.NEW.add_separator()
        self.NEW.add_command(label= "New File", command= lambda : print("New File"), compound= 'left')
        self.NEW.add_command(label= "New Excel File", image= self.XLSX_IMG, command= lambda : print("Xlsx File"), compound= 'left')
        self.NEW.add_command(label= "New Word File", image= self.WORD_IMG, command= lambda : print("Word File"), compound= 'left')
        self.NEW.add_command(label= "New PowerPoint File", image= self.PPTX_IMG, command= lambda : print("PPT File"), compound= 'left')
        self.NEW.add_command(label= "New Text Document" , command= lambda : print("Text"), compound= 'left')

    def new_folder_func(self) :
        print("New Folder")

class quickPopUp(filePopUp) :
    def __init__ (self, window, fg= "#F8F8F6", bg= "#272822") :
        self.ROOT = window
        self.BG , self.FG = bg , fg

        self.MENU = Menu(self.ROOT, bg= self.BG, fg= self.FG, tearoff= False)
        
        self.MENU.add_command(label= "Open", command= lambda : print("Open"))
        self.MENU.add_command(label= "Open File Location", command= lambda : print("Location"))
        self.MENU.add_command(label= "Unpin From Quick Access", command= lambda : print("Unpin"))


if __name__ == "__main__" :
    win = Tk()
    win.geometry("500x400")

    f = Frame(win, bg= "#272822")
    f.pack(fill= 'x')

    l = Label(f, text= "Hello")
    l.pack()

    fm = filePopUp(win)
    fm.setPopUp(l)

    frm = framePopUp(win)
    frm.setPopUp(f)
    
    win.mainloop()