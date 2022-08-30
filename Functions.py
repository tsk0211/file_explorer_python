from tkinter import Label, Frame, Entry
from getpass import getuser
from send2trash import send2trash
from tkinter.messagebox import askyesno, showwarning
from xlsxwriter import Workbook
from threading import Thread
from PIL import Image, ImageTk
from shutil import copytree, copy, rmtree
import sqlite3
import os

class Functions_For_Explorer :
    def __init__(self) :
        pass

    def refresh(self, path= "") :
        if self.ENTRYBAR.DIR_ENTRY.get() == "C:\\Users\\Default Users" :
            return 0
        if not self.ENTRYBAR.SEARCH_ENTRY.get().startswith("Search In") :
            return 0

        if self.ENTRYBAR.DIR_ENTRY.get() in self.DRIVES :
            self.ENTRYBAR.DIR_ENTRY.insert('end', "\\")
        
        if path == "" :
            path__ = self.ENTRYBAR.DIR_ENTRY.get()
        else :
            path__ = path

        if path__ == "This PC" :
            self.FOLDER_NAME_LIST = self.DRIVES
            self.ENTRYBAR.SEARCH_ENTRY.delete(0, 'end')
            self.ENTRYBAR.SEARCH_ENTRY.insert('end', "Search In This PC")
            self.this_pc()
            return None

        if path__ == "" :
            path__ = os.getcwd()

        if path__.strip("\\")[-1] in ["cmd.exe",'cmd'] :
            os.chdir(self.ENTRYBAR.DIR_ENTRY.get())
            os.startfile("cmd.exe")
            return 0

        path__ = path__.lstrip("\\")
        l = os.listdir(path__)
        fols , files = [], []
        for FILE in l :
            if os.path.isdir(path__ + "\\" + FILE) :
                fols.append(FILE)
            else :
                files.append(FILE)
        
        self.FOLDER_NAME_LIST = fols + files

        # Buttons Re-Approved
        self.MENUBAR.RENAME_BTN.configure(state= "disabled")
        self.MENUBAR.MOVE_TO_BTN.configure(state= "disabled")
        self.MENUBAR.DELETE_BTN.configure(state= "disabled")
        self.MENUBAR.CUT_BTN.configure(state= "disabled")
        self.MENUBAR.COPY_BTN.configure(state= "disabled")
        self.MENUBAR.OPEN_BTN.configure(state= "disabled")

        if path__ not in self.BACK_LIST :
            self.BACK_LIST.append(path__)

        for X in self.FOLDER_FRAME.FRAME.winfo_children() :
            X.destroy()

        if (len(self.FOLDER_NAME_LIST) == 0) :
            Label(self.FOLDER_FRAME.FRAME, text= "Folder Is Empty")
            return 0
        
        self.r , self.c , self.fn = 0 , 0 , 0

        for X in self.FOLDER_NAME_LIST :
            lab = Frame(self.FOLDER_FRAME.FRAME, name= str(self.fn))
            lab.grid(row= self.r, column= self.c, padx= self.PADX, pady= self.PADY)

            self.IMAGE = self.get_image(X)
            self.IMAGE = self.IMAGE.resize((self.IMAGE_SIZE, self.IMAGE_SIZE))
        
            self.IMAGE = ImageTk.PhotoImage(self.IMAGE)

            if not self.EXTENSION_SHOW :
                if not os.path.isdir(self.ENTRYBAR.DIR_ENTRY.get() + "\\" + X):
                    txt = X.split(".")
                    txt.pop()
                    txt = ".".join(txt)
                else :
                    txt = X
            else :
                txt = X

            inlab = Label(lab, image= self.IMAGE, compound= self.COMPOUND_IMGS, text= txt[:self.LIMIT] ,
                        width= self.fol_w, height= self.fol_h, name= str(self.fn), bg= self.BG ,
                        fg= self.FG, padx= self.PADX, pady= 0, anchor= self.ANCHOR)
            inlab.image = self.IMAGE
            inlab.pack()

            inlab.bind("<Double-ButtonRelease-1>", self.double_click)
            lab.bind("<Double-ButtonRelease-1>", self.double_click)
            inlab.bind("<Button-1>", self.one_clicked)
            lab.bind("<Button-1>", self.one_clicked)
            
            self.FILE_MENU.setPopUp(lab)
            self.FILE_MENU.setPopUp(inlab)

            self.FRAME_LIST.append(lab)

            self.c += 1
            self.fn += 1
            if self.c == self.MAX_FOL_N :
                self.r += 1
                self.c = 0
        
        self.show_in_quick_access()

        h = Label(self.FOLDER_FRAME.FRAME,bg= self.BG, height= 20, width= 5)
        h.grid(row= self.r+1 , columnspan= self.MAX_FOL_N)
        h.bind("<Button-3>", lambda e : self.FRAME_MENU.MENU.tk_popup(e.x_root, e.y_root))

    def get_image(self, name, path= "") :
        os.chdir(self.DIR)

        if path == "" :
            pth = self.ENTRYBAR.DIR_ENTRY.get() + "\\" + name
        else :
            pth = path

        lis = name.split(".")
        ext = lis[-1]
        if os.path.isdir(pth) :
            img = Image.open("Images/imgs/27.png")

        elif ext in ['py', 'pyi', 'rpy', 'pyt'] :
            img = Image.open("Images/imgs/9.png")

        elif ext == 'ini' :
            img = Image.open("Images/imgs/33.png")

        elif ext in ['xls', 'xlsx', 'xlsm', 'xlam', 'xlsb', 'xml', 'xltx', 'xltm','xlm', 'xlt', 'xla'] :
            img = Image.open("Images/imgs/4.png")
        
        elif ext == 'asm' :
            img = Image.open("Images/imgs/34.png")
        
        elif ext == 'lnk' :
            img = Image.open("Images/imgs/35.png")

        elif ext == 'cgf' :
            img = Image.open("Images/imgs/36.png")

        elif ext == 'par' :
            img = Image.open("Images/imgs/37.png")

        elif ext in ['mp3', 'avi', 'AVI', 'mkv'] :
            img = Image.open("Images/imgs/vlc.png")
        
        elif ext == 'mp4' :
            img = Image.open("Images/imgs/6.png")

        elif ext == 'pdf' :
            img = Image.open("Images/imgs/28.png")

        elif ext in ['c','cpp','c++','cxx','cmm'] :
            img = Image.open("Images/imgs/0.png")

        elif ext in ['ppt', 'pptx', 'pptm', 'pot', 'potx', 'potm', 'ppsx', 'ppsm', 'pps', 'ppam', 'ppa'] :
            img = Image.open("Images/imgs/8.png")

        elif ext in ['docx','docm','dot','dotm','dotx'] :
            img = Image.open("Images/imgs/12.png")

        elif ext in ['cmd', 'bat', 'exe'] :
            img = Image.open("Images/imgs/3.png")

        elif ext in ['html','htm'] :
            img = Image.open("Images/imgs/2.png")

        elif ext in ['jpg','jpeg','png'] :
            img = Image.open(pth)
        
        elif ext == ['dll'] :
            img = Image.open("Images/imgs/32.png")

        elif ext == "txt" :
            img = Image.open("Images/imgs/21.png")
        
        elif ext in ['java','jav','json','js'] :
            img = Image.open("Images/imgs/26.png")

        elif ext in ['7z', 'rar', 'zip', 'zipx', 'rev', 'r001', 'r00'] :
            img = Image.open("Images/imgs/29.png")
        
        else :
            img = Image.open("Images/imgs/22.png")
        
        return img

    def double_click(self, event) :
        pth = self.ENTRYBAR.DIR_ENTRY.get()

        if pth.endswith("\\") :
            file_fol = pth + self.FOLDER_NAME_LIST[int(event.widget.winfo_name())]
        elif pth == "" :
            file_fol = self.FOLDER_NAME_LIST[int(event.widget.winfo_name())]
        else :
            file_fol = pth + "\\" + self.FOLDER_NAME_LIST[int(event.widget.winfo_name())]
        
        if os.path.isdir(file_fol) :
            try :
                self.ENTRYBAR.DIR_ENTRY.delete(0,'end')
                self.ENTRYBAR.DIR_ENTRY.insert(0, file_fol)

                self.ENTRYBAR.SEARCH_ENTRY.delete(0, 'end')
                self.ENTRYBAR.SEARCH_ENTRY.insert("end", f"Search In {self.SELECTED_FRAME['text']}")

                self.SELECTED_FRAME = Frame(self.root)

                # Disablling Buttons
                self.MENUBAR.RENAME_BTN.configure(state= "disabled")
                self.MENUBAR.MOVE_TO_BTN.configure(state= "disabled")
                self.MENUBAR.CUT_BTN.configure(state= "disabled")
                self.MENUBAR.COPY_BTN.configure(state= "disabled")
                self.MENUBAR.OPEN_BTN.configure(state= "disabled")
                self.MENUBAR.DELETE_BTN.configure(state= "disabled")

                if file_fol not in self.BACK_LIST :
                    self.BACK_LIST.append(file_fol)
                self.refresh()
            
            except :
                n = self.ENTRYBAR.DIR_ENTRY.get().split("\\")
                lw = n[-1]
                n.pop()
                n = "\\".join(n)

                showwarning("File Expolrer - By Tushar", f" The Folder {lw} Is Not\n   Accessable.")

                self.ENTRYBAR.DIR_ENTRY.delete(0, 'end')
                self.ENTRYBAR.DIR_ENTRY.insert('end', n)
                self.refresh()


        else :
            os.startfile(file_fol)

    def back_func(self) :
        if self.BACK_LIST[-1] not in self.FORWD_LIST :
            self.FORWD_LIST.append(self.BACK_LIST[-1])
        
        if len(self.BACK_LIST) >= 2 :
            fol = self.BACK_LIST[-2]
            self.BACK_LIST.pop()

            self.ENTRYBAR.DIR_ENTRY.delete(0, 'end')
            self.ENTRYBAR.DIR_ENTRY.insert('end', fol)

            self.refresh()

    def forword_func(self) :
        if len(self.FORWD_LIST) >= 1 :
            fol = self.FORWD_LIST[-1]
            self.FORWD_LIST.pop()

            self.ENTRYBAR.DIR_ENTRY.delete(0,'end')
            self.ENTRYBAR.DIR_ENTRY.insert('end', fol)

            self.refresh()

    def rename_func_2nd(self) :
        src = self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.FOLDER_NAME_LIST[self.selected_index]
        dst = self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.RENAME_ENTRY.get()

        os.rename(src= src, dst= dst)

        self.FOLDER_NAME_LIST.append(self.RENAME_ENTRY.get())
        self.FOLDER_NAME_LIST.remove(self.FOLDER_NAME_LIST[self.selected_index])

        self.RENAME_ENTRY.destroy()

        self.refresh()

    def rename_func_main(self, event= "") :
        if self.RENAME_ENTRY :
            return 0
        if event == "" :
            parent = self.SELECTED_FRAME
        else :
            parent = self.root.nametowidget(event.widget.winfo_name())
        
        self.selected_index = int(parent.winfo_name())

        txt = self.FOLDER_NAME_LIST[self.selected_index]

        img = self.get_image(self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())])
        img = img.resize((self.IMAGE_SIZE, self.IMAGE_SIZE))
        
        img = ImageTk.PhotoImage(img)

        ik = Label(parent, image= img, bg= self.BG)
        ik.image = img
        ik.pack()

        self.RENAME_ENTRY = Entry(parent, borderwidth= 1, bg= self.BG, fg= self.FG)
        self.RENAME_ENTRY.insert("end" , txt)
        self.RENAME_ENTRY.pack(side= 'bottom')

        self.RENAME_ENTRY.focus_force()

        self.RENAME_ENTRY.bind("<Return>" , lambda e : self.rename_func_2nd())

    def one_clicked(self, eve) :
        if self.MULTIPLE_SELECT :
            eve.widget.config(relief= "sunken")
            return

        if self.SELECTED_FRAME.winfo_name().isdigit() :
            self.SELECTED_FRAME.config(relief= 'flat')

        # Normallizing Buttons
        self.MENUBAR.RENAME_BTN.configure(state= "normal")
        self.MENUBAR.MOVE_TO_BTN.configure(state= "normal")
        self.MENUBAR.DELETE_BTN.configure(state= "normal")
        self.MENUBAR.CUT_BTN.configure(state= "normal")
        self.MENUBAR.COPY_BTN.configure(state= "normal")
        self.MENUBAR.OPEN_BTN.configure(state= "normal")
        
        if eve.widget.winfo_name().isdigit() :
            self.SELECTED_FRAME = eve.widget
            t = self.FOLDER_NAME_LIST[int(eve.widget.winfo_name())]

            txt = ""
            st , en = 0 , self.LIMIT
            i = int(len(t) / self.LIMIT)

            if not self.EXTENSION_SHOW :
                if not os.path.isdir(self.ENTRYBAR.DIR_ENTRY.get() + "\\" + t):
                    l = t.split(".")
                    l.pop()
                    t = ".".join(l)


            for j in range(i+1) :
                txt += "\n"
                txt += t[st : en]
                st += self.LIMIT
                en += self.LIMIT

            self.SELECTED_FRAME.configure(relief= self.AFTER_R)
            eve.widget.configure(text= txt)

    def open_with_code(self) :
        if self.SELECTED_FRAME.winfo_name().isdigit() :
            file = self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())]
        else :
            file = self.ENTRYBAR.DIR_ENTRY.get()

        os.system("code -n \"" + file + "\"")

    def setFileMenu(self) :
        self.FILE_MENU.MENU.entryconfig("Rename", command= self.rename_func_main)
        self.FILE_MENU.MENU.entryconfig("Delete", command= lambda : print("deleteFolderOrFile"))

    def quick_this_pc(self) :
        # Creating Labels Of Drives
        thpc = ImageTk.PhotoImage(Image.open("Images/imgs/30.png").resize((44,44)))
        thpc_l = Label(self.QUICK_ACCESS.FRAME, text= "This PC", textvariable= "This PC", image= thpc, bg= self.BG,
                        fg= self.FG, padx= 15, compound= 'left', font= self.FONT, anchor= "w")
        thpc_l.image = thpc
        thpc_l.pack(anchor= 'w', fill= 'x')

        i =ImageTk.PhotoImage(Image.open("Images/imgs/14.png").resize((44,44)))
        cd = Label(self.QUICK_ACCESS.FRAME, text= "C: Drive", textvariable= "C:\\", compound= 'left', image= i, bg= self.BG, fg= self.FG,
                    font= self.FONT, padx= 15, anchor= "w")
        
        dk = ImageTk.PhotoImage(Image.open("Images/imgs/11.png").resize((44,44)))
        desk = Label(self.QUICK_ACCESS.FRAME, text= "Desktop", textvariable= f"C:\\Users\\{getuser()}\\Desktop", compound= 'left', image= dk, bg= self.BG, fg= self.FG,
                    font= self.FONT, padx= 15, anchor= "w")
        
        d = ImageTk.PhotoImage(Image.open("Images/imgs/10.png").resize((44,44)))
        dd = Label(self.QUICK_ACCESS.FRAME, text= "D: Drive", textvariable= "D:\\", compound= 'left', image= d, bg= self.BG, fg= self.FG,
                    font= self.FONT, padx= 15, anchor= "w")
        ed = Label(self.QUICK_ACCESS.FRAME, text= "E: Drive", textvariable= "E:\\", compound= 'left', image= d, bg= self.BG, fg= self.FG,
                    font= self.FONT, padx= 15, anchor= "w")
        fd = Label(self.QUICK_ACCESS.FRAME, text= "F: Drive", textvariable= "F:\\", compound= 'left', image= d, bg= self.BG, fg= self.FG,
                    font= self.FONT, padx= 15, anchor= "w")
        gd = Label(self.QUICK_ACCESS.FRAME, text= "G: Drive", textvariable= "G:\\", compound= 'left', image= d, bg= self.BG, fg= self.FG,
                    font= self.FONT, padx= 15, anchor= "w")
        hd = Label(self.QUICK_ACCESS.FRAME, text= "H: Drive", textvariable= "H:\\", compound= 'left', image= d, bg= self.BG, fg= self.FG,
                    font= self.FONT, padx= 15, anchor= "w")
        ifd = Label(self.QUICK_ACCESS.FRAME, text= "H: Drive", textvariable= "I:\\", compound= 'left', image= d, bg= self.BG, fg= self.FG,
                    font= self.FONT, padx= 15, anchor= "w")
        jd = Label(self.QUICK_ACCESS.FRAME, text= "H: Drive", textvariable= "J:\\", compound= 'left', image= d, bg= self.BG, fg= self.FG,
                    font= self.FONT, padx= 15, anchor= "w")
        
        ami = ImageTk.PhotoImage(Image.open("Images/imgs/31.png").resize((44,44)))
        am = Label(self.QUICK_ACCESS.FRAME, text= f"{getuser()}", textvariable= f"C:\\Users\\{getuser()}", compound= 'left', image= ami, bg= self.BG, fg= self.FG,
                    font= self.FONT, padx= 15, anchor= "w")
        
        # Assigning Images To Labels
        cd.image = i
        desk.image = dk
        dd.image = d
        ed.image = d
        fd.image = d
        gd.image = d
        hd.image = d
        ifd.image = d
        jd.image = d
        am.image = ami

        # Binding For Opening
        cd.bind("<Button-1>", self.open_through_quick_access)
        desk.bind("<Button-1>", self.open_through_quick_access)
        dd.bind("<Button-1>", self.open_through_quick_access)
        ed.bind("<Button-1>", self.open_through_quick_access)
        fd.bind("<Button-1>", self.open_through_quick_access)
        gd.bind("<Button-1>", self.open_through_quick_access)
        hd.bind("<Button-1>", self.open_through_quick_access)
        ifd.bind("<Button-1>", self.open_through_quick_access)
        jd.bind("<Button-1>", self.open_through_quick_access)
        am.bind("<Button-1>", self.open_through_quick_access)
        thpc_l.bind("<Button-1>", self.open_through_quick_access)

        # Binding For Entering
        cd.bind("<Enter>", self.set_quick)
        desk.bind("<Enter>", self.set_quick)
        dd.bind("<Enter>", self.set_quick)
        ed.bind("<Enter>", self.set_quick)
        fd.bind("<Enter>", self.set_quick)
        gd.bind("<Enter>", self.set_quick)
        hd.bind("<Enter>", self.set_quick)
        ifd.bind("<Enter>", self.set_quick)
        jd.bind("<Enter>", self.set_quick)
        am.bind("<Enter>", self.set_quick)
        thpc_l.bind("<Enter>", self.set_quick)

        # Binding For Leaving
        cd.bind("<Leave>", self.not_quick)
        desk.bind("<Leave>", self.not_quick)
        dd.bind("<Leave>", self.not_quick)
        ed.bind("<Leave>", self.not_quick)
        fd.bind("<Leave>", self.not_quick)
        gd.bind("<Leave>", self.not_quick)
        hd.bind("<Leave>", self.not_quick)
        ifd.bind("<Leave>", self.not_quick)
        jd.bind("<Leave>", self.not_quick)
        am.bind("<Leave>", self.not_quick)
        thpc_l.bind("<Leave>", self.not_quick)

        # Packing On Quick Access Window
        cd.pack(anchor= 'w', pady= 8, fill= 'x')
        desk.pack(anchor= 'w', pady= 8, fill= 'x')
        am.pack(anchor= 'w', pady= 8, fill= 'x')
        if os.path.isdir("D:/") : dd.pack(anchor= 'w', pady= 6, fill= 'x')
        if os.path.isdir("E:/") : ed.pack(anchor= 'w', pady= 6, fill= 'x')
        if os.path.isdir("F:/") : fd.pack(anchor= 'w', pady= 6, fill= 'x')
        if os.path.isdir("G:/") : gd.pack(anchor= 'w', pady= 6, fill= 'x')
        if os.path.isdir("H:/") : hd.pack(anchor= 'w', pady= 6, fill= 'x')
        if os.path.isdir("I:/") : ifd.pack(anchor= 'w', pady= 6, fill= 'x')
        if os.path.isdir("J:/") : jd.pack(anchor= 'w', pady= 6, fill= 'x')

    def open_through_quick_access(self, event) :
        self.ENTRYBAR.DIR_ENTRY.delete(0,'end')
        self.ENTRYBAR.DIR_ENTRY.insert('end', event.widget['textvariable'])

        if os.path.isdir(str(event.widget['textvariable'])) :
            nam = event.widget['textvariable'].split("\\")
            self.ENTRYBAR.SEARCH_ENTRY.delete(0, 'end')
            if len(nam[-1]) > 1 :
                self.ENTRYBAR.SEARCH_ENTRY.insert('end', "Search In " + nam[-1])
            else :
                self.ENTRYBAR.SEARCH_ENTRY.insert('end', "Search In " + nam[0])

        self.MENUBAR.NEW_FOL_BTN.configure(state= 'normal')
        self.MENUBAR.NEW_FILE_BTN.configure(state= 'normal')
        
        self.refresh()

    def up_arrow(self) :
        n = self.ENTRYBAR.DIR_ENTRY.get()
        self.BACK_LIST.append(n)
        self.FORWD_LIST.append(n)

        if len(n) <= 3 :
            return 0
        
        ls = n.split("\\")     
        ls.pop()
        out = "\\".join(ls)

        self.ENTRYBAR.DIR_ENTRY.delete(0,'end')
        self.ENTRYBAR.DIR_ENTRY.insert('end',out)
        self.refresh()

    def open_file(self) :
        if self.SELECTED_FRAME.winfo_name().isdigit() :
            if os.path.isdir(self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())]) :
                naw = self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())]
                self.ENTRYBAR.DIR_ENTRY.delete(0, 'end')
                self.ENTRYBAR.DIR_ENTRY.insert('end', naw)
                self.refresh()
            else :
                os.startfile(self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())])

    def delete_file_fol(self) :
        if len(self.COPY_FILES) > 0 :
            sure = askyesno(title= "File Explorer By Tushar - Delete Command", message= f"Are you Sure To Delete {self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())]}")

            if sure :
                if self.MULTIPLE_SELECT :
                    for X in self.COPY_FILE_PATHS :
                        send2trash(X)
                    self.MULTIPLE_SELECT = False
                    self.COPY_FILE_PATHS , self.COPY_FILES = [] , []
                else :
                    send2trash(f"{self.ENTRYBAR.DIR_ENTRY.get()}\\{self.FOLDER_NAME_LIST[(self.SELECTED_FRAME.winfo_name())]}")
                self.SELECTED_FRAME = Frame(self.root, name= "non_digit")
                self.MULTIPLE_SELECT = False
        self.refresh()

    def new_folder_1(self) :
        self.fn += 1
        self.new_fold = Frame(self.FOLDER_FRAME.FRAME, bg= self.BG, width= self.fol_w, height= self.fol_h,
                    name= str(self.fn))
        img_lab = Label(self.new_fold, bg= self.BG, image= self.FOLDER_IMG_32)
        self.new_name = Entry(self.new_fold, bg= self.BG, fg= self.FG, width= 18)
        
        self.new_fold.grid(row= self.r, column= self.c, padx= 20, pady= 5)
        img_lab.pack()
        self.new_name.pack()

        self.new_name.bind("<Return>", self.create_folder)

    def create_folder(self, eve) :
        os.mkdir(self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.new_name.get())

        for c in self.new_fold.winfo_children() :
            c.destroy()
        self.new_fold.destroy()

        self.refresh()

    def change_max_no(self, eve= "") :
        if self.ICON_TYPE == 'normal' :
            if self.TITLEBAR.minimized :
                self.MAX_FOL_N = 8
            else :
                self.MAX_FOL_N = 4
        elif self.ICON_TYPE == "extral" :
            if self.TITLEBAR.minimized :
                self.MAX_FOL_N = 4
            else :
                self.MAX_FOL_N = 2
        elif self.ICON_TYPE == "large" :
            if self.TITLEBAR.minimized :
                self.MAX_FOL_N = 6
            else :
                self.MAX_FOL_N = 3
        elif self.ICON_TYPE == "list" or self.ICON_TYPE == "tiles" :
            if self.TITLEBAR.minimized :
                self.MAX_FOL_N = 1
            else :
                self.MAX_FOL_N = 1
        elif self.ICON_TYPE == "small" :
            self.PADX = 0
            if self.TITLEBAR.minimized :
                self.MAX_FOL_N = 8
            else :
                self.MAX_FOL_N = 5
        self.refresh()

    def open_in_new_window(self) :
        pass

    # Creating New File With Some Common Extensions
    def create_new_file (self, eve) :
        if self.new_name.get() in self.FOLDER_NAME_LIST :
            askyesno(title= "File Explorer By Tushar -Create File", message= f"{self.new_name.get()} Is Already Exists...")
            return 0
        
        l = self.new_name.get().split(".")
        if l[-1] in ['xls', 'xlsx', 'xlsm', 'xlam', 'xlsb', 'xml', 'xltx', 'xltm','xlm', 'xlt', 'xla'] :
            self.create_xlsx(0)
            return 0
        if l[-1] in ['ppt', 'pptx', 'pptm', 'pot', 'potx', 'potm', 'ppsx', 'ppsm', 'pps', 'ppam', 'ppa'] :
            self.create_pptx(0)
            return 0
        if l[-1] in ['docx','docm','dot','dotm','dotx'] :
            self.create_word(0)
            return 0

        file = open(self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.new_name.get(), "w")
        file.close()

        for c in self.new_fold.winfo_children() :
            c.destroy()

        self.refresh()

    def create_xlsx(self, event) :
        if self.new_name.get() in self.FOLDER_NAME_LIST :
            askyesno(title= "File Explorer By Tushar -Create Excel File", message= f"{self.new_name.get()} Is Already Exists...")
            return 0
        nam = self.new_name.get()
        el = nam.split(".")

        if el[-1] not in ['xls', 'xlsx', 'xlsm', 'xlam', 'xlsb', 'xml', 'xltx', 'xltm','xlm', 'xlt', 'xla'] :
            nam += ".xlsx"
        pth = self.ENTRYBAR.DIR_ENTRY.get() + "\\" + nam
        
        excl = Workbook(pth)
        excl.close()

        for X in self.new_fold.winfo_children() :
            X.destroy()
        self.refresh()

    def create_word(self, e) :
        if self.new_name.get() in self.FOLDER_NAME_LIST :
            askyesno(title= "File Explorer By Tushar -Create Word File", message= f"{self.new_name.get()} Is Already Exists...")
            return 0
        nam = self.new_name.get()
        el = nam.split(".")

        if ((el[-1] not in ['docx','docm','dot','dotm','dotx']) or ("." not in nam)) :
            nam += ".docx"
        
        f = open(self.ENTRYBAR.DIR_ENTRY.get() + '\\' + nam , "w+")
        f.close()

        for X in self.new_fold.winfo_children() :
            X.destroy()
        self.refresh()

    def create_pptx(self, e) :
        if self.new_name.get() in self.FOLDER_NAME_LIST :
            askyesno(title= "File Explorer By Tushar -Create File", message= f"{self.new_name.get()} Is Already Exists...")
            return 0
        nam = self.new_name.get()
        el = nam.split(".")

        if ("." not in nam) or (el[-1] not in ['ppt', 'pptx', 'pptm', 'pot', 'potx', 'potm', 'ppsx', 'ppsm', 'pps', 'ppam', 'ppa']) :
            nam += ".pptx"
        
        f = open(self.ENTRYBAR.DIR_ENTRY.get() + "\\" + nam, 'w+')
        f.close()

        for X in self.new_fold.winfo_children() :
            X.destroy()
        self.refresh()

    # Creating Files Input Method With Some Common Extensions
    def new_file(self) :
        self.fn += 1
        self.new_fold = Frame(self.FOLDER_FRAME.FRAME, bg= self.BG, width= self.fol_w, height= self.fol_h,
                    name= str(self.fn))
        self.img_lab = Label(self.new_fold, bg= self.BG, image= self.FILE_IMG)
        self.new_name = Entry(self.new_fold, bg= self.BG, fg= self.FG, width= 18)
        
        self.new_fold.grid(row= self.r, column= self.c, padx= 20, pady= 5)
        self.img_lab.pack()
        self.new_name.pack()

        self.new_name.bind("<Return>", self.create_new_file)

    def new_xlsx(self) :
        self.new_file()
        self.img_lab.configure(image= self.XLSX_IMG)
        self.new_name.bind("<Return>", self.create_xlsx)

    def new_word(self) :
        self.new_file()
        self.img_lab.configure(image= self.WORD_IMG)

        self.new_name.bind("<Return>", self.create_word)

    def new_pptx(self) :
        self.new_file()
        self.img_lab.configure(image= self.PPTX_IMG)

        self.new_name.bind("<Return>", self.create_pptx)

    # Copy, Cut, Paste Stuff
    def copy_file(self) :
        if self.MULTIPLE_SELECT :
            pass
        else :
            if self.SELECTED_FRAME.winfo_name().isdigit() :
                self.COPY_FILE_PATHS.append(self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())])
                self.COPY_FILES.append(self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())])

        self.FRAME_MENU.MENU.entryconfig("Paste", state= 'normal')
        self.COPY_OR_PASTE = "COPY"
        self.MENUBAR.PST_BTN.configure(state= 'normal')
        self.refresh()

    def cut_file(self) :
        self.FRAME_MENU.MENU.entryconfig("Paste", state= 'normal')
        self.MENUBAR.PST_BTN.configure(state= 'normal')
        self.COPY_OR_PASTE = "CUT"
        
        if self.MULTIPLE_SELECT :
            pass
        else :
            if self.SELECTED_FRAME.winfo_name().isdigit() :
                self.COPY_FILE_PATHS.append(self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())])
                self.COPY_FILES.append(self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())])
        self.refresh()

    def paste_file(self) :
        if len(self.COPY_FILE_PATHS) > 0 :
            for X in range(len(self.COPY_FILE_PATHS)) :
                print(self.FOLDER_NAME_LIST)
                print(self.COPY_FILES)
                print(self.COPY_FILE_PATHS)

                if self.COPY_FILES[X] in self.FOLDER_NAME_LIST :
                    self.PASTE_MESSAGE = askyesno(title= "Tushar's File Explorer By Tushar - Copy File",
                    message= f"{self.COPY_FILES[X]}\nIs Already Exists. Please Rename It.....")
                    return 0
                
                if self.COPY_OR_PASTE == 'COPY' :
                    if os.path.isdir(self.COPY_FILE_PATHS[X]) :
                        paste_path = self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.COPY_FILES[X]

                        copytree(src= self.COPY_FILE_PATHS[X], dst= paste_path)
                    else :
                        name_file = self.COPY_FILES[X]
                        if name_file in self.FOLDER_NAME_LIST :
                            askyesno("Tushar's File Explorer By Tushar - Copy File", f"{name_file} File \nAlready Exists.")
                            return 0
                        copy(self.COPY_FILE_PATHS[X], self.ENTRYBAR.DIR_ENTRY.get())
                
                if self.COPY_OR_PASTE == 'CUT' :
                    if os.path.isdir(self.COPY_FILE_PATHS[X]) :
                        copytree(src= (self.COPY_FILE_PATHS[X]), dst= (self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.COPY_FILES[X]))
                        rmtree(self.COPY_FILE_PATHS[X])
                    else :
                        copy(src= (self.COPY_FILE_PATHS[X]), dst= (self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.COPY_FILES[X]))
                        os.remove(self.COPY_FILE_PATHS[X])
                    self.FRAME_MENU.MENU.entryconfig("Paste", state= 'disabled')

            self.MENUBAR.PST_BTN.configure(state= 'disabled')

        self.refresh()
        self.MULTIPLE_SELECT = False
        self.COPY_FILE_PATHS , self.COPY_FILES = [] , []

    def show_files(self) :
        if len(self.FOLDER_FRAME.FRAME.winfo_children()) > 0 :
            for x in self.FOLDER_FRAME.FRAME.winfo_children() :
                x.destroy()
        else :
            self.refresh()

    # This PC
    def this_pc(self) :
        for X in self.FOLDER_FRAME.FRAME.winfo_children() :
            X.destroy()

        r , c , fn = 0 , 0 , 0

        self.MENUBAR.NEW_FOL_BTN.configure(state= 'disabled')
        self.MENUBAR.NEW_FILE_BTN.configure(state= 'disabled')

        for X in self.DRIVES :
            if ("C:\\" == X + "\\") :
                i = self.C_DRIVE_IMG
                lab = Label(self.FOLDER_FRAME.FRAME, image= i, compound= 'top', text= X, name= str(fn),
                            bg= self.BG, fg= self.FG, width= self.fol_w, height= self.fol_h, pady= 5, padx= 0)
                lab.image = i
                lab.grid(row= r, column= c, padx= 5, pady= 5)

                lab.bind("<Double-ButtonRelease-1>", self.select_this_pc)
                lab.bind("<Button-1>", self.one_clicked)

                fn += 1
                c += 1
                if c == self.MAX_FOL_N :
                    r += 1
                    c = 0
            elif os.path.isdir(X + "\\") :
                i = self.DRIVE_IMG
                lab = Label(self.FOLDER_FRAME.FRAME, image= i, compound= 'top', text= X, name= str(fn),
                            bg= self.BG, fg= self.FG, width= self.fol_w, height= self.fol_h, padx= 0, pady= 5)
                lab.image = i
                lab.grid(row= r, column= c, padx= 5, pady= 5)

                lab.bind("<Double-ButtonRelease-1>", self.select_this_pc)
                lab.bind("<Button-1>", self.one_clicked)

                fn += 1
                c += 1
                if c == self.MAX_FOL_N :
                    r += 1
                    c = 0

    def select_this_pc(self, event) :
        self.FOLDER_NAME_LIST = self.DRIVES

        self.ENTRYBAR.DIR_ENTRY.delete(0,'end')
        self.ENTRYBAR.DIR_ENTRY.insert(0,self.DRIVES[int(event.widget.winfo_name())] + "\\")

        self.refresh()

    def mini_mize(self) :
        self.TITLEBAR.minimize_func()

        if not self.ENTRYBAR.SEARCH_ENTRY.get().startswith("Search In") :
            return 0
        self.change_max_no()
        self.refresh()

    def __str__(self) :
        return """
        It Includes Every Function Need To Run Explorer Class.
            Without It, It's Only Imaginary View Of File Explorer.
            If You Wish To Run It, Without Explorer Class.
            You Will Need All Images And 
            :- Title Bar Class Object
            :- Menu Bar Class Object
            :- Entry Bar Class Object
            
            Images You Have To Search Or Give Instructions To name them
            otherwise they will show error.
        """

    def normal_icon(self) :
        self.IMAGE_SIZE = 44
        
        # Setting Variables To stun
        self.MENUBAR.MEDIUM_BIG.config(relief= 'raised')
        self.MENUBAR.EXTRA_BIG.config(relief= 'flat')
        self.MENUBAR.SMALL_BIG.config(relief= 'flat')
        self.MENUBAR.LARGE_BIG.config(relief= 'flat')
        self.MENUBAR.LIST_BIG.config(relief= 'flat')
        self.MENUBAR.TILES_BIG.config(relief= 'flat')

        self.ICON_TYPE = 'normal'
        self.COMPOUND_IMGS = "top"

        if self.TITLEBAR.minimized :
            self.MAX_FOL_N = 4
        else :
            self.MAX_FOL_N = 8
        self.PADX , self.LIMIT = 4 , 15
        self.fol_h , self.fol_w = 125 , 86
        self.ANCHOR = 'center'

        if self.ENTRYBAR.SEARCH_ENTRY.get().startswith("Search In") or self.ENTRYBAR.DIR_ENTRY.get() == "This PC" :
            self.refresh()

    def list_icon(self) :
        self.IMAGE_SIZE = 16
        
        # Setting Variables To stun
        self.MENUBAR.MEDIUM_BIG.config(relief= 'flat')
        self.MENUBAR.EXTRA_BIG.config(relief= 'flat')
        self.MENUBAR.SMALL_BIG.config(relief= 'flat')
        self.MENUBAR.LARGE_BIG.config(relief= 'flat')
        self.MENUBAR.LIST_BIG.config(relief= 'raised')
        self.MENUBAR.TILES_BIG.config(relief= 'flat')

        self.ICON_TYPE = 'list'
        self.COMPOUND_IMGS = "left"

        self.fol_h , self.fol_w = 20 , 200
        self.ANCHOR = 'w'

        if self.TITLEBAR.minimized :
            self.MAX_FOL_N = 1
        else :
            self.MAX_FOL_N = 1
        self.PADX , self.LIMIT = 4 , 100
        if self.ENTRYBAR.SEARCH_ENTRY.get().startswith("Search In") or self.ENTRYBAR.DIR_ENTRY.get() == "This PC":
            self.refresh()

    def tile_icon(self) :
        self.IMAGE_SIZE = 66
        
        # Setting Variables To stun
        self.MENUBAR.MEDIUM_BIG.config(relief= 'flat')
        self.MENUBAR.EXTRA_BIG.config(relief= 'flat')
        self.MENUBAR.SMALL_BIG.config(relief= 'flat')
        self.MENUBAR.LARGE_BIG.config(relief= 'flat')
        self.MENUBAR.LIST_BIG.config(relief= 'flat')
        self.MENUBAR.TILES_BIG.config(relief= 'raised')

        self.ICON_TYPE = 'list'
        self.COMPOUND_IMGS = "left"

        self.fol_h , self.fol_w = 60 , 300
        self.ANCHOR = 'w'

        if self.TITLEBAR.minimized :
            self.MAX_FOL_N = 1
        else :
            self.MAX_FOL_N = 1
        self.PADX , self.LIMIT = 15 , 100
        
        if self.ENTRYBAR.SEARCH_ENTRY.get().startswith("Search In") or self.ENTRYBAR.DIR_ENTRY.get() == "This PC":
            self.refresh()

    def small_icon(self) :
        self.IMAGE_SIZE = 32
        
        # Setting Variables To stun
        self.MENUBAR.MEDIUM_BIG.config(relief= 'flat')
        self.MENUBAR.EXTRA_BIG.config(relief= 'flat')
        self.MENUBAR.SMALL_BIG.config(relief= 'raised')
        self.MENUBAR.LARGE_BIG.config(relief= 'flat')
        self.MENUBAR.LIST_BIG.config(relief= 'flat')
        self.MENUBAR.TILES_BIG.config(relief= 'flat')

        self.ICON_TYPE = 'small'
        self.COMPOUND_IMGS = "top"

        if self.TITLEBAR.minimized :
            self.MAX_FOL_N = 4
        else :
            self.MAX_FOL_N = 8
        self.PADX , self.LIMIT = 4 , 15
        self.fol_h , self.fol_w = 125 , 86
        self.ANCHOR = 'center'
        if self.ENTRYBAR.SEARCH_ENTRY.get().startswith("Search In") or self.ENTRYBAR.DIR_ENTRY.get() == "This PC" :
            self.refresh()

    def large_icon(self) :
        self.IMAGE_SIZE = 72
        
        # Setting Variables To stun
        self.MENUBAR.MEDIUM_BIG.config(relief= 'flat')
        self.MENUBAR.EXTRA_BIG.config(relief= 'flat')
        self.MENUBAR.SMALL_BIG.config(relief= 'flat')
        self.MENUBAR.LARGE_BIG.config(relief= 'raised')
        self.MENUBAR.LIST_BIG.config(relief= 'flat')
        self.MENUBAR.TILES_BIG.config(relief= 'flat')
        
        self.ICON_TYPE = 'large'
        self.COMPOUND_IMGS = "top"

        if self.TITLEBAR.minimized :
            self.MAX_FOL_N = 3
        else :
            self.MAX_FOL_N = 6
        self.PADX , self.LIMIT = 7 , 15
        self.fol_h , self.fol_w = 125 , 86
        self.ANCHOR = 'center'
        if self.ENTRYBAR.SEARCH_ENTRY.get().startswith("Search In") or self.ENTRYBAR.DIR_ENTRY.get() == "This PC":
            self.refresh()

    def extra_large_icon(self) :
        self.IMAGE_SIZE = 88
        
        # Setting Variables To stun
        self.MENUBAR.MEDIUM_BIG.config(relief= 'flat')
        self.MENUBAR.EXTRA_BIG.config(relief= 'raised')
        self.MENUBAR.SMALL_BIG.config(relief= 'flat')
        self.MENUBAR.LARGE_BIG.config(relief= 'flat')
        self.MENUBAR.LIST_BIG.config(relief= 'flat')
        self.MENUBAR.TILES_BIG.config(relief= 'flat')
        
        self.ICON_TYPE = 'extral'
        self.COMPOUND_IMGS = "top"

        if self.TITLEBAR.minimized :
            self.MAX_FOL_N = 2
        else :
            self.MAX_FOL_N = 4
        self.PADX , self.LIMIT = 25 , 15
        self.fol_h , self.fol_w = 125 , 86
        self.ANCHOR = 'center'
        if self.ENTRYBAR.SEARCH_ENTRY.get().startswith("Search In") or self.ENTRYBAR.DIR_ENTRY.get() == "This PC" :
            self.refresh()

    def add_home_menu_func(self) :
        self.MENUBAR.NEW_FOL_BTN.config(command= self.new_folder_1, state= 'normal')
        self.MENUBAR.NEW_FILE_BTN.config(command= self.new_file, state= 'normal')
        self.MENUBAR.COPY_BTN.config(command= self.copy_file)
        self.MENUBAR.OPEN_BTN.config(command= self.open_file)
        self.MENUBAR.CUT_BTN.config(command= self.cut_file)
        self.MENUBAR.PST_BTN.config(command= self.paste_file)
        self.MENUBAR.MOVE_TO_BTN.config(command= self.cut_file)
        self.MENUBAR.RENAME_BTN.configure(command= self.rename_func_main)
        self.MENUBAR.DELETE_BTN.configure(command= self.delete_file_fol)

    def add_view_menu_func(self) :
        self.MENUBAR.LARGE_BIG.config(command= self.large_icon)
        self.MENUBAR.MEDIUM_BIG.config(command= self.normal_icon)
        self.MENUBAR.EXTRA_BIG.config(command= self.extra_large_icon)
        self.MENUBAR.SMALL_BIG.config(command= self.small_icon)
        self.MENUBAR.LIST_BIG.config(command= self.list_icon)
        self.MENUBAR.TILES_BIG.config(command= self.tile_icon)
        self.MENUBAR.CHECK_BTN2.bind("<Button-1>", self.extensions_func)
        self.EXTENSION_VAR = 1

    def quick_data(self) :
        db = sqlite3.connect("Databases\\quick_acc.db")
        cr = db.cursor()

        cr.execute("""SELECT *,oid FROM quick""")
        fol_lis = cr.fetchall()

        db.commit()
        db.close()

        return fol_lis

    def search_click(self, eve) :
        path__ = self.ENTRYBAR.DIR_ENTRY.get() 
        if path__ not in ["This PC", "C:\\"] :
            def ser():
                self.SEARCH_FILES , self.SEARCH_FILE_PATHS = [] , []
                files = os.walk(self.ENTRYBAR.DIR_ENTRY.get())
                
                for X, Y, Z in files :
                    #Search For Sub-Folders
                    for SF in Y :
                        if len(SF) > 0 :
                            self.SEARCH_FILE_PATHS.append(X)
                            self.SEARCH_FILES.append(SF)
                    #Search For Files
                    for FL in Z :
                        self.SEARCH_FILES.append(FL)
                        self.SEARCH_FILE_PATHS.append(X)
                
                print(self.SEARCH_FILES)
                print(self.SEARCH_FILE_PATHS)
            Thread(target= ser).start()

    def search(self) :
        NAME = self.ENTRYBAR.SEARCH_ENTRY.get()
        print(NAME)
        r = 0
        for X in self.FOLDER_FRAME.FRAME.winfo_children() :
            X.destroy()
        
        if len(NAME) == 0 :
            self.refresh()
            return 0
        f = 0
        for X in self.SEARCH_FILES :
            if NAME in X :
                img = self.get_image(X,self.SEARCH_FILE_PATHS[self.SEARCH_FILES.index(X)] + "/" + X)
                img = img.resize((self.IMAGE_SIZE, self.IMAGE_SIZE))
                img = ImageTk.PhotoImage(img)
                
                lab = Label(self.FOLDER_FRAME.FRAME, text= (X + "\n\t\t" +self.SEARCH_FILE_PATHS[self.SEARCH_FILES.index(X)])
                            , image= img, compound= 'left', relief= 'groove', width= 800, name= str(f),
                            bg= self.BG, fg= self.FG, height= 50, padx= 40, pady= 10, anchor= 'w')
                lab.image = img
                lab.bind("<Double-Button-1>", self.double_click_search)
                lab.grid(row= r, sticky= 'w', rowspan= 1)
                r += 1
            f += 1

        if f == 0 :
            txt = f"No Files OR Folders Named {NAME} ."
        else :
            txt = ""
        Label(self.FOLDER_FRAME.FRAME, text= txt, bg= self.BG, fg= self.FG, height= 25, width= 500).grid(row= r)

    def double_click_search(self, event) :
        self.ENTRYBAR.DIR_ENTRY.delete(0, 'end')
        file_path = self.SEARCH_FILE_PATHS[int(event.widget.winfo_name())] + "\\" + self.SEARCH_FILES[int(event.widget.winfo_name())]
        
        if os.path.isdir(file_path) :
            self.ENTRYBAR.DIR_ENTRY.insert('end', file_path )
            self.refresh()
        else :
            os.startfile(file_path)

    def extensions_func(self, event) :
        if self.EXTENSION_SHOW == True :
            self.EXTENSION_SHOW = False
            self.EXTENSION_VAR = 1
        else :
            self.EXTENSION_SHOW = True
            self.EXTENSION_VAR = 0
        self.refresh()

    def open_with_sublime(self) :
        if self.SELECTED_FRAME.winfo_name().isdigit() :
            file = self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.FOLDER_NAME_LIST[int(self.SELECTED_FRAME.winfo_name())]
        else :
            file = self.ENTRYBAR.DIR_ENTRY.get()
        cur_dir = self.ENTRYBAR.DIR_ENTRY.get()
        
        os.chdir("C:\\Program Files\\Sublime Text 3")
        os.system('sublime_text \"' + file + '\"' )
        os.chdir(cur_dir)
    
    # Quick Access
    def add_to_quick_access(self) :
        if self.SELECTED_FRAME.winfo_name().isdigit() :
            ind = int(self.SELECTED_FRAME.winfo_name())
            name = self.FOLDER_NAME_LIST[ind]
        else :
            lis = self.ENTRYBAR.DIR_ENTRY.get().split("\\")
            name = lis[-1]
        loc = self.ENTRYBAR.DIR_ENTRY.get()

        if loc.endswith("\\") :
            path = loc + name
        else :
            path = loc + "\\" + name
        
        DB = sqlite3.connect("Databases/Quick_Access.db")
        CR = DB.cursor()

        CR.execute("""CREATE TABLE IF NOT EXISTS items (
                file_n TEXT,
                file_p TEXT,
                file_l TEXT
            )""")
        
        CR.execute("""INSERT INTO items VALUES (:file_n, :file_p, :file_l)""",
        {
            'file_n' : name,
            'file_p' : path,
            'file_l' : loc
        })

        DB.commit()
        DB.close()
        self.show_in_quick_access()
        print("ADDED.")
    
    def show_in_quick_access(self) :
        self.QUICK_ID , self.Q_LIST , self.Q_LOC = [], [], []
        DB = sqlite3.connect("Databases/Quick_Access.db")
        CR = DB.cursor()

        CR.execute("""CREATE TABLE IF NOT EXISTS items (
                file_n TEXT,
                file_p TEXT,
                file_l TEXT
            )""")

        CR.execute("SELECT *,oid FROM items")
        ITEMS = CR.fetchall()

        for X in self.QUICK_ACCESS.FRAME.winfo_children() :
            X.destroy()
        
        self.quick_this_pc()
        q_id = 0

        for I in ITEMS :
            nam, pat, loc = I[0], I[1], I[2]
            self.QUICK_ID.append(I[3])
            self.Q_LIST.append(pat)
            self.Q_LOC.append(loc)

            if not os.path.exists(pat) :
                continue

            MAGE = self.get_image(nam, pat)
            MAGE = MAGE.resize((44, 44))
        
            img = ImageTk.PhotoImage(MAGE)

            l = Label(self.QUICK_ACCESS.FRAME, text= nam, image= img, compound= 'left', font= ("Cambria", 13, 'bold'),
                    bg= self.BG, fg= self.FG, name= str(q_id), justify= 'left', anchor= 'w')
            l.image = img
            l.pack(padx= 20, fill= 'x')

            l.bind("<Double-Button-1>", self.open_quick)
            l.bind("<Enter>", self.set_quick)
            l.bind("<Leave>", self.not_quick)
            self.QUICK_MENU.setPopUp(l)


            q_id = q_id + 1

        Label(self.QUICK_ACCESS.FRAME, height= 35, bg= self.BG).pack()
        DB.commit()
        DB.close()

    def set_quick(self, e) :
        e.widget.config(relief= "groove")
        if e.widget.winfo_name().isdigit() :
            self.QUICK_SELECT = int(e.widget.winfo_name())

    def not_quick(self, e) :
        e.widget.config(relief= 'flat')

    def open_quick(self, e= "") :
        if e == "" :
            p = int(self.QUICK_SELECT)
        else :
            p = int(e.widget.winfo_name())
        file = self.Q_LIST[p]
        
        if os.path.isdir(file) :
            self.ENTRYBAR.DIR_ENTRY.delete(0, 'end')
            self.ENTRYBAR.DIR_ENTRY.insert('end', file)
            self.refresh()
        else :
            os.startfile(file)

    def unpin_quick(self) :
        DB = sqlite3.connect("Databases/Quick_Access.db")
        CR = DB.cursor()

        val = self.QUICK_ID[self.QUICK_SELECT]
        CR.execute("""DELETE FROM items WHERE oid=""" + str(val))

        DB.commit()
        DB.close()
        self.refresh()

    def quick_location(self) :
        loc = self.Q_LOC[self.QUICK_SELECT]
        self.ENTRYBAR.DIR_ENTRY.delete(0, 'end')
        self.ENTRYBAR.DIR_ENTRY.insert('end', loc)
        self.refresh()

    # Multiple Selecting Items
    def multiple_select(self, event) :
        self.one_clicked(event)
        self.COPY_FILE_PATHS.append(self.ENTRYBAR.DIR_ENTRY.get() + "\\" + self.FOLDER_NAME_LIST[int(event.widget.winfo_name())])
        self.COPY_FILES.append(self.FOLDER_NAME_LIST[int(event.widget.winfo_name())])
        
        print(self.COPY_FILE_PATHS)
        print(self.COPY_FILES)
        self.MULTIPLE_SELECT = True

        # Normallizing Buttons
        self.MENUBAR.RENAME_BTN.configure(state= "normal")
        self.MENUBAR.MOVE_TO_BTN.configure(state= "normal")
        self.MENUBAR.DELETE_BTN.configure(state= "normal")
        self.MENUBAR.CUT_BTN.configure(state= "normal")
        self.MENUBAR.COPY_BTN.configure(state= "normal")
        self.MENUBAR.OPEN_BTN.configure(state= "normal")

    def multiple_all(self, event) :
        dst = self.ENTRYBAR.DIR_ENTRY.get() + "\\"
        for FILE in self.FOLDER_NAME_LIST :
            self.COPY_FILE_PATHS.append(dst + FILE)
            self.COPY_FILES.append(FILE)
        for X in self.FOLDER_FRAME.FRAME.winfo_children() :
            for f in X.winfo_children():
                if f.winfo_name().isdigit() :
                    X.winfo_children()[0].configure(relief= 'sunken')
        
        # Normallizing Buttons
        self.MENUBAR.RENAME_BTN.configure(state= "normal")
        self.MENUBAR.MOVE_TO_BTN.configure(state= "normal")
        self.MENUBAR.DELETE_BTN.configure(state= "normal")
        self.MENUBAR.CUT_BTN.configure(state= "normal")
        self.MENUBAR.COPY_BTN.configure(state= "normal")
        self.MENUBAR.OPEN_BTN.configure(state= "normal")
    

