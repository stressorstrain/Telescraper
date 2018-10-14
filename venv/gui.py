import tkinter as tk
from PIL import Image, ImageTk
import os


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.color2 = "#A6ACE6"
        self.path = os.getcwd()

        # Frames
        container = tk.Frame(self, bg=self.color2)
        self.frames = {}
        frame = Log_Page(container, self)
        self.frames[Log_Page] = frame
        self.show_frame(Log_Page)

        # Placing
        container.grid(row=0, column=0, sticky="NSEW")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        frame.grid(column=0, row=0, sticky="NSEW")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Log_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#A6ACE6", width=20, height=20)
        self.path = os.getcwd()

        # Frames
        self.log_frame = tk.Frame(
            self, parent, bg="#AEB3C9",
            highlightbackground='#9A0050', highlightcolor='#9A0050',
            highlightthickness=1
        )
        self.log_frame.grid_forget()
        self.plat_buttons = tk.Frame(
            self, parent, bg="#AEB3C9",
            highlightbackground='#9A0050', highlightcolor='#9A0050',
            highlightthickness=1
        )
        self.plat_buttons.grid(row=1, sticky="NS", padx=(10, 10), pady=(20, 20))

        # Images
        banner_img = ImageTk.PhotoImage(Image.open(self.path + "/topo2.gif"))
        teled_img = tk.PhotoImage(self.path + "/iconalunos.png")

        # Labels
        usr_lb = tk.Label(self.log_frame, text="Usuário")
        usr_lb.grid(row=0, column=0, sticky="W", padx=(50, 0), pady=15)

        pss_lb = tk.Label(self.log_frame, text="Senha")
        pss_lb.grid(row=1, column=0, sticky="W", padx=(50, 0))

        ra_lb = tk.Label(self.log_frame, text="RA", width=15, bg="#AEB3C9", font=(None, 7), fg="grey")
        ra_lb.grid(row=0, column=2)
        dac_lb = tk.Label(self.log_frame, text="Senha DAC", width=15, bg="#AEB3C9", font=(None, 7), fg="grey")
        dac_lb.grid(row=1, column=2)

        banner_lb = tk.Label(self,  image=banner_img)
        banner_lb.image = banner_img
        banner_lb.grid(column=0, row=0)

        # self.lb04 = tk.Label(log_frame, text="Erro de autenticação.", fg='red', bg="#AEB3C9")

        # Entries
        self.user_entry = tk.Entry(self.log_frame, highlightbackground='#9A0050', highlightcolor='#9A0050')
        self.user_entry.grid(row=0, column=1, sticky="W", padx=(10, 0), pady=(5, 15))
        self.pass_entry = tk.Entry(self.log_frame, highlightbackground='#9A0050', highlightcolor='#9A0050', show="*")
        self.pass_entry.grid(row=1, column=1, sticky="W", padx=(10, 0), pady=(5, 15))

        # Buttons
        enter_bt = tk.Button(
            self.log_frame, text="Enter",
            highlightbackground='#9A0050', highlightcolor='#9A0050',
                                    )
        enter_bt.grid(row=3, column=1, sticky="W", padx=(10, 0))
        exit_bt = tk.Button(
            self.log_frame, text="Exit", highlightbackground='#9A0050',
            highlightcolor='#9A0050'
                                    )
        exit_bt.grid(row=3, column=1, sticky="W", padx=(110, 0), pady=(10, 10))

        teleduc_bt = tk.Button(self.plat_buttons, image=teled_img)
        teleduc_bt.grid()

    def pick_plataforma(self):
        self.log_frame.grid(row=1, sticky="NS", padx=(10, 10), pady=(20, 20))


app = GUI()
app.mainloop()
