import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.batch import BatchServiceClient
from msrest.authentication import BasicTokenAuthentication

app = func.FunctionApp()

@app.function_name(name="BatchTrigger")
@app.route(route="batch")
def batch_auth_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://batch.core.windows.net/.default")
        logging.info(f"🪪 AAD Token Acquired: {token.token[:40]}...")

        token_auth = BasicTokenAuthentication({"access_token": token.token})
        batch_client = BatchServiceClient(
            credentials=token_auth,
            batch_url="https://arkbatchaccount.centralindia.batch.azure.com"
        )

        # Call something harmless
        pools = list(batch_client.pool.list())
        pool_names = [p.id for p in pools]

        return func.HttpResponse(f"✅ Connected! Pools: {pool_names}")

    except Exception as e:
        logging.error(f"❌ Exception: {str(e)}")
        return func.HttpResponse(f"❌ ERROR: {str(e)}", status_code=500)
