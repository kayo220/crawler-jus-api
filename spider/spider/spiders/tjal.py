import scrapy
import json

class TjalSpider(scrapy.Spider):
    name = "tjal"
    allowed_domains = ["www2.tjal.jus.br", "esaj.tjce.jus.br"]
    # start_urls = ["https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=0710802-55.2018&foroNumeroUnificado=0001&dePesquisaNuUnificado=0710802-55.2018.8.02.0001&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"]
    def __init__(self, *args, **kwargs):
        super(TjalSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',')

    def parse(self, response):
        #Define the comands for xpath from grau1 and grau2
        comandos = {
            "grau1":{
                "classe": "//*[@id='classeProcesso']/text()",
                "valor_acao": "//*[@id='valorAcaoProcesso']/text()",
                "vara": "//*[@id='varaProcesso']/text()",
                "juiz": "//*[@id='juizProcesso']/text()",
                "assunto": "//*[@id='assuntoProcesso']/text()",
                "foro": "//*[@id='foroProcesso']/text()",
                "partes_processo": "//*[@id='tablePartesPrincipais']//*[@class='fundoClaro']"
            },
            "grau2":{
                "classe": "//*[@id='classeProcesso']/span/text()",
                "valor_acao": "//*[@id='valorAcaoProcesso']/span/text()",
                "vara": "//tr[@class='fundoClaro']/td[3]/text()",
                "juiz":"//tr[@class='fundoClaro']/td[4]/text()",
                "assunto": "//*[@id='assuntoProcesso']/span/text()",
                "foro":"//tr[@class='fundoClaro']/td[2]/text()",
                "partes_processo": "//*[@id='tableTodasPartes' or @id='tablePartesPrincipais']//*[contains(@class, 'fundoClaro')]"
            }
        }
        #Defines if is grau1 or grau2
        if "cposg5" in response.request.url:
            grau = "grau2"
        else:
            grau = "grau1"

        area = response.xpath("//*[@id='areaProcesso']/span/text()")
        if area == []:
            area = ''
        else:
            area = area.get().strip()

        processos = [] #should be empty unless is a grau2 process with multiple processes
        processos = response.xpath("//*[@class='custom-radio']/@value")
        if grau == "grau2" and "processo.codigo" not in response.request.url and processos != []:
                processos = processos.getall()
                if(len(processos) >= 1):
                    url_aux = response.request.url.split('/cposg5')
                    for processo in processos: 
                        yield response.follow(url = url_aux[0]+"/cposg5/show.do?processo.codigo="+processo, callback=self.parse)

        classe = response.xpath(comandos[grau]['classe'])
        if classe == []:
            classe = ''
        else:
            classe = classe.get().strip()

        data_distribuicao = response.xpath("//*[@id='dataHoraDistribuicaoProcesso']/text()")
        if data_distribuicao == []:
            data_distribuicao = ''
        else:
            data_distribuicao = data_distribuicao.get().strip().replace('\n', '')
        
        valor_acao = response.xpath("//*[@id='valorAcaoProcesso']/text()")
        if valor_acao == [] :
            valor_acao = ''
        else:
            valor_acao = valor_acao.get().strip().split()[-1]

        assunto = response.xpath(comandos[grau]["assunto"])
        if assunto == [] : 
            assunto = ''
        else:
            assunto = assunto.get().strip()

        foro = response.xpath(comandos[grau]["foro"])
        if foro == []:
            foro = ''
        else:
            foro = foro.get().strip()

        vara = response.xpath(comandos[grau]["vara"])
        if vara == []:
            vara = ''
        else:
            vara = vara.get().strip()

        juiz = response.xpath(comandos[grau]["juiz"])
        if juiz == []:
            juiz = ''
        else:
            juiz = juiz.get().strip()

        partes_processo =  response.xpath(comandos[grau]["partes_processo"])
        partes_processo_final = []
        for parte_processo in partes_processo:
            partes_processo_aux = {}
            parte = parte_processo.xpath("./td[1]/span/text()").extract_first().strip()
            pessoas = parte_processo.xpath("./td[2]/text()[not(normalize-space() = '')]").getall()
            tipo = parte_processo.xpath("./td[2]/span/text()").getall()
            pessoas = list(map(str.strip, pessoas))
            pessoas = list(filter(None, pessoas))
            qtd_pessoas = len(pessoas)
            qtd_tipo = len(tipo)
            for i in range (0, qtd_pessoas-qtd_tipo):
                tipo.insert(0,'')
            for i in range(0, len(pessoas)):
                pessoas[i] = tipo[i].strip().replace("&nbsp","") + pessoas[i]
            partes_processo_aux[parte] = pessoas
            partes_processo_final.append(partes_processo_aux)
        datas_movimentacao = response.xpath("//*[@class='dataMovimentacao']/text()").extract()
        datas_movimentacao = ', '.join(list(map(str.strip, datas_movimentacao)))
        todas_movimentacoes = response.xpath("//tbody[@id='tabelaTodasMovimentacoes']/tr")
        movimentacoes_final = []
        for movivimentacao in todas_movimentacoes:
            movimentacoes = {}
            data = movivimentacao.xpath(".//td[1]/text()").extract_first().strip();
            descricoes = movivimentacao.xpath(".//td[3]/node()/text()").extract()
            if(len(descricoes) == 1 and descricoes[0].strip() == ''):
                descricoes = movivimentacao.xpath(".//td[3]/text()").extract()
            else: 
                descricoes = movivimentacao.xpath(".//td[3]//text()").extract()
                descricoes = list(map(str.strip, descricoes))#clear empty spaces in each string element
                descricoes = list(filter(None, descricoes))#clear empty elements
                if(len(descricoes) == 3):
                    descricoes[2] = "Vencimento: " + descricoes[2]
            for i in range(0, len(descricoes)):
                descricoes[i] = descricoes[i].strip();
                descricoes[i] = descricoes[i].replace('\r\n', ' ')
            descricoes = list(filter(None, descricoes))
            movimentacoes[data] = " ".join(descricoes)
            movimentacoes_final.append(movimentacoes)
        data = None
        if classe!='' or area != '' or data_distribuicao!='':#if process is valid and has informations
            data = {
                "classe": classe,
                "area":area,
                "assunto": assunto,
                "data_distribuicao":data_distribuicao,
                "juiz": juiz,
                "valor_acao": valor_acao,
                "partes_do_processo": partes_processo_final,
                "movimentacoes": movimentacoes_final,
            }
        yield data