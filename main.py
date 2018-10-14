from gui import GUI
import requests
from telescraper import Methods
from moodlescraper import Methods as Methods2
import re
import threading
from tkinter import filedialog
import os


class Telescraper:
    def __init__(self):
        self.gui = GUI()
        self.gui.mainloop()
        self.usr = None
        self.pss = None


class Authentication:
    def __init__(self, usr, pss, parent):
        self.usr = usr
        self.pss = pss
        self.session = None
        self.methods = Methods
        self.methods2 = Methods2
        self.parent = parent
        self.dis = None
        self.it = None
        self.doc = None
        self.thread = None

    def check_connection(self):
        self.session = requests.Session()
        url = "https://www.ggte.unicamp.br/ea/"
        timeout = 5
        try:
            _ = requests.get(url, timeout=timeout)
            self.session.close()
            return True

        except requests.ConnectionError:
            self.session.close()
            return False

    def telescraping(self):
        try:
            log = self.methods(self.usr, self.pss, self.display_in_thread).init_scrapper()
            return log
        except:
            print("erro")

    def moodlescraping(self):
        log = self.methods2(self.usr, self.pss, self.display_in_thread).init_scrapper()
        return log

    def display_in_thread(self, name, it, doc):
        self.thread = threading.Thread(target=self.display_current)
        self.dis = name
        self.it = it
        self.doc = doc
        self.thread.start()

    def display_current(self):
        pass
        if self.it == 0:
            label = self.parent.ani_display1
            label.config(text=self.dis)
        else:
            label = self.parent.ani_display2
            label.config(text=self.doc)


class Listing:
    def __init__(self,  parent, disciplinas, doc_names, dis_docs, topiclink, plat, progbar, tkbutton, threadin):
        self.parent = parent
        self.disciplinas = disciplinas
        self.doc_names = doc_names
        self.dis_docs = dis_docs
        self.topiclink = topiclink
        self.plat = plat
        self.progbar = progbar
        self.tkbutton = tkbutton
        self.threading = threadin
        self.dow_img = self.parent.tka.PhotoImage(file="/home/guibax/Programs/PycharmProjects/Tele/downloads-icon.gif")
        self.listing()

    def listing(self):
        tree = self.parent.ttk.Treeview(self.parent.selector_txt)
        tree.heading('#0', text="Disciplinas")
        tree.bind(
            "<Double-1>",
            lambda event: self.parent.selecao(event, tree, self.dis_docs)
                        )
        keys = list(self.disciplinas.keys())

        for dis in keys:
            tree.insert("", "end", dis, text=dis)
            x = 1
            for doc in self.dis_docs[dis]:
                    while tree.exists(doc):
                        doc = doc + "(" + str(x) + ")"
                        x = x+1
                    tree.insert(dis, "end", doc, text=doc, image=self.dow_img)

        tree.grid(row=0, column=0, sticky="NSEW")

        self.parent.down_bt = self.tkbutton(
            self.parent.selected_d_text, text="Download",
            highlightbackground=self.parent.color1, highlightcolor=self.parent.color1,
            command=self.predown
        )
        self.parent.down_bt.grid(row=0, column=1, sticky="W", padx=(0, 20))
        self.parent.clear_bt = self.tkbutton(
                                    self.parent.selected_d_text, command=self.cleaning,
                                    highlightbackground=self.parent.color1,
                                    highlightcolor=self.parent.color1, text="Limpar"
                                                    )
        self.parent.clear_bt.grid(row=0, column=0, sticky="W", padx=(20, 0))

    def cleaning(self):
        self.parent.selected_txt.delete("1.0", "end")
        self.progbar['value'] = 0

    def predown(self):
        docs_selection = self.parent.selected_txt.get("1.0", 'end-1c')
        rep = docs_selection.replace("\n", ",")
        splited = rep.split(",")
        for i in splited:
            if i == '':
                del splited[splited.index(i)]
        ls = len(splited)
        if ls:
            Download(splited, self, ls)
        else:
            self.parent.parent.pop_up("Nem um documento foi selecionado!")


class Download:
    def __init__(self, splited, parent, ls):

        self.parent = parent
        self.splited = splited
        self.docdic = self.parent.doc_names
        self.parent.log = self.parent.parent.log
        self.topiclink = self.parent.topiclink
        self.plat = self.parent.plat
        self.prog_bar = self.parent.progbar
        self.threading = self.parent.threading
        self.ls = ls
        self.webdir = 'http://webensino.unicamp.br/cursos'
        self.topic_docs = "http://webensino.unicamp.br/cursos/aplic/material/ver.php?"
        self.cur = 0
        self.docname = None
        self.subfolder = 1
        self.folder = None
        self.filename = None
        self.filedir = 0
        self.dirname = None
        self.filesize = 0
        self.check_folder()

    def check_folder(self):
        self.parent.parent.parent.pop_up("Gostaria de criar subpastas para cada Disciplina?", "folder", self)

    def iter(self, folder):
        self.folder = folder
        self.thread = self.threading.Thread(target=self.tester)
        self.thread.start()

    def tester(self):
        self.filedir = filedialog.askdirectory()

        for doc in self.splited:
            self.docname = doc
            keys = list(self.parent.dis_docs.keys())
            dic = list(self.parent.dis_docs.values())
            if self.folder == 0:
                main_folder = self.filedir + "/Telescraper"
                for dis in dic:
                    for doca in dis:
                        if doca == self.docname:
                            self.dirname = (keys[dic.index(dis)]).split("-")[0]
                            if os.path.isdir(main_folder):
                                if os.path.isdir(main_folder+"/"+self.dirname):
                                    self.post_down()
                                else:
                                    os.mkdir(main_folder+"/"+self.dirname)
                                    self.post_down()
                            else:
                                os.mkdir(main_folder)
                                os.mkdir(main_folder+"/"+self.dirname)
                                self.post_down()
            else:
                self.post_down()

    def post_down(self):
        doclink = (self.docdic[self.docname])
        if self.plat == "Teleduc":
            topiclink = self.topiclink[doclink]
            topic_html = self.parent.log.get(self.topic_docs+topiclink)
            idd = re.findall(r"(?<=\+\')(.*?)(?=\')", topic_html.text, re.MULTILINE)
            r = self.parent.log.get(self.webdir+doclink+idd[0])
            self.filesize = r.headers.get('Content-Length')
            self.prog(r)
        else:
            r = self.parent.log.get(doclink)
            self.filesize = r.headers.get('Content-Length')
            self.prog(r)

    def prog(self,  r,):
        if self.folder == 0:
            self.filename = self.filedir+"/Telescraper/"+self.dirname+"/"+self.docname
            self.prog_bar['maximum'] = self.ls
            self.final_down(r)
        else:
            self.filename = self.filedir+"/"+self.docname
            self.prog_bar['maximum'] = self.ls
            self.final_down(r)

    def final_down(self, r):
        with open(self.filename, 'wb') as f:
            if self.filesize is None:  # no content length header
                f.write(r.content)
            else:
                for chunk in r.iter_content(chunk_size=1):
                    f.write(chunk)
        self.cur = self.cur + 1
        self.prog_bar['value'] = self.cur


if __name__ == "__main__":
    Telescraper()
