self.root.withdraw()
self.root2 = tk.Toplevel()
self.root2.geometry("329x434")
self.root2.configure(background='white')
self.root2.title('Logger')
self.root2.resizable(0, 0)
self.root2.grid_rowconfigure(0, weight=1)
self.root2.grid_columnconfigure(0, weight=1)
photo = tk.PhotoImage(file=self.path + "/favicon.gif")
self.root2.tk.call('wm', 'iconphoto', self.root2._w, photo)

# Images

image1 = Image.open(self.path + "/topo.gif")
photo1 = ImageTk.PhotoImage(image1)
image_file_path = "/home/guibax/Programs/PycharmProjects/Telesup/loading.gif"
photo = tk.PhotoImage(file=self.path + "/favicon.gif")
self.dow_img = tk.PhotoImage(file=self.path + "/downloads-icon.gif")
self.teleduc_img = tk.PhotoImage(file=self.path + "/iconalunos.png")
self.moodle_img = tk.PhotoImage(file=self.path + "/iconmoodle.png")
self.cancel_img = tk.PhotoImage(file=self.path + "/Cancel-512.gif")

# Frames

fr10 = tk.Frame(self.root2, bg="white")
self.fr11 = tk.Frame(
    fr10, bg="#AEB3C9",
    highlightbackground='#9A0050', highlightcolor='#9A0050', highlightthickness=1)
fr10.columnconfigure(0, weight=1)

self.fr11.rowconfigure(0, weight=1)
self.fr11.focus_get()

self.fr12 = tk.Frame(
    fr10, bg="white")
fr10.columnconfigure(0, weight=1)

self.fr12.rowconfigure(0, weight=1)

# Labels
lb00 = tk.Label(fr10, height=50, image=photo1)
lb00.image = photo1

lb01 = tk.Label(self.fr11, text="Usuário")
lb02 = tk.Label(self.fr11, text="Senha")
lb03 = tk.Label(self.fr11, text="RA", width=15, bg="#AEB3C9", font=(None, 7), fg="grey")
self.lb04 = tk.Label(self.fr11, text="Erro de autenticação.", fg='red', bg="#AEB3C9")
self.lb05 = tk.Label(self.fr12, height=40, image=self.ani_img[0], bg="white")
self.lb06 = tk.Label(self.fr12, text="Aguarde, carregando arquivos...", bg="white", fg="#9A0050")

# Text
self.tx1 = tk.Text(self.fr2, text=None)

# Buttons

bt01 = tk.Button(
    self.fr11, text="Enter",
    highlightbackground='#9A0050', highlightcolor='#9A0050',
    command=self.itnerator)
bt02 = tk.Button(
    self.fr11, text="Exit", highlightbackground='#9A0050',
    highlightcolor='#9A0050', command=self.root2.destroy)

self.bt03 = tk.Button(fr10, image=self.teleduc_img, command=self.log)

self.bt04 = tk.Button(
    fr10, image=self.moodle_img)

# Entry
self.user_entry = tk.Entry(self.fr11, highlightbackground='#9A0050', highlightcolor='#9A0050')
self.pass_entry = tk.Entry(self.fr11, highlightbackground='#9A0050', highlightcolor='#9A0050', show="*")

# Placing
bt01.grid(row=3, column=1, sticky="W", padx=(10, 0))
bt02.grid(row=3, column=1, sticky="W", padx=(110, 0), pady=(10, 10))
self.bt03.grid(row=1, column=0, pady=15)
self.bt04.grid(row=2, column=0, pady=15)
fr10.grid(sticky="NSEW")
self.fr11.grid_forget()
self.fr12.grid_forget()
lb00.grid(row=0, column=0, sticky="NSEW")
lb01.grid(row=0, column=0, sticky="W", padx=(20, 0), pady=15)
lb02.grid(row=1, column=0, sticky="W", padx=(20, 0))
lb03.grid(row=0, column=2)
self.lb04.grid(row=2, column=1)
self.lb04.grid_forget()
self.lb05.grid_forget()
self.lb06.grid_forget()
self.tx1.grid(column=0, row=0)
self.user_entry.grid(row=0, column=1, sticky="W", padx=(10, 0), pady=(5, 15))
self.pass_entry.grid(row=1, column=1, sticky="W", padx=(10, 0), pady=(5, 15))
