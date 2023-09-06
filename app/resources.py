from flask_restx import Resource, Namespace
from .api_models import process_request_model
from .process_request_handler import hasInvalidProcess, mountAllUrls, retrieveProcesses
from .configs import config_processos
import time
ns = Namespace("api")


@ns.route("/processos")
class GetProcessos(Resource):

    @ns.expect(process_request_model)
    def post(self):
        if "process_numbers" not in ns.payload:
            return {"msg": "Você precisa enviar o número do processo (process_numbers)"}, 400
        processos = ns.payload["process_numbers"].split(',')
        if len(processos) > config_processos['qtd_maxima_processos']:
            return {"msg": "Quantidade máxima de processos por requisições é "+str(config_processos['qtd_maxima_processos'])}, 400
        if hasInvalidProcess(processos):
            return {"msg": "Processo inválido (tribunal inválido). Tribunais aceitos: "+", ".join(config_processos['nome_tribunais'])}, 400
        url_processos = mountAllUrls(processos)
        response = retrieveProcesses(url_processos)
        return {"processos": response}, 200