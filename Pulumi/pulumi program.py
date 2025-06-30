import pulumi
from pulumi_azure_native import resources, containerservice, network

config = pulumi.Config()
prefix = "cluster1"
location = "eastus"
kubernetes_version = "1.29.7"
node_vm_size = "Standard_D4ds_v4"
number_of_nodes = 2
max_nodes = 5

# Create a resource group
rg = resources.ResourceGroup(f"{prefix}-rg", resource_group_name="arkorg", location=location)

# Create a virtual network
vnet = network.VirtualNetwork(
    f"{prefix}-vnet",
    resource_group_name=rg.name,
    location=rg.location,
    address_space={
        "address_prefixes": ["10.0.0.0/16"],
    },
    tags={
        "Environment": "Dev/Test",
        "Project": "AKS Deployment",
    },
)

# Create a subnet
subnet = network.Subnet(
    f"{prefix}-subnet",
    resource_group_name=rg.name,
    virtual_network_name=vnet.name,
    address_prefixes=["10.0.0.0/22"],
    service_endpoints=[
        {"service": "Microsoft.Storage"},
        {"service": "Microsoft.KeyVault"},
    ],
)

# Create AKS Cluster
aks = containerservice.ManagedCluster(
    f"{prefix}-aks",
    resource_group_name=rg.name,
    kubernetes_version=kubernetes_version,
    dns_prefix=prefix,
    agent_pool_profiles=[
        containerservice.ManagedClusterAgentPoolProfileArgs(
            name="agentpool",
            count=number_of_nodes,
            vm_size=node_vm_size,
            os_type=containerservice.OSType.LINUX,
            enable_node_public_ip=False,
            type=containerservice.AgentPoolType.VIRTUAL_MACHINE_SCALE_SETS,
            mode=containerservice.AgentPoolMode.SYSTEM,
            enable_auto_scaling=True,
            min_count=number_of_nodes,
            max_count=max_nodes,
            os_disk_size_gb=64,
            os_disk_type="Managed",
            vnet_subnet_id=subnet.id,
            availability_zones=["1", "2", "3"],
            max_pods=110,
        )
    ],
    identity={"type": "SystemAssigned"},
    enable_rbac=True,
    network_profile={
        "network_plugin": "azure",
        "network_policy": None,  # No network policy (allow all ingress and egress)
        "load_balancer_sku": "standard",
        "serviceCidr": "10.1.0.0/16",
        "dnsServiceIP": "10.1.0.10",
        "network_mode": "transparent",
        "outboundType": "loadBalancer",
    },
    sku=containerservice.ManagedClusterSKUArgs(
        name="Standard",
        tier="Standard",
    ),
    auto_upgrade_profile=containerservice.ManagedClusterAutoUpgradeProfileArgs(
        upgrade_channel="None"
    ),
    node_os_upgrade_channel="NodeImage",
    tags={
        "Environment": "Dev/Test",
        "Project": "AKS Deployment",
        "Owner": "Rapidevisa",
    },
)

pulumi.export("cluster_name", aks.name)
pulumi.export("resource_group_name", rg.name)
