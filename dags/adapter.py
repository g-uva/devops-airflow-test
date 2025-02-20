from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import requests
import json

class FissionOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 fission_function_name,
                 container_image,
                 command=None,
                 environment_name=None,  # Optional: Specify a Fission environment
                 fission_url="http://fission-controller:8080", # Your Fission controller URL
                 *args, **kwargs):
        super(FissionOperator, self).__init__(*args, **kwargs)
        self.fission_function_name = fission_function_name
        self.container_image = container_image
        self.command = command
        self.environment_name = environment_name
        self.fission_url = fission_url

    def execute(self, context):
        payload = {
            "name": self.fission_function_name,  # Or a dynamically generated name
            "env": {
                "image": self.container_image
            },
            "code": {  # If you're providing code directly (less common for containers)
                "function": "" # Leave empty for container images
            },
            "resources": { # Resource requests if needed
                "limits": {
                    "cpu": "100m",
                    "memory": "128Mi"
                }
            }

        }

        if self.command:
            payload["env"]["command"] = self.command

        if self.environment_name:
          payload["env"]["environment"] = self.environment_name

        # 1. Check if the function exists. If not, create it
        function_url = f"{self.fission_url}/v2/functions/{self.fission_function_name}"
        try:
            requests.get(function_url) # Check if function exists
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                # Create the function
                create_response = requests.post(f"{self.fission_url}/v2/functions", json=payload)
                create_response.raise_for_status() # Raise exception for bad status codes
                self.log.info(f"Fission function '{self.fission_function_name}' created.")
            else:
                raise e

        # 2. Trigger function execution
        invoke_url = f"{self.fission_url}/v2/functions/{self.fission_function_name}"

        invoke_response = requests.post(invoke_url, json={}) # Empty JSON for now, can pass input here

        invoke_response.raise_for_status()
        self.log.info(f"Fission function '{self.fission_function_name}' triggered.")

        # 3. Get the invocation ID (if needed for asynchronous execution)
        invocation_id = invoke_response.json().get("invocationId") # If Fission returns it

        # 4. (Optional) For asynchronous operations, you might need to poll for the result
        #    using the invocation ID.

        # ... (Implementation for polling and result retrieval)

        return "Fission function executed." # Or return the invocation ID or result