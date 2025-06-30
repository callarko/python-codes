import json
import azure.functions as func
import azure.durable_functions as DurableFunc
from app.main import app as fastapi_app

app = func.AsgiFunctionApp(app=fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
myApp = DurableFunc.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@myApp.route("orchestrators/{functionName}")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    function_name = req.route_params.get('functionName')
    if req.get_body():
        request_body = json.loads(req.get_body().decode())
    else:
        request_body = None

    instance_id = await client.start_new(function_name, client_input=request_body)
    response = client.create_check_status_response(req, instance_id)
    return response
