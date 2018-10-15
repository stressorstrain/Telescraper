import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
import animated


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.color2 = "#A6ACE6"
        self.path = os.getcwd()
        self.resizable(0, 0)
        self.title("Telescraper")
        icon = ImageTk.PhotoImage(Image.open(self.path + "/favicon.gif"))
        self.tk.call('wm', 'iconphoto', self._w, icon)
        LogPage(self)


class LogPage(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.parent.withdraw()
        self.color0 = "#AEB3C9"
        self.color1 = "#9A0050"
        self.resizable(0, 0)
        self.path = os.getcwd()
        self.thread = None
        self.plataforma = None
        self.folder = None
        icon = ImageTk.PhotoImage(Image.open(self.path + "/favicon.gif"))

        self.tk.call('wm', 'iconphoto', self._w, icon)

        # Frames
        main_frame = tk.Frame(self, bg=self.color0)
        main_frame.grid()

        self.log_frame = tk.Frame(
            main_frame, bg=self.color0,
            highlightbackground=self.color1, highlightcolor=self.color1,
            highlightthickness=1
        )
        self.log_frame.grid_forget()

        self.labelf = tk.Frame(main_frame, bg=self.color0)
        self.labelf.grid(row=1, pady=10)

        self.plat_buttons = tk.Frame(main_frame,  bg=self.color0)
        self.plat_buttons.grid(row=2, sticky="NS", padx=(10, 10), pady=(10, 20))

        self.aniframe = tk.Frame(main_frame, bg=self.color0)
        self.aniframe.grid(row=3, column=0)

        # Images
        banner_img = ImageTk.PhotoImage(Image.open(self.path + "/topo2.gif"))
        teled_img = ImageTk.PhotoImage(Image.open(self.path + "/iconalunos.gif"))
        moodle_img = ImageTk.PhotoImage(Image.open(self.path + "/iconmoodle.jpeg"))
        ani_path = "/home/guibax/Programs/PycharmProjects/Tele/loading.gif"
        self.ani_img = animated.AnimatedGif(ani_path)

        # Labels
        usr_lb = tk.Label(self.log_frame, text="Usuário", bg=self.color0)
        usr_lb.grid(row=0, column=0, sticky="W", padx=(50, 0), pady=15)

        pss_lb = tk.Label(self.log_frame, text="Senha", bg=self.color0)
        pss_lb.grid(row=1, column=0, sticky="W", padx=(50, 0))

        ra_lb = tk.Label(self.log_frame, text="RA", width=15, bg=self.color0, font=(None, 7), fg="grey")
        ra_lb.grid(row=0, column=2)
        dac_lb = tk.Label(self.log_frame, text="Senha DAC", width=15, bg=self.color0,  font=(None, 7), fg="grey")
        dac_lb.grid(row=1, column=2)

        self.plat_lb = tk.Label(self.log_frame, bg=self.color0, fg="green")
        self.plat_lb.grid(row=4, column=1)

        banner_lb = tk.Label(main_frame,  image=banner_img)
        banner_lb.image = banner_img
        banner_lb.grid(column=0, row=0)

        text_label = tk.Label(self.labelf, text="Selecione a plataforma desejada: ", bg=self.color0, fg=self.color1)
        text_label.grid()

        # self.lb04 = tk.Label(self.log_frame, text="Erro de autenticação.", fg='red', bg="#AEB3C9")
        self.anilb = tk.Label(self.aniframe,  image=self.ani_img[0], bg=self.color0)
        self.anilb.grid_forget()
        self.anitxt = tk.Label(self.aniframe,   text="Aguarde, carregando arquivos...", bg=self.color0, fg=self.color1)
        self.anitxt.grid_forget()
        self.ani_display1 = tk.Label(self.aniframe, text="Disciplina: ", bg=self.color0, fg=self.color1)
        self.ani_display1.grid_forget()
        self.ani_display2 = tk.Label(self.aniframe, text="Documento: ", bg=self.color0, fg=self.color1)
        self.ani_display2.grid_forget()

        # Entries
        self.user_entry = tk.Entry(self.log_frame, highlightbackground=self.color1, highlightcolor=self.color1)
        self.user_entry.grid(row=0, column=1, sticky="W", padx=(10, 0), pady=(5, 15))
        self.pass_entry = tk.Entry(
                                                        self.log_frame, highlightbackground=self.color1,
                                                        highlightcolor=self.color1, show="*"
                                                        )
        self.pass_entry.grid(row=1, column=1, sticky="W", padx=(10, 0), pady=(5, 15))

        # Buttons
        enter_bt = tk.Button(
            self.log_frame, text="Entrar",
            highlightbackground=self.color1, highlightcolor=self.color1,
            command=self.itnerator
                                    )
        enter_bt.grid(row=3, column=1, sticky="W", padx=(10, 0))
        exit_bt = tk.Button(
            self.log_frame, text="Sair", highlightbackground=self.color1,
            highlightcolor=self.color1, command=self.quit
                                    )
        exit_bt.grid(row=3, column=1, sticky="W", padx=(110, 0), pady=(10, 10))
        back_bt = tk.Button(
            self.log_frame, text="Voltar", highlightbackground=self.color1,
            highlightcolor=self.color1, command=self.back_button
                                    )
        back_bt.grid(row=3, column=2,  pady=(10, 10))

        teleduc_bt = tk.Button(self.plat_buttons, image=teled_img, command=lambda: self.pick_plataforma('Teleduc'))
        teleduc_bt .image = teled_img
        teleduc_bt.grid()

        moodle_bt = tk.Button(self.plat_buttons, image=moodle_img, command=lambda: self.pick_plataforma("Moodle"))
        moodle_bt .image = moodle_img
        moodle_bt.grid(pady=10)

    def back_button(self):
        self.plat_buttons.grid(row=1, sticky="NS", padx=(10, 10), pady=(20, 20))
        self.log_frame.grid_forget()
        self.anitxt.grid_forget()
        self.ani_display1.grid_forget()
        self.ani_display2.grid_forget()

    def pick_plataforma(self, plataforma):
        self.plataforma = plataforma
        self.plat_buttons.grid_forget()
        self.labelf.grid_forget()
        self.plat_lb.config(text="Plataforma Atual: "+self.plataforma)
        self.log_frame.grid(row=1, sticky="NS", padx=(10, 10), pady=(20, 20))

    def pick_entries(self):
        self.aniframe.grid(row=3, column=0)
        try:
            from main import Authentication
            user = str(self.user_entry.get())
            pss = str(self.pass_entry.get())
            main = Authentication
            net_status = Authentication(user, pss, self).check_connection()
            if net_status:
                if self.plataforma == 'Teleduc':
                    auth_response = main(user, pss, self).telescraping()
                    if auth_response == "erro de login":
                        self.pop_up(auth_response, 0, None)
                        self.thread.stop()
                    else:
                        disciplina = auth_response['distopic']
                        doc_names = auth_response['docname_link']
                        dis_docs = auth_response['dis_docs']
                        log = auth_response['log']
                        topiclink = auth_response['topic_link']
                        Main(self, disciplina, doc_names, dis_docs, log, topiclink, self.plataforma)
                elif self.plataforma == "Moodle":
                    auth_response = main(user, pss, self).moodlescraping()
                    if auth_response == "erro de login":
                        self.pop_up(auth_response, 0, None)
                        self.thread.stop()
                        return
                    else:
                        disciplina = auth_response['distopic']
                        doc_names = auth_response['doc_name']
                        dis_docs = auth_response['dis_docs']
                        log = auth_response['log']
                        topiclink = None
                        Main(self, disciplina, doc_names, dis_docs, log, topiclink, self.plataforma)
            else:
                net_status = "Falha na conexão com o site, verifique sua rede ou se o site está ativo"
                self.pop_up(net_status, 0, None)
        except:
            erro = "erro no scraping, tente novamente"
            self.anitxt.config(text="Erro no scraping")
            self.pop_up(erro, 0, None)
            self.anilb.grid_forget()

    def quit(self):
        self.destroy()
        self.parent.destroy()

    def update_label_image(self, label, ani_img, ms_delay, frame_num):
        label.configure(image=ani_img[frame_num])
        frame_num = (frame_num + 1) % len(ani_img)
        self.after(ms_delay, self.update_label_image, label, ani_img, ms_delay, frame_num)

    def enable_animation(self):
        ms_delay = 1000 // len(self.ani_img)
        self.after(ms_delay, self.update_label_image, self.anilb, self.ani_img, ms_delay, 0)

    def animate_in_thread(self):
        self.thread = threading.Thread(target=self.pick_entries)
        self.thread.start()

    def itnerator(self):
        self.anilb.grid(row=1, column=0)
        self.anitxt.grid(row=0, column=0)
        self.ani_display1.grid(row=2, column=0, sticky="W")
        self.ani_display2.grid(row=3, column=0, sticky="W")
        self.animate_in_thread()
        self.animate()

    def animate(self):
        self.anilb.grid(pady=(10, 10))
        self.anilb.grid(row=1, pady=(10, 10))
        self.enable_animation()

    def pop_up(self, text, command, who):
        toplevel = tk.Toplevel(self, bg=self.color0)
        texto = str(text)
        icon = ImageTk.PhotoImage(Image.open(self.path + "/favicon.gif"))
        toplevel.tk.call('wm', 'iconphoto', toplevel._w, icon)
        toplevel.resizable(0, 0)
        label = tk.Label(toplevel, text=texto, bg=self.color0, fg=self.color1)
        label.grid(row=0, pady=(10, 10), padx=(10, 10))
        if command:
            self.itnerato(toplevel,  command, who)

    def itnerato(self, toplevel, command, who):
        buttonf = tk.Frame(toplevel, width=20, bg="black")
        ok_bt = tk.Button(buttonf, text="Sim")
        ncl_bt = tk.Button(buttonf, text="Não")
        buttonf.grid(row=1, pady=(2, 10))
        ok_bt.grid(row=0, column=0)
        ncl_bt.grid(row=0, column=1)

        if command == "folder":
            ok_bt.config(command=lambda: self.foldera(who, 0, toplevel))
            ncl_bt.config(command=lambda: self.foldera(who, 1, toplevel))
        else:
            ok_bt.config(command=lambda: self.change_plat(0, toplevel, who))
            ncl_bt.config(command=lambda: self.change_plat(1, toplevel, who))

    def foldera(self, parent, ans, level):
        if ans == 0:
            level.destroy()
            # parent.folder = 0
            parent.iter(0)

        else:
            level.destroy()
            # parent.folder = 1
            parent.iter(1)

    def change_plat(self, ans, level, arg):
        if ans == 0:
            if self.plataforma == "Teleduc":
                self.plataforma = "Moodle"
                self.plat_lb.config(text="Plataforma Atual: " + self.plataforma)
                arg.destroy()
                self.deiconify()
                self.aniframe.grid_forget()
            else:
                self.plataforma = "Teleduc"
                self.plat_lb.config(text="Plataforma Atual: " + self.plataforma)
                arg.destroy()
                self.deiconify()
                self.aniframe.grid_forget()

            level.destroy()
        else:
            level.destroy()


class Main(tk.Toplevel):
    def __init__(self, parent, disciplina, doc_names, dis_docs, log, topiclink, plat):
        tk.Toplevel.__init__(self, parent, bg="#AEB3C9")
        self.parent = parent
        self.color0 = "#AEB3C9"
        self.color1 = '#9A0050'
        self.tka = tk
        self.parent.withdraw()
        self.path = os.getcwd()
        icon = ImageTk.PhotoImage(Image.open(self.path + "/favicon.gif"))
        self.tk.call('wm', 'iconphoto', self._w, icon)
        self.resizable(0, 0)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        wipor = (int(self.screen_porc("width", 56)))
        hepor = (int(self.screen_porc("height", 50)))
        x = str(int(self.screen_height/2 - hepor/2))
        y = str(int(self.screen_width/2 - wipor/2))
        self.geometry('{}x{}+{}+{}'.format(wipor, hepor, y, x))
        self.ttk = ttk
        self.listing = None
        self.disciplina = disciplina
        self.doc_names = doc_names
        self.dis_docs = dis_docs
        self.log = log
        self.topiclink = topiclink
        self.plat = plat
        self.selecoes = []
        self.update()

        # Frames

        main_frame = tk.Frame(self, bg=self.color0)
        main_frame.grid(sticky="NSEW", padx=(10, 10), pady=(10, 10))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        main_frame.grid_propagate(0)

        self.selected = tk.Frame(
                                 main_frame, bg=self.color0, highlightbackground=self.color1,
                                 highlightcolor=self.color1, highlightthickness=1
                                                    )
        self.selected.grid(row=0, column=1, pady=(5, 5), padx=(5, 5), sticky="NS")
        self.selected.grid_columnconfigure(0, weight=1)

        self.selected_txt = tk.Frame(self.selected)
        self.selected_txt.grid(row=1, column=0, sticky="N")

        self.selected_down = tk.Frame(self.selected, bg=self.color0)
        self.selected_down.grid(row=3, column=0,  pady=(10, 0), sticky="EW")
        self.selected_down.grid_columnconfigure(0, weight=1)

        self.prgo_fr = tk.Frame(self.selected, bg=self.color0)
        self.prgo_fr.grid(row=2, column=0, pady=5)

        # Labels
        self.down_lb = tk.Label(self.selected, text= "LISTA DE DOWNLOADS", bg=self.color0, font='Helvetica 10 bold')
        self.down_lb .grid(row=0, column=0, pady=(5, 0))
        # Text

        self.selector_txt = tk.Frame(
                                                             main_frame, bg="white", highlightbackground=self.color1,
                                                             highlightcolor=self.color1
                                                            )
        self.selector_txt.grid(column=0, row=0, sticky="NSEW")
        self.selector_txt.grid_rowconfigure(0, weight=1)
        self.selector_txt.grid_columnconfigure(0, weight=1)

        self.selected_txt = tk.Text(
                                    self.selected_txt, bg="white",
                                    highlightbackground=self.color1, highlightcolor=self.color1
                                                        )
        self.selected_txt.grid(column=0, row=0)

        self.selected_d_text = tk.Frame(self.selected_down, bg=self.color0)
        self.selected_d_text.grid(column=0, row=0, sticky="EW ")
        self.selected_d_text.grid_columnconfigure(0, weight=1)

        # Buttons
        self.exit_bt = tk.Button(
            self.selected_d_text, command=self.destroy, bg=self.color0,
            highlightbackground=self.color1, highlightcolor=self.color1, text="Sair"
        )
        self.exit_bt.grid(row=1, column=1, pady=(10, 0))
        self.plat_bt = tk.Button(
            self.selected_d_text,  bg=self.color0, fg=self.color1, cursor="hand2", relief="flat",
            text="Plataforma Atual: " + self.plat, borderwidth=0, highlightthickness=0,
            activebackground=self.color0, activeforeground="green",
            command=lambda: self.parent.pop_up("Deseja mudar de plataforma?", 0, self)
        )
        self.inst_lb = tk.Label(self.prgo_fr,
                                text="*Duplo clique no nome da disciplina para selecionar todos os seus documentos para download"
                                +"\n"+"*Duplo clique no nome do documento para adiciona-lo a lista de downloads                 ",
                                bg=self.color0, fg="grey", font=("Courier", 7))
        self.inst_lb.grid(row=0, column=0)
        self.plat_bt.grid(row=1, column=0, pady=(0, 0), sticky='w')
        self.plat_lb =tk.Label(self.selected_d_text, bg=self.color0, fg="grey", text=" \t*clique para mudar ", font=("Courier", 7))
        self.plat_lb.grid(row=1,column=0, pady=(30, 0), sticky="w")

        self.prog_bar = ttk.Progressbar(self.prgo_fr, orient="horizontal", value=0,
                                        length=self.screen_porc("width", 26), mode="determinate")
        self.prog_bar.grid(column=0, row=1, pady=(20, 0))
        self.listinga()

    def screen_porc(self, vector, porc):

        if vector == "width":
                width = (self.screen_width*porc)/100
                return width
        elif vector == "height":
                height = (self.screen_height*porc)/100
                return height

    def listinga(self):
        from main import Listing
        self.listing = Listing
        self.listing(self, self.disciplina, self.doc_names, self.dis_docs, self.topiclink, self.plat, self.prog_bar, tk.Button, threading)

    def selecao(self, event, tree, disciplinas):
        self.selecoes = tree.selection()
        keys = disciplinas.keys()
        if self.selecoes[0] in keys:
            if disciplinas[self.selecoes[0]]:
                for docs in disciplinas[self.selecoes[0]]:
                    self.selected_txt.insert("end", docs+"\n")
            else:
                self.parent.pop_up("Sem materiais disponivels!", None, None)

        else:
            self.selected_txt.insert("end", self.selecoes[0] + "\n")