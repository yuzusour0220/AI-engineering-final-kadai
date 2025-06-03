# Use the native inference API to send a text message to Amazon Titan Text G1 - Express.

import boto3
import json

from botocore.exceptions import ClientError


# Create a session using the specific SSO profile
session = boto3.Session(profile_name="Student-646962881826")

# Create an Amazon Bedrock Runtime client from the session
brt = session.client("bedrock-runtime", region_name="ap-northeast-1")
# Create an Amazon Bedrock Runtime client.


# Set the model ID, e.g., Amazon Titan Text G1 - Express.
model_id = "amazon.titan-text-express-v1"

# Define the prompt for the model.
prompt = "Describe the purpose of a 'hello world' program in one line."

# Format the request payload using the model's native structure.
native_request = {
    "inputText": prompt,
    "textGenerationConfig": {"maxTokenCount": 512, "temperature": 0.5, "topP": 0.9},
}

# Convert the native request to JSON.
request = json.dumps(native_request)

try:
    # Invoke the model with the request.
    response = brt.invoke_model(modelId=model_id, body=request)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

# Decode the response body.
model_response = json.loads(response["body"].read())

# Extract and print the response text.
response_text = model_response["results"][0]["outputText"]
print(response_text)
