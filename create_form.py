import os.path
import pickle
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/drive']

def authenticate_google_api():
    """Authenticate the user and return valid Google API credentials."""
    creds = None
    token_path = 'google_credentials/token.json'
    
    # Check if the token.json file exists
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If no valid credentials, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('google_credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=63813)

        # Save the credentials for the next run
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    return creds

def create_google_form(quiz_data):
    """Creates a Google Form and populates it with quiz data."""
    creds = authenticate_google_api()
    service = build('forms', 'v1', credentials=creds)

    # Step 1: Create the form with only the title
    form_body = {
        "info": {
            "title": "Quiz",
            "documentTitle": "Generated Quiz",
        }
    }

    form = service.forms().create(body=form_body).execute()
    form_id = form['formId']

    # Step 2: Use batchUpdate to add questions to the form
    requests = []
    for question in quiz_data:
        requests.append({
            "createItem": {
                "item": {
                    "title": question["question"],
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": question["option_a"]},
                                    {"value": question["option_b"]},
                                    {"value": question["option_c"]},
                                    {"value": question["option_d"]}
                                ],
                                "shuffle": False
                            }
                        }
                    }
                },
                "location": {
                    "index": 0
                }
            }
        })

    # Send batchUpdate request
    batch_update_body = {
        "requests": requests
    }

    service.forms().batchUpdate(formId=form_id, body=batch_update_body).execute()

    # Get form URL
    form_url = f"https://docs.google.com/forms/d/{form_id}/edit"
    print(f"Form created: {form_url}")
    return form_url
