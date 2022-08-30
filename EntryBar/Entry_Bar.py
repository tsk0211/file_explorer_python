from tkinter import Frame, PhotoImage, Button, Entry, Tk

class EntryBar :
    def __init__(self, root, font= ("Seoge UI",15,'bold'), bg= "#272822", fg= "#F8F8F6") :
        '''
            Class EntryBar

                    This class is for Tk, Tcl
                Entry Bar for File Explorer
                Window. This Will Give Allowance
                to get the functions threw
                
                : DIR_ENTRY <-:-> Entry Feild For Directory Address.\n
                : SEARCH_ENTRY <-:-> Search Function Entry Feild.
        '''
        self.__ROOT = root
        self.FONT , self.BG , self.FG = font , bg , fg

        # Images
        self.__BACK_IMG = PhotoImage(file= ("Images\\EntryBar\\left-arrow.png"))
        self.__FORD_IMG = PhotoImage(file= ("Images\\EntryBar\\next.png"))
        self.__UPWD_IMG = PhotoImage(file= ("Images\\EntryBar\\up-arrow.png"))
        self.__SEARCH_IMG = PhotoImage(file= ("Images\\EntryBar\\search.png"))
        self.__RELOAD_IMG = PhotoImage(file= ("Images\\EntryBar\\reload.png"))

        # Main Frame
        self.MAIN_FRAME = Frame(self.__ROOT, bg= self.BG, relief= 'groove', bd= 1, borderwidth= 1)
        self.MAIN_FRAME.pack(fill= 'x', side= 'top', pady= 5)


        # Buttons Frame
        self.__BUT_FRM = Frame(self.MAIN_FRAME, bg= self.BG, relief= 'flat')
        self.__BUT_FRM.pack(side= 'left', fill= 'x')

        # Buttons
        self.BACK_BTN = Button(self.__BUT_FRM, image= self.__BACK_IMG, bg= self.BG, width= 20, relief= 'flat', state= 'disabled', activebackground= self.BG)
        self.FORD_BTN = Button(self.__BUT_FRM, image= self.__FORD_IMG, bg= self.BG, width= 20, relief= 'flat', state= 'disabled', activebackground= self.BG)
        self.UPWD_BTN = Button(self.__BUT_FRM, image= self.__UPWD_IMG, bg= self.BG, width= 20, relief= 'flat', activebackground= self.BG)
        
        self.BACK_BTN.pack(side= 'left', padx= 3)
        self.FORD_BTN.pack(side= 'left', padx= 3)
        self.UPWD_BTN.pack(side= 'left', padx= 3)


        # Entry For Use Entry Box
        self.DIR_ENTRY = Entry(self.MAIN_FRAME, bg= self.BG, fg= self.FG, font= ("Seoge UI",10))
        self.DIR_ENTRY.pack(side= 'left', fill= 'x', expand= 1, pady= 5)

        # Search Frame
        self.__SEARCH_FRM = Frame(self.MAIN_FRAME, bg= self.BG)
        self.__SEARCH_FRM.pack(side= 'right')

        def del_ent() :
            self.SEARCH_ENTRY.config(state= "normal")
            self.SEARCH_ENTRY.delete(0, 'end')

        self.SEARCH_ENTRY = Entry(self.__SEARCH_FRM, bg= self.BG, width= 30, fg= self.FG, font= ("Seoge UI",10))
        self.SEARCH_ENTRY.insert(0, f"Search In Desktop")
        self.SEARCH_ENTRY.bind("<Button-1>", lambda e : del_ent())
        self.SEARCH_BTN = Button(self.__SEARCH_FRM, image= self.__SEARCH_IMG, bg= self.BG, fg= self.FG, font= ("Seoge UI",10), borderwidth= 0)
        self.REFRESH_BTN = Button(self.__SEARCH_FRM, image= self.__RELOAD_IMG, borderwidth= 0, bg= self.BG, fg= self.FG, font= ("Seoge UI",10))

        self.REFRESH_BTN.pack(side= 'left', padx= 3)
        self.SEARCH_BTN.pack(side= 'right', padx= (0,3))
        self.SEARCH_ENTRY.pack(side= 'left', padx= 3)


if __name__ == "__main__" :
    win = Tk()
    win.geometry("700x600")
    EntryBar(win)
    win.mainloop()