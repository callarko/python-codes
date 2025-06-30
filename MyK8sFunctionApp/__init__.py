import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from kubernetes import client, config

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Hardcode pod name and namespace for testing
        pod_name = 'nginx'  # Your pod name
        namespace = 'default'  # Namespace where the pod is running

        # Set the AKS API server URL
        aks_api_server = 'https://myakscluster-dns-ieevn5ni.hcp.eastus.azmk8s.io'
        
        # Get token using managed identity
        credential = DefaultAzureCredential()
        token = credential.get_token("https://management.azure.com/.default").token

        # Kubernetes client configuration
        configuration = client.Configuration()
        configuration.host = aks_api_server
        configuration.verify_ssl = True
        configuration.api_key = {"authorization": f"Bearer {token}"}
        
        # Create Kubernetes API client
        k8s_client = client.CoreV1Api(client.ApiClient(configuration))

        # Log the attempt to restart the pod
        logging.info(f"Attempting to restart pod {pod_name} in namespace {namespace}.")

        # Restart pod by deleting it
        k8s_client.delete_namespaced_pod(pod_name, namespace, body=client.V1DeleteOptions())

        return func.HttpResponse(
            f"Pod {pod_name} in namespace {namespace} has been restarted.",
            status_code=200
        )
    except client.ApiException as e:
        logging.error(f"Exception when calling CoreV1Api->delete_namespaced_pod: {e}")
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=e.status
        )
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
