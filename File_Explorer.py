from tkinter import PhotoImage, Tk, Frame, PanedWindow, IntVar
from TitleBar.Title_Bar import TitleBar
from MenuBar.Menu_Bar import MenuBar
from EntryBar.Entry_Bar import EntryBar
from PaneWindow.Pane_Window import ScrollableFrame
from Functions import Functions_For_Explorer
from PopUpMenu.PopupMenu import filePopUp, framePopUp, quickPopUp
from getpass import getuser
import os

class Explorer (Functions_For_Explorer) :
    def __init__(self, root, bg= "#272822", fg= "#F8F8F6", font= ("Cambria", 15)) :
        self.root = root
        self.BG , self.FG = bg , fg
        self.FONT = font
        self.MAX_FOL_N , self.LIMIT = 4 , 16
        self.COMPOUND_IMGS = "top"
        self.COPYFILE_NAME, self.CUT_FILE_PATH = None, None
        self.SEARCH_FILE_PATHS , self.SEARCH_FILES = [] , []
        self.COPY_FILE_PATHS , self.COPY_FILES = [] , []
        self.MULTIPLE_SELECT = False
        self.IMAGE_SIZE = 44
        self.RENAME_ENTRY = False
        self.ICON_TYPE = 'normal'
        self.PADX , self.PADY = 5 , 0
        self.ANCHOR , self.AFTER_R = 'center', 'groove'
        self.DIR , self.EXTENSION_SHOW , self.EXTENSION_VAR = os.getcwd() , False , IntVar(self.root, value= 1)
        self.selected_index = 0
        self.fol_w , self.fol_h = 85 , 125

        self.root.configure(bg= self.BG)
        self.root.geometry("800x600+20+20")

        # Images
        self.FOLDER_IMG_32 = PhotoImage(file= "Images/imgs/23.png")
        self.FILE_IMG = PhotoImage(file= "Images/imgs/22.png")
        self.XLSX_IMG = PhotoImage(file= "Images/imgs/4.png")
        self.WORD_IMG = PhotoImage(file= "Images/imgs/12.png")
        self.PPTX_IMG = PhotoImage(file= "Images/imgs/8.png")
        self.DRIVE_IMG = PhotoImage(file= "Images/ThisPC/0.png")
        self.C_DRIVE_IMG = PhotoImage(file= "Images/ThisPC/1.png")

        # Drivers List
        self.DRIVES = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:']

        # Title Bar
        self.TITLEBAR = TitleBar(self.root, bg= "#0063B1", fg= self.FG)
        self.TITLEBAR.setTitle("File Explorer - By Tushar")
        self.TITLEBAR.MINIMIZE.bind("<ButtonRelease-1>", self.change_max_no)
        self.TITLEBAR.double_tap = self.mini_mize

        # Menu Bar
        self.HIDDEN = IntVar(value= 0)
        self.MENUBAR = MenuBar(self.root, bg= self.BG, fg= self.FG, depth= self.TITLEBAR.D, var= self.HIDDEN)

        # Entry Bar
        self.ENTRYBAR = EntryBar(self.root, bg= self.BG, fg= self.FG)
        self.MENUBAR.DIR = self.ENTRYBAR.DIR_ENTRY

        # Status Label
        self.STATUS_BAR = Frame(self.root, bg= self.BG, height= 25)
        self.STATUS_BAR.pack(side= 'bottom', fill= 'x')

        # Main Frame To PaneWindow
        self.PANEWIN = PanedWindow(self.root, bg= self.BG, orient= 'horizontal')
        self.PANEWIN.pack(fill= 'both', expand= True)

        self.QUICK_ACCESS = ScrollableFrame(self.PANEWIN, bg= self.BG,  fill_= "y", width_= 2)
        self.FOLDER_FRAME = ScrollableFrame(self.PANEWIN, bg= self.BG,  fill_= "both", expand_= 0)
        self.FOLDER_FRAME.SCROLL_BAR.focus_force()

        self.PANEWIN.add(self.QUICK_ACCESS.MAIN_FRAME)
        self.PANEWIN.add(self.FOLDER_FRAME.MAIN_FRAME)

        self.QUICK_ACCESS.animation()

        self.ENTRYBAR.DIR_ENTRY.bind("<Return>" , lambda e : self.refresh())
        self.ENTRYBAR.BACK_BTN.configure(state= 'normal')
        self.ENTRYBAR.FORD_BTN.configure(state= 'normal')
        self.ENTRYBAR.BACK_BTN.bind("<Button-1>",lambda e : self.back_func())
        self.ENTRYBAR.FORD_BTN.bind("<Button-1>",lambda e : self.forword_func())
        self.BACK_LIST , self.FORWD_LIST , self.FRAME_LIST = [] , [] , []

        self.rename_sel = False
        self.MENUBAR.RENAME_BTN.configure(state= "disabled")
        self.SELECTED_FRAME = Frame(self.root)
        self.ENTRYBAR.DIR_ENTRY.delete(0,'end')
        self.ENTRYBAR.DIR_ENTRY.insert('end' , f"C:\\Users\\{getuser()}\\Desktop")

        self.FILE_MENU = filePopUp(self.root)
        self.FRAME_MENU = framePopUp(self.root)
        self.QUICK_MENU = quickPopUp(self.root)
        self.FRAME_MENU.setPopUp(self.FOLDER_FRAME.FRAME)

        # PopUp Bindings
        self.FOLDER_FRAME.FRAME.bind("<Button-3>" , self.FRAME_MENU.popUp)
        self.FOLDER_FRAME.MAIN_FRAME.bind("<Button-3>" , self.FRAME_MENU.popUp)
        self.FOLDER_FRAME.CANVAS.bind("<Button-3>" , self.FRAME_MENU.popUp)

        # Start-Up Functions
        self.refresh()
        self.setFileMenu()
        self.quick_this_pc()

        # Commanding Buttons
        self.ENTRYBAR.REFRESH_BTN.configure(command= self.refresh)
        self.ENTRYBAR.UPWD_BTN.configure(command= self.up_arrow)
        
        # Commanding PopUp File Menus
        self.FILE_MENU.MENU.config(title= "File Menu")
        if os.path.exists("C:/Program Files/Microsoft VS Code") == 1 :
            self.FILE_MENU.MENU.entryconfig("Open With Code", command= self.open_with_code)
        if os.path.exists(f"C:/Program Files/Sublime Text 3/sublime_text.exe") :
           self.FILE_MENU.MENU.entryconfig("Open With Sublime Text", command= self.open_with_sublime)
        self.FILE_MENU.MENU.entryconfig("Open".ljust(45), command= self.open_file)
        self.FILE_MENU.MENU.entryconfig("Delete", command= self.delete_file_fol)
        self.FILE_MENU.MENU.entryconfig("Copy", command= self.copy_file)
        self.FILE_MENU.MENU.entryconfig("Cut", command= self.cut_file)
        self.FILE_MENU.MENU.entryconfig("Pin To Quick Access", command= self.add_to_quick_access)

        # Commanding PopUp Frame Menu
        if os.path.exists("code") :
            self.FRAME_MENU.MENU.entryconfig("Open With Code", command= self.open_with_code)
        self.FRAME_MENU.MENU.entryconfig("Refresh" , command= self.refresh)
        self.FRAME_MENU.MENU.entryconfig("Paste" , command= self.paste_file)
        self.FRAME_MENU.MENU.entryconfigure("View".ljust(45), command= self.show_files)
        self.FRAME_MENU.MENU.entryconfigure("Open Command Prompt Here", command= lambda : self.MENUBAR.cmd(8))

        # Commanding PopUp New Frame Menus
        self.FRAME_MENU.NEW.entryconfigure("New Folder".ljust(45), command= self.new_folder_1)
        self.FRAME_MENU.NEW.entryconfigure("New File", command= self.new_file)
        self.FRAME_MENU.NEW.entryconfigure("New Word File", command= self.new_word)
        self.FRAME_MENU.NEW.entryconfigure("New Excel File", command= self.new_xlsx)
        self.FRAME_MENU.NEW.entryconfigure("New PowerPoint File", command= self.new_pptx)

        # Commanding Quick Access Menu
        self.QUICK_MENU.MENU.entryconfig("Open", command= self.open_quick)
        self.QUICK_MENU.MENU.entryconfig("Open File Location", command= self.quick_location)
        self.QUICK_MENU.MENU.entryconfig("Unpin From Quick Access", command= self.unpin_quick)

        # Commanding MenuBar Buttons (Home Section)
        self.add_home_menu_func()
        self.MENUBAR.HOME.bind("<ButtonRelease-1>", lambda e: self.add_home_menu_func())

        # Commanding MenuBar Buttons (View Section)
        self.MENUBAR.VIEW.bind("<ButtonRelease-1>", lambda e: self.add_view_menu_func())

        self.ENTRYBAR.SEARCH_ENTRY.bind("<Button-1>", self.search_click)
        self.ENTRYBAR.SEARCH_ENTRY.bind("<ButtonRelease-1>", lambda e : self.ENTRYBAR.SEARCH_ENTRY.delete(0,'end'))
        self.ENTRYBAR.SEARCH_ENTRY.bind("<Return>", lambda E : self.search())
        self.ENTRYBAR.SEARCH_BTN.bind("<Button-1>", lambda E : self.search())
        self.root.bind("<Control-Button-1>", self.multiple_select)
        self.root.bind("<Control-Key-a>", self.multiple_all)
        self.FILE_MENU.open_with_code = self.open_with_code


if __name__ == "__main__" :
    win = Tk()
    Explorer(win)
    win.mainloop()