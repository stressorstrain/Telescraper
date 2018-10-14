import requests
import re


class Methods:
    def __init__(self, usr, pss, parent):
        self.usr = usr
        self.pss = pss
        self.relista = open("regex_strings.txt", "r").readlines()
        self.urls = open("urls.txt", "r").readlines()
        self.tag_strings = open("tag_Strings.txt").readlines()
        self.payload = {
            'username': '155606',
            'password': 'log2!Day4:20!',
        }
        self.login_url = 'https://www.ggte.unicamp.br/eam/login/index.php'
        self.distopic = {}
        self.docname_link = {}
        self.dis_docs = {}
        self.session = requests.Session
        self.log = None
        self.parent_display = parent
        self.init_scrapper()
        # self.matching_text()

    def init_scrapper(self):
        self.urls = [string.replace("\n", "") for string in self.urls]
        self.relista = [string.replace("\n", "") for string in self.relista]
        self.check_auth()
        return {
            'doc_name': self.docname_link,
            'dis_docs': self.dis_docs,
            'distopic': self.distopic,
            'log': self.log,

        }

    def check_auth(self):
        self.log = self.session()
        loggin = self.log.post(self.urls[6], data=self.payload)
        log_text = loggin.text

        if self.relista[10] in log_text:
            get_ativas_html = re.findall(
                r"(?=custom_menu_language)(.*?)(?=custom_menu_themecolours)",
                log_text)
            get_ativas_clean = re.findall(
                r"(?=custom_menu_language\" class=\"custom_menu\">)(.*?)(?<=/span></span></a></li><li>)",
                get_ativas_html[0])
            self.cleaning_match(get_ativas_html, get_ativas_clean)
        else:
            print(" Erro de Logina")

    def cleaning_match(self, get_ativas_html, get_ativas_clean):
        deltags = (get_ativas_html[0].replace(get_ativas_clean[0], ""))
        newtag = None
        tags = []
        dis_list = []

        for string in self.tag_strings:
            string = string.replace("\n", "")
            tags.append(string)

        if tags[0] in deltags:
            newtag = deltags.replace(tags[0], "")
            newtag = newtag.replace(tags[1], " ")
        disciplina = newtag.split('href=')
        x = disciplina[0]
        disciplina.remove(x)

        for dis in disciplina:
            x = re.findall(r"(?=[A-Z]_)(.*?)(?<=[A-Z]\d\D)", dis, re.MULTILINE)
            if len(x) > 1:
                dis = dis.replace(x[1], "")
            if tags[3] in dis:
                dis = dis.replace(tags[3], "")
            newdis = dis.split(">")
            dis_list.append(newdis)

        for lista in dis_list:
            self.distopic.update({lista[1]: lista[0]})
        self.matching_docs()

    def matching_docs(self):
        disname = list(self.distopic.keys())
        for dis in disname:
            self.parent_display(dis, 0, "doc")
            self.get_links(dis)

    def get_links(self, dis):
            dislink = self.distopic[dis].replace('"', "")
            get_dis_html = self.log.get(dislink)
            dis_html = get_dis_html.text
            docs_name = []
            docslink = re.findall(
                r"(?=http://www\.ggte\.unicamp\.br/eam/mod/resource/view)(.*?)(?=hide)",
                dis_html, re.MULTILINE)
            if not docslink:
                print("Sem Materiais Disponíveis")
            else:
                for string in docslink:
                    x = re.match(r"(?=^)(.*?)(?<=href=\")", string, re.MULTILINE)
                    if x:
                        string = re.sub(r"(?=^)(.*?)(?<=href=\")", "", string, re.MULTILINE)
                    strr = '<span class="access'
                    if strr in string:
                        string = string.replace(strr, "")
                    string = re.sub(r"(?=\"><)(.*?)(?<=name\">)", ", ", string, re.MULTILINE)
                    docname_link = string.split(",")
                    docs_name.append(docname_link[1])
                    self.parent_display(dis, 1, docname_link[1])
                    self.docname_link.update({docname_link[1]: docname_link[0]})
            self.dis_docs.update({dis: docs_name})
