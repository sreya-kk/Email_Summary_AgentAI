import os
import pickle
import datetime
import openai
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API Key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the scope (read-only access to Gmail)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate with Gmail using OAuth 2.0 and return credentials."""
    creds = None

    # Check if token.pickle exists (to avoid re-authentication)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or invalid, log in again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES
            )
            creds = flow.run_local_server(port=8501)

        # Save credentials for next time
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def fetch_previous_day_emails():
    """Fetch all emails from the previous day."""
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    # Get the date range for yesterday
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y/%m/%d')
    today = datetime.datetime.now().strftime('%Y/%m/%d')

    # Gmail search query to get all emails from the previous day
    query = f"after:{yesterday} before:{today}"

    # Fetch messages matching the query
    results = service.users().messages().list(userId='me', q=query, maxResults=50).execute()
    messages = results.get('messages', [])

    email_data = []
    if not messages:
        print("No emails found from the previous day.")
        return email_data

    for msg in messages:
        msg_id = msg['id']
        msg_details = service.users().messages().get(userId='me', id=msg_id).execute()
        headers = msg_details['payload']['headers']
        
        email_info = {
            "id": msg_id,
            "from": next((h['value'] for h in headers if h['name'] == 'From'), "Unknown"),
            "subject": next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject"),
            "snippet": msg_details.get('snippet', "No preview available"),
        }
        email_data.append(email_info)

    return email_data

def summarize_emails(emails):
    """Summarize the fetched emails using GPT-4."""
    if not emails:
        return "No emails to summarize."

    openai.api_key = OPENAI_API_KEY

    email_text = "\n\n".join([f"From: {email['from']}\nSubject: {email['subject']}\nSnippet: {email['snippet']}" for email in emails])

    prompt = f"""
    You are an AI assistant.Identify top 10 urgent and important emails separately. Summarize the following emails into key takeaways. Based on the email body, subject and sender info. Avoid spams, ads and random app notifications.
    :
    
    {email_text}

    Provide a short summary with priority ranking.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI assistant.Identify top 10 urgent and important emails separately. Summarize the following emails into key takeaways. Based on the email body, subject and sender info. Avoid spams, ads and random app notifications."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message
    except Exception as e:
        return f"Error generating summary: {str(e)}"

if __name__ == "__main__":
    emails = fetch_previous_day_emails()
    summary = summarize_emails(emails)
    print("\n### EMAIL SUMMARY ###\n")
    print(summary)
