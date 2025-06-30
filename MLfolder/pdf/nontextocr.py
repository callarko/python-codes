from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# Set up OCR credentials for Computer Vision
ocr_endpoint = "https://arkoocrresource.cognitiveservices.azure.com/"
ocr_key = "1796cb1e74df4439b57fdea1c6ac3ed0"  # Replace with your key

# Create Computer Vision client
computervision_client = ComputerVisionClient(ocr_endpoint, CognitiveServicesCredentials(ocr_key))

# Open the local PDF file
with open("local_copy.pdf", "rb") as pdf_file:
    read_response = computervision_client.read_in_stream(pdf_file, raw=True)

# Extract the operation ID from the response
operation_location = read_response.headers["Operation-Location"]
operation_id = operation_location.split("/")[-1]

# Wait for the operation to complete
while True:
    result = computervision_client.get_read_result(operation_id)
    if result.status not in ['notStarted', 'running']:
        break

# Extract and print the text
if result.status == OperationStatusCodes.succeeded:
    for page in result.analyze_result.read_results:
        for line in page.lines:
            print(line.text)
