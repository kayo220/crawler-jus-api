from .configs import config_processos
import subprocess
import json
import time
import uuid
import os

#Return true if one of process does not contains a valid tribunal
def hasInvalidProcess(processos):
    for processo in processos:
        processo_valido = False
        for tribunal in config_processos['tribunais']:
            if tribunal in processo:
                processo_valido = True
                break
        if processo_valido == False:
            return True
    return False

#Return the tribunal of a processo
def getCodigoTribunal(processo):
    for tribunal in config_processos['tribunais']:
        if tribunal in processo:
            return tribunal
        
#Return the URLs of a processo
def mountProcessUrl(processo):
    tribunal = getCodigoTribunal(processo)
    urls = [config_processos['url_tribunais'][tribunal]['grau1']+'?processo.numero='+processo,
            config_processos['url_tribunais'][tribunal]['grau2']+'?cbPesquisa=NUMPROC&dePesquisaNuUnificado='+processo+'&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO']
    return urls

#Mount all the processos with the 1grau and 2grau URL
def mountAllUrls(processos):
    processos_url = []
    for processo in processos:
        urls = mountProcessUrl(processo)
        processos_url.append({"processo":processo, "urls": urls})
    return processos_url
    
#Read the json file with a retry strategy
def read_file(file_name, retry):
    try:
        f = open(file_name, encoding='utf-8')
        data = json.load(f)
        return data
    except Exception as Error: 
        if(retry ==  20):
            return "Erro ao carregar processo"
        time.sleep(0.3)
        return read_file(file_name, retry+1)

#Starts the crawler and mounts the response payload
def retrieveProcesses(processos):
    dir = os.getcwd()+"/spider/spider/spiders"
    for processo in processos:
        processo['filename'] = str(uuid.uuid1())+'.json'
        subprocess.Popen(['scrapy', 'crawl', 'tjal', '-a','start_urls='+','.join(processo['urls']), '--nolog', '-o', processo['filename']], cwd=dir)
    for processo in processos:
        output = read_file(dir+'/'+processo['filename'], 0)
        if output != "Erro ao carregar processo":
            processo['result']={"grau1": [output[0]], "grau2": output[1:]}
        else:
            processo['result']={"Erro": "Falha ao buscar processo!"}
    for processo in processos:
        subprocess.run(['rm', '-f', processo['filename']], cwd=dir, stdout=subprocess.PIPE)
        del processo['filename']
    return processos
