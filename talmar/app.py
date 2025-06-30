from fastapi import FastAPI, Request
from cryptography import x509
from cryptography.hazmat.primitives import serialization
import base64

app = FastAPI()

@app.get("/")
async def validate_cert(request: Request):
    cert_header = request.headers.get("X-ARR-ClientCert")
    if not cert_header:
        return {"message": "Client certificate not found"}

    try:
        cert_bytes = base64.b64decode(cert_header)
        cert = x509.load_pem_x509_certificate(cert_bytes)
        return {"subject": cert.subject.rfc4514_string(), "issuer": cert.issuer.rfc4514_string()}
    except Exception as e:
        return {"error": str(e)}
