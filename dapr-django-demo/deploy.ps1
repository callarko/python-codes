# Variables
$resourceGroup="arkorg"
$location="japaneast"
$envName="dapr-env"
$acrName="djangodapracr$(Get-Random -Maximum 9999)"
$acrLoginServer="$acrName.azurecr.io"

# Create ACR
az acr create -n $acrName -g $resourceGroup --sku Basic --admin-enabled true --location eastus

# Build and push service-a image
az acr build --registry $acrName --image service-a:latest .

# Build and push service-b image
az acr build --registry $acrName --image service-b:latest .

# Get ACR credentials
$acrCreds = az acr credential show -n $acrName --query "{username: username, password: passwords[0].value}" -o json | ConvertFrom-Json
$acrUser = $acrCreds.username
$acrPass = $acrCreds.password

# Create Container App Environment with Dapr enabled
az containerapp env create `
  --name $envName `
  --resource-group $resourceGroup `
  --location $location

# Deploy service-a
az containerapp create `
  --name service-a `
  --resource-group $resourceGroup `
  --environment $envName `
  --image "$acrLoginServer/service-a:latest" `
  --target-port 8000 `
  --ingress internal `
  --registry-server $acrLoginServer `
  --registry-username $acrUser `
  --registry-password $acrPass `
  --enable-dapr `
  --dapr-app-id service-a `
  --dapr-app-port 8000

# Deploy service-b
az containerapp create `
  --name service-b `
  --resource-group $resourceGroup `
  --environment $envName `
  --image "$acrLoginServer/service-b:latest" `
  --target-port 8000 `
  --ingress internal `
  --registry-server $acrLoginServer `
  --registry-username $acrUser `
  --registry-password $acrPass `
  --enable-dapr `
  --dapr-app-id service-b `
  --dapr-app-port 8000
