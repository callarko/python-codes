import azure.functions as func
import logging
from datetime import datetime

# Configure logging globally with custom format
logging.basicConfig(level=logging.INFO)

app = func.FunctionApp()

@app.route(route="HttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def HttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    # Include a UTC timestamp in every log
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    logging.info(f"{timestamp} - Processing a new request.")

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        logging.info(f"{timestamp} - Successfully processed request for name: {name}.")
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully."
        )
    else:
        logging.warning(f"{timestamp} - No name provided in the query string or request body.")
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
