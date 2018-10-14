import requests
import re


class Methods:
    def __init__(self, usr, pss):
        self.get_aprovado = "<Response [200]>"
        self.login_url = "https://www.ggte.unicamp.br/ea/index_ldap.php"
        self.baseurl = 'http://webensino.unicamp.br/pagina_inicial/index.php'
        self.filedir = 'http://webensino.unicamp.br/cursos'

        self.relista = open("regex_strings.txt", "r").readlines()
        self.urls = open("urls.txt", "r").readlines()
        self.payload = {
            'user': '155606',
            'pass': "log2!Day4:20!",
            'btnTeleduc': 'submit'  # remember me
        }
        self.payload2 = {'enviaA': 'disciplinas', 'enviaB': '', 'enviaC': ''}
        self.dis_name = []
        self.dict_link = {}
        self.dict_doc = {}
        self.material = {}
        self.topic_links = {}
        self.docnames_links = {}
        self.topic_url = []
        self.distopic = {}

        self.session = requests.Session
        self.log = None

        # self.matching_text()

    def check_connection(self):
        opens = self.session()
        url = "https://www.google.com.br"
        timeout = 5
        try:
            _ = requests.get(url, timeout=timeout)
            opens.close()
            return True

        except requests.ConnectionError:
            opens.close()
            return False

    def init_scrapper(self):
        self.urls = [string.replace("\n", "") for string in self.urls]
        self.relista = [string.replace("\n", "") for string in self.relista]
        return self.check_auth()

    def check_auth(self):
        self.log = self.session()
        logged = self.log.post(self.login_url, data=self.payload)

        return dict(response=logged, logger=self.log)

    def matching_disc(self):
        ativas_page = (self.log.post(self.baseurl, data=self.payload2)).text
        get_ativas = re.findall(r"&cod_curso=[0-9]*", ativas_page, re.MULTILINE)
        if get_ativas:
            for disciplina in get_ativas:
                self.match_topicos(disciplina)

            # print(self.material['BA480A - Anatomia Humana Geral'])
        else:
            print("No such pattern")

    def match_topicos(self, disciplina):
        material_apoio = self.log.get(self.urls[2] + 'material.php?' + disciplina + '&cod_ferramenta=4')
        doc_name = []

        if str(material_apoio) == self.get_aprovado:
            for name in re.findall(r"(?=[A-Z]{2})(.*)(?=</nobr)", material_apoio.text, re.MULTILINE):
                if name:
                    self.dis_name.append(name)
                    sub_pasta = re.findall(r"(?=material.php)(.*?)(?=\"><img src=../figuras)", material_apoio.text,
                                           re.MULTILINE)
                    if sub_pasta:
                        for pasta in sub_pasta:
                            pasta = self.log.get(self.urls[2] + pasta)
                            match_topico = re.findall(r"(?=ver.php)(.*?)(?=\"><)", pasta.text, re.MULTILINE)
                            self.distopic.update({name: match_topico})
                            if match_topico:
                                self.matching(name, doc_name, material_apoio, match_topico)
                    else:
                        match_topico = []
                        self.matching(name, doc_name, material_apoio, match_topico)
                else:
                    print("Disciplina Inexistente")

    def matching(self, name, doc_name, material_apoio, match_topico):
        if match_topico:
            for topico in match_topico:
                self.topic_url.append(topico)
                self.list_pdf(topico, name, doc_name)
            self.distopic.update({name: match_topico})
        else:
            match_topico = re.findall(r"(?=cod_curso)(.*)(?=\"><img src=../figuras/arqp.gif)", material_apoio.text,
                                      re.MULTILINE)
            for topico in match_topico:
                self.topic_url.append(topico)
                self.list_pdf(topico, name, doc_name)
            self.distopic.update({name: match_topico})

        # topicurl_get = self.log.get(topic_url[0])
        # print(topicurl_get.text)
        topicos_lista = []
        if match_topico:
            # print(match_topico)
            for topico in match_topico:
                self.topic_url.append(topico)
                self.list_pdf(topico, name, doc_name)
                # topicos_lista.append(match_topico[topico])
            for topic in self.topic_url:
                self.material.update({topic: self.topic_url})

        else:
            print("Sem Materiais Disponíveis")

    def list_pdf(self, topico, name, doc_name):
        pdf_html = self.log.get(self.urls[2] + 'ver.php?' + topico)
        links = []
        if str(pdf_html) == self.get_aprovado:
            for doc in re.findall(r"/\w*/\w*///.+?(?=\s)", pdf_html.text, re.MULTILINE):
                # resex = re.findall(r"/\w*/\w*///.+?(?=\s)", pdf_html.text, re.MULTILINE)
                links.append(doc)
                self.topic_links.update({topico: links})
            for docs in re.findall(r"(?<=/{3})(.*?)(?=\s)", pdf_html.text, re.MULTILINE):
                replace = (docs.replace("%20", " "))
                doc_name.append(replace)
                self.dict_doc.update({name: doc_name})
            for docname in doc_name:
                for link in links:
                    # print(docname+" " +link)
                    self.docnames_links.update({docname: link})
                    # self.docnames_links.update({docname:links.index[doc_name[docindex]]})
            self.dict_link.update({name: links})


if __name__ == "__main__":
    Methods(None, None)
