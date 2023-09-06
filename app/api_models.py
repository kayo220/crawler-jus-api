from flask_restx import fields
from .extensions import api
process_request_model = api.model("GetProcess", {"process_numbers": fields.String(description="String contendo a lista dos projetos, separados por vírgula", example="0710802-55.2018.8.02.0001,0070337-91.2008.8.06.0001", required=True)})