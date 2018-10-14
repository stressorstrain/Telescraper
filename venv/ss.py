self.path = os.getcwd()
self.root2 = None
self.user_entry = None
self.root = tk.Tk()
# self.main = main.Telescraper
self.mainlog = None
self.filedir = 'http://webensino.unicamp.br/cursos'
self._frames = []

# Defaults colors
self.color1 = "#9A0050"
self.color2 = "#A6ACE6"

self.root.geometry("950x504")
self.root.configure(background=self.color2)
photo = tk.PhotoImage(file=self.path + "/favicon.gif")
self.dow_img = tk.PhotoImage(file=self.path + "/downloads-icon.gif")
self.teleduc_img = tk.PhotoImage(file=self.path + "/iconalunos.png")
self.moodle_img = tk.PhotoImage(file=self.path + "/iconmoodle.png")
self.cancel_img = tk.PhotoImage(file=self.path + "/Cancel-512.gif")
# self.root.tk.call('wm', 'iconphoto', self.root._w, photo)
self.root.title('Telescrapper')
self.root.resizable(0, 0)

self.fr1 = tk.Frame(self.fr0, bg="white", height=100, width=250)
self.fr2 = tk.Frame(self.fr0, bg="white", width=250, height=100)
self.bt1 = tk.Button(self.fr2, text="down", command=self.real_down)
self.fr10 = None
self.fr11 = None
self.lb04 = None
self.tx1 = None
widget_list = [self.root, self.fr0, self.fr1]

for widget in widget_list:
    widget.grid_rowconfigure(0, weight=1)
    widget.grid_columnconfigure(0, weight=1)

# Progressbar
self.progress = ttk.Progressbar(self.fr2, orient="horizontal",
                                length=200, mode="determinate")
self.bytes = 0
self.maxbytes = 0

# Placing
self.fr0.grid(row=0, column=0, sticky="NSEW")
self.fr1.grid(row=0, column=0, sticky="NSEW", pady=(10, 10), padx=(5, 3))
self.fr2.grid(row=0, column=1, pady=(10, 10), padx=(1, 5), sticky="NS")
self.bt1.grid(row=1, column=0, sticky="NS")
self.progress.grid(row=2, column=0, sticky="NSEW", pady=(10, 0))
self.log_gui()
self.root.mainloop()
