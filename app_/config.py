ENVIRONMENT = "local"
if ENVIRONMENT == "local":
    API_URL = "http://localhost:8000"
else:
    API_URL = "https://cdyt75xvdl.execute-api.us-east-1.amazonaws.com/agents"
