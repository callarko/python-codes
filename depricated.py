from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from kubernetes import client, config
import json

# Initialize Azure credentials and AKS client
credential = DefaultAzureCredential()
subscription_id = "20df4f6c-0ab2-4a88-82d5-9d23dbddfc7d"
resource_group_name = "arkorg"
cluster_name = "arkoaks"

aks_client = ContainerServiceClient(credential, subscription_id)

# Get the AKS cluster
aks_cluster = aks_client.managed_clusters.get(resource_group_name, cluster_name)

# Get Kubernetes configuration from AKS cluster
config.load_kube_config()

# Initialize Kubernetes client
k8s_client = client.ApiClient()
discovery_client = client.DiscoveryV1Api(k8s_client)

# List all API groups and versions
api_groups = discovery_client.get_api_groups()

deprecated_apis = []

# Check each API group and version for deprecation
for group in api_groups.groups:
    for version in group.versions:
        group_version = f"{group.name}/{version.version}" if group.name else version.version
        try:
            resources = discovery_client.get_api_resources(group_version=group_version)
            for resource in resources.resources:
                if hasattr(resource, 'deprecated') and resource.deprecated:
                    deprecated_apis.append({
                        'group': group.name,
                        'version': version.version,
                        'resource': resource.name
                    })
        except client.exceptions.ApiException as e:
            print(f"Error fetching resources for {group_version}: {e}")

print(json.dumps(deprecated_apis, indent=2))
