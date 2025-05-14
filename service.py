from foundry_local import FoundryLocalManager

# By using an alias, the most suitable model will be selected 
# to your end-user's device.
alias = "deepseek-r1-1.5b"

# Create a FoundryLocalManager instance. This will start the Foundry.
manager = FoundryLocalManager()

service_info = manager.get_service_info()
print(f"Service info: {service_info}")

# List available models in the catalog
catalog = manager.list_catalog_models()
print(f"Available models in the catalog: {catalog}")

# Download and load a model
model_info = manager.download_model(alias)
model_info = manager.load_model(alias)
print(f"Model info: {model_info}")

# List models in cache
local_models = manager.list_local_models()
print(f"Models in cache: {local_models}")

# List loaded models
loaded = manager.list_loaded_models()
print(f"Models running in the service: {loaded}")

# Unload a model
manager.unload_model(alias)
