import msal
import requests
import json
import os

# Replace these values with your app's details
client_id = os.envron['cli']
authority = f"https://login.microsoftonline.com/common"
scope = ["Mail.Read"]

app = msal.PublicClientApplication(client_id, authority=authority)

def get_initial_tokens():
    # Initiate the device code flow
    flow = app.initiate_device_flow(scopes=scope)
    if "user_code" not in flow:
        raise ValueError("Failed to create device flow. Error: %s" % json.dumps(flow, indent=4))

    # Print the device code message for the user to authenticate
    print(flow["message"])

    # Poll until we have a token or an error
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        print("wooooooooooo")
        return result["access_token"], result["refresh_token"]
    else:
        raise ValueError("Failed to obtain access token. Error: %s" % result.get("error"))

access, refresh = get_initial_tokens()
print(f"access: {access}")
print()
print(f"refresh: {refresh}")
