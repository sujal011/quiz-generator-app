# google_forms.py

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth import get_credentials

def create_google_form(title, description):
    creds = get_credentials()
    try:
        service = build('forms', 'v1', credentials=creds)
        form = {
            "info": {
                "title": title,
                "description": description
            }
        }
        created_form = service.forms().create(body=form).execute()
        return created_form['formId']
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def add_multiple_choice_question(form_id, question, options, correct_option=None):
    creds = get_credentials()
    try:
        service = build('forms', 'v1', credentials=creds)
        requests = [
            {
                "createItem": {
                    "item": {
                        "title": question,
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [{"value": opt} for opt in options],
                                    "shuffle": False
                                }
                            }
                        }
                    },
                    "location": {
                        "index": "0"  # Adds to the top; adjust as needed
                    }
                }
            }
        ]
        service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")

def get_form_url(form_id):
    return f"https://docs.google.com/forms/d/{form_id}/edit"
