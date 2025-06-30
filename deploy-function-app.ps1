# Variables
$resourceGroup = "v-asen-Mindtree"
$location = "Australia East"
$storageAccount = "vasenmindtreeb4e2"
$functionApp = "arkofuncapp"

# Login to Azure
az login

# Create Storage Account
az storage account create --name $storageAccount --location $location --resource-group $resourceGroup --sku Standard_LRS

# Create Function App
az functionapp create --resource-group $resourceGroup --consumption-plan-location $location --runtime python --runtime-version 3.9 --functions-version 3 --name $functionApp --storage-account $storageAccount

# Deploy Function App
func azure functionapp publish $functionApp
