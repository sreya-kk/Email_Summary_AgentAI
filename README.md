AI-Powered Email Summarizer
An AI-driven agent that fetches, summarizes, and prioritizes emails from the previous day using GPT-4.


Fetches emails from Gmail using OAuth 2.0
Uses GPT-4 to summarize and rank emails by priority
Displays top 10 emails in an interactive Streamlit UI
Secure API key management with .env file


Setup & Installation
1. Clone the Repository


git clone https://github.com/sreya-kk/Email_Summary_AgentAI.git
cd Email_Summary_AgentAI


2. Install Dependencies


pip install -r requirements.txt


3. Set Up Gmail API
Enable Gmail API in Google Cloud Console.
Download client_secret.json and place it in the project folder.
Authenticate using:


python gmail_auth.py


4. Secure Your OpenAI API Key
Create a .env file:


touch .env
Add:
ini


OPENAI_API_KEY=your-api-key-here


5. Run the Streamlit App


streamlit run app.py

How It Works


Logs into Gmail and fetches the previous day’s emails
Summarizes emails using GPT-4/o1
Ranks and displays the top 10 emails in a tabular format



License
This project is open-source 
