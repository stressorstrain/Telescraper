# -*- coding: utf-8 -*-
import tkinter as tk

class Model():
    def __init__(self):
        self.mode = tk.IntVar()


class NavbarFrm(tk.Frame):
    def __init__(self, master=None, mode_var=None):
        tk.Frame.__init__(self, master)
        self.__mode = mode_var
        self.__init()

    def __init(self):
        self.__rb_1 = tk.Radiobutton(self, text="Option 1",
                                     variable=self.__mode,
                                     value=0)
        self.__rb_2 = tk.Radiobutton(self, text="Option 2",
                                     variable=self.__mode,
                                     value=1)
        self.__rb_3 = tk.Radiobutton(self, text="Option 3",
                                     variable=self.__mode,
                                     value=2)
        self.__packing()

    def __packing(self):
        self.__rb_1.pack(side="left")
        self.__rb_2.pack(side="left")
        self.__rb_3.pack(side="left")


class LabelFrm(tk.Frame):
    def __init__(self, master=None, mode_var=None):
        tk.Frame.__init__(self, master)
        self.__mode = mode_var
        self.__init()

    def __init(self):
        self.__label = tk.Label(self, textvariable=self.__mode)
        self.__packing()

    def __packing(self):
        self.__label.pack()


class MainApp(tk.Frame):
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.__init(model)

    def __init(self, model):
        self.__model  = Model()
        self.__navbar = NavbarFrm(self, self.__model.mode)
        self.__label  = LabelFrm(self,  self.__model.mode)
        self.__packing()

    def __packing(self):
        self.__navbar.pack(fill="x")
        self.__label.pack(fill="both")

        self.pack(expand=True, fill="both")


def main():
    root = tk.Tk()
    root.title("test")
    model = Model()
    app = MainApp(root, model)
    root.mainloop()

if __name__ == '__main__':
    main()