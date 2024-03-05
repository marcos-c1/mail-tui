import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError 

# If modifying these scopes, delete the file token.json.
SCOPES = {
  'messages-read-only': "https://www.googleapis.com/auth/gmail.readonly",
  'messages-crud': "https://mail.google.com/",
}

class Service:
  
    def __init__(self, scope=''):
        self.creds = None
        if scope:
            self.store_or_retrieve_creds(scope)
        else:
            self.store_or_retrieve_creds(SCOPES['messages-crud'])
    
    def store_or_retrieve_creds(self, scope=str):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
          self.creds = Credentials.from_authorized_user_file("token.json", scope)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
              self.creds.refresh(Request())
            else:
              flow = InstalledAppFlow.from_client_secrets_file(
                  "credentials.json", scope
              )
            self.creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
          token.write(self.creds.to_json())

    def list_user_gmail_labels(self):
        """
        Lists the user's Gmail labels.
        """
        try:
            service = build("gmail", "v1", credentials=self.creds)
            results = service.users().labels().list(userId="me").execute()
            labels = results.get("labels", [])

            if not labels:
                print("No labels found.")
                return
            print("Labels:")
            for label in labels:
                print(label["name"])

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def get_user_id_messages(self):
        """
        Lists the user's Gmail's message.
        """

        try:
            # Call the Gmail API
            service = build("gmail", "v1", credentials=self.creds)
            results = service.users().messages().list(userId="me").execute()
            messages = results.get("messages", [])

            if not messages:
                print("No messages found.")
                return
            return messages

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def get_message_info(self, messages=list | str):
        if len(messages) > 0:
            if type(messages) == list:
                for msg in messages:
                    id = msg['id']
                    try:
                        # Call the Gmail API
                        service = build("gmail", "v1", credentials=self.creds)
                        # Returns a dictionary
                        results = service.users().messages().get(userId="me", id=id).execute()
                        print(results.keys())
                        break
                        if not messages:
                            print("No messages found.")
                            return

                    except HttpError as error:
                        # TODO(developer) - Handle errors from gmail API.
                        print(f"An error occurred: {error}")

            else:
                try:
                    # Call the Gmail API
                    service = build("gmail", "v1", credentials=self.creds)
                    results = service.users().messages(id=msg['id']).get(userId="me").execute()
                    messages = results.get("messages", [])
                    print(messages)
                                                                                            
                    if not messages:
                        print("No messages found.")
                        return
                                                                                                
                except HttpError as error:
                    # TODO(developer) - Handle errors from gmail API.
                    print(f"An error occurred: {error}")

    def get_profile_info(self):
        try:
            service = build("gmail", "v1", credentials=self.creds)
            results = service.users().getProfile(userId="me").execute()
            print(results.keys())
        except HttpError as error:
            print(f"An error ocurred: {error}")

if __name__ == "__main__":
  s = Service(SCOPES["messages-crud"])
  #msgs = s.get_user_id_messages()
  #s.get_message_info(messages=msgs)
  s.get_profile_info()
  
