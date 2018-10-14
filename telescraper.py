import requests
import re


class Methods:
    def __init__(self, usr, pss, parent):
        self.get_aprovado = "<Response [200]>"
        self.login_url = "https://www.ggte.unicamp.br/ea/index_ldap.php"
        self.baseurl = 'http://webensino.unicamp.br/pagina_inicial/index.php'
        self.filedir = 'http://webensino.unicamp.br/cursos'

        self.relista = open("regex_strings.txt", "r").readlines()
        self.urls = open("urls.txt", "r").readlines()
        self.payload = {
            'user': '160251',
            'pass': '*ThC420*',
            'btnTeleduc': 'submit'  # remember me
        }
        self.payload2 = {'enviaA': 'disciplinas', 'enviaB': '', 'enviaC': ''}
        self.dis_name = []
        self.topic_url = []
        self.distopic = {}
        self.topic_linkdoc = {}
        self.topic_docname = {}
        self.docname_link = {}
        self.dis_docs = {}
        self.req = requests.head
        self.parent_display = parent
        self.session = requests.Session
        self.log = None

        # self.matching_text()

    def init_scrapper(self):
        self.urls = [string.replace("\n", "") for string in self.urls]
        self.relista = [string.replace("\n", "") for string in self.relista]
        return self.check_auth()

    def check_auth(self):
        self.log = self.session()
        log = re.findall(r"Teleduc 3", self.log.post(self.login_url, data=self.payload).text, re.MULTILINE)
        if log:
            return "erro de login"
        else:
            return self.matching_disc()

    def matching_disc(self):
        ativas_page = (self.log.post(self.baseurl, data=self.payload2)).text
        get_ativas = re.findall(r"&cod_curso=[0-9]*", ativas_page, re.MULTILINE)
        if get_ativas:
            for disciplina in get_ativas:
                self.match_topicos(disciplina)
        else:
            print("No such pattern")
        return {
            'distopic': self.distopic,
            'docname_link': self.docname_link,
            'dis_docs': self.dis_docs,
            'log': self.log,
            'topic_link': self.topic_linkdoc
        }

    def match_topicos(self, disciplina):
        material_apoio = self.log.get(self.urls[2] + 'material.php?' + disciplina + '&cod_ferramenta=4')
        if str(material_apoio) == self.get_aprovado:
            for name in re.findall(r"(?=[A-Z]{2})(.*)(?=</nobr)", material_apoio.text, re.MULTILINE):
                if name:
                    self.dis_name.append(name)
                    self.parent_display(name, 0, "none")
                    sub_pasta = re.findall(
                        r"(?=material.php)(.*?)(?=\"><img src=../figuras)", material_apoio.text, re.MULTILINE
                    )
                    if sub_pasta:
                        for pasta in sub_pasta:
                            pasta = self.log.get(self.urls[2] + pasta)
                            match_topico = re.findall(r"(?=ver.php)(.*?)(?=\"><)", pasta.text, re.MULTILINE)
                            if match_topico:
                                return self.matching(name, material_apoio, match_topico)
                    else:
                        match_topico = []
                        return self.matching(name, material_apoio, match_topico)


                else:
                    print("Disciplina Inexistente")

    def matching(self, name, material_apoio, match_topico):
        docs_dis = []
        if not match_topico:
            match_topico = re.findall(
                r"(?=cod_curso)(.*)(?=\"><img src=../figuras/arqp.gif)", material_apoio.text, re.MULTILINE
            )
        self.distopic.update({name: match_topico})
        for topico in match_topico:
            self.topic_url.append(topico)
            doclink = []
            doc_names = []
            docs = self.log.get(self.urls[3] + topico)

            if str(docs) == self.get_aprovado:
                for doc in re.findall(r"/\w*/\w*///.+?(?=\s)", docs.text, re.MULTILINE):
                    doclink.append(doc)
            else:
                print("ué")
            for link in doclink:
                self.topic_linkdoc.update({link: topico})
            finddoc = re.findall(r"(?<=/{3})(.*?)(?=\s)", docs.text, re.MULTILINE)
            for docname in finddoc:
                replace = (docname.replace("%20", " "))
                doc_names.append(replace)
                docs_dis.append(replace)
            for docname in range(0, len(finddoc)):
                self.docname_link.update({doc_names[docname]: doclink[docname]})
                self.parent_display(name, 1, finddoc[docname])

        self.dis_docs.update({name: docs_dis})
        return
