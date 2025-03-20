import streamlit as st
import pandas as pd
from gmail_auth import fetch_previous_day_emails, summarize_emails

# Streamlit UI Config
st.set_page_config(page_title="Email Summarizer", layout="wide")

st.title("📧 AI-Powered Email Summarizer")
st.write("Fetch and prioritize emails from the previous day using AI.")

# Button to fetch emails
if st.button("📩 Fetch Top 10 Priority Emails"):
    with st.spinner("Fetching and summarizing emails..."):
        emails = fetch_previous_day_emails()
        
        if emails:
            summary = summarize_emails(emails)

            # Convert JSON summary to structured table
            email_data = []
            for idx, email in enumerate(emails[:10]):  # Only top 10
                email_data.append({
                    "Priority": idx + 1,  # Numbering the priority
                    "Sender": email["from"],
                    "Subject": email["subject"],
                    "Snippet": email["snippet"]
                })

            # Convert list to DataFrame
            df = pd.DataFrame(email_data)

            # Display the clean table
            st.subheader("📊 Top 10 Priority Emails")
            st.dataframe(df)

        else:
            st.warning("No emails found for the previous day.")
