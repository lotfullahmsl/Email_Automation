# import imaplib
# import smtplib
# import email
# from email.mime.text import MIMEText
# import requests

# # === Configuration ===
# EMAIL = 'muslimwallotfullah@gmail.com'
# PASSWORD = 'jjpp jepb ntrw aajj'  # Gmail App Password
# GROQ_API_KEY = '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'

# IMAP_SERVER = 'imap.gmail.com'
# SMTP_SERVER = 'smtp.gmail.com'
# SMTP_PORT = 465


# def get_unread_emails():
#     print("🔄 Connecting to Gmail (IMAP)...")
#     mail = imaplib.IMAP4_SSL(IMAP_SERVER)
#     mail.login(EMAIL, PASSWORD)
#     print("✅ Logged into Gmail!")

#     mail.select('inbox')
#     print("📥 Checking for unread emails...")

#     status, response = mail.search(None, '(UNSEEN)')
#     email_ids = response[0].split()
#     print(f"📧 Found {len(email_ids)} unread emails.")
#     emails = []

#     for e_id in email_ids:
#         print(f"📨 Reading email ID {e_id.decode()}")
#         _, msg_data = mail.fetch(e_id, '(RFC822)')
#         msg = email.message_from_bytes(msg_data[0][1])

#         sender = email.utils.parseaddr(msg['From'])[1]
#         subject = msg['Subject'] or "(No Subject)"
#         print(f"📬 From: {sender} | Subject: {subject}")

#         # Extract body
#         body = ""
#         if msg.is_multipart():
#             for part in msg.walk():
#                 content_type = part.get_content_type()
#                 content_dispo = str(part.get('Content-Disposition'))
#                 if content_type == 'text/plain' and 'attachment' not in content_dispo:
#                     charset = part.get_content_charset() or 'utf-8'
#                     try:
#                         body = part.get_payload(decode=True).decode(charset, errors='replace')
#                     except Exception:
#                         body = "[Could not decode body]"
#                     break
#         else:
#             try:
#                 body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
#             except Exception:
#                 body = "[Could not decode body]"

#         print(f"📄 Email body:\n{body}\n")
#         emails.append({'id': e_id, 'sender': sender, 'subject': subject, 'body': body})

#     return mail, emails


# def mark_as_read(mail, email_ids):
#     print("📌 Marking emails as read...")
#     for e_id in email_ids:
#         mail.store(e_id, '+FLAGS', '\\Seen')
#     print("✅ All processed emails marked as read.\n")


# def generate_groq_reply(email_body):
#     print("💬 Sending to Groq API...")

#     url = "https://api.groq.com/openai/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
#         "messages": [
#             {"role": "system", "content": "You are a helpful assistant replying to emails professionally."},
#             {"role": "user", "content": f"Reply to this email:\n\n{email_body}"}
#         ],
#         "temperature": 0.7,
#         "max_tokens": 512,
#         "stream": False
#     }

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()
#         data = response.json()
#         reply = data['choices'][0]['message']['content']
#         print(f"🤖 Groq replied:\n{reply}\n")
#         return reply
#     except requests.exceptions.HTTPError as e:
#         print(f"❌ HTTPError: {e.response.status_code} - {e.response.text}")
#         return "Sorry, we couldn’t process your message right now."
#     except Exception as e:
#         print(f"❌ General error from Groq API: {e}")
#         return "Sorry, we couldn’t process your message right now."


# def send_email(to_address, subject, body):
#     print(f"📤 Sending reply to {to_address}...")
#     msg = MIMEText(body)
#     msg['Subject'] = "Re: " + subject
#     msg['From'] = EMAIL
#     msg['To'] = to_address

#     try:
#         with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
#             smtp.login(EMAIL, PASSWORD)
#             smtp.send_message(msg)
#         print("✅ Email sent successfully!\n")
#     except Exception as e:
#         print(f"❌ Failed to send email: {e}\n")


# def main():
#     print("🚀 Starting Email Auto-Responder...\n")
#     mail, emails = get_unread_emails()

#     if not emails:
#         print("📭 No unread emails. Exiting.")
#         mail.logout()
#         return

#     for mail_obj in emails:
#         print(f"🔁 Processing email from {mail_obj['sender']}")
#         reply = generate_groq_reply(mail_obj['body'])
#         send_email(mail_obj['sender'], mail_obj['subject'], reply)

#     # Mark all emails as read
#     email_ids = [e['id'] for e in emails]
#     mark_as_read(mail, email_ids)

#     mail.logout()
#     print("🎉 Done with all unread emails!")


# if __name__ == "__main__":
#     main()

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
import requests
import time

# === Configuration ===
EMAIL = 'muslimwallotfullah@gmail.com'
PASSWORD = 'jjpp jepb ntrw aajj'  # Gmail App Password
GROQ_API_KEY = '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'

IMAP_SERVER = 'imap.gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465


def get_unread_emails():
    print("🔄 Connecting to Gmail (IMAP)...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    print("✅ Logged into Gmail!")

    mail.select('inbox')
    print("📥 Checking for unread emails...")

    status, response = mail.search(None, '(UNSEEN)')
    email_ids = response[0].split()
    print(f"📧 Found {len(email_ids)} unread emails.")
    emails = []

    for e_id in email_ids:
        print(f"📨 Reading email ID {e_id.decode()}")
        _, msg_data = mail.fetch(e_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        sender = email.utils.parseaddr(msg['From'])[1]
        subject = msg['Subject'] or "(No Subject)"
        print(f"📬 From: {sender} | Subject: {subject}")

        # Extract body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_dispo = str(part.get('Content-Disposition'))
                if content_type == 'text/plain' and 'attachment' not in content_dispo:
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        body = part.get_payload(decode=True).decode(charset, errors='replace')
                    except Exception:
                        body = "[Could not decode body]"
                    break
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
            except Exception:
                body = "[Could not decode body]"

        print(f"📄 Email body:\n{body}\n")
        emails.append({'id': e_id, 'sender': sender, 'subject': subject, 'body': body})

    return mail, emails


def mark_as_read(mail, email_ids):
    print("📌 Marking emails as read...")
    for e_id in email_ids:
        mail.store(e_id, '+FLAGS', '\\Seen')
    print("✅ All processed emails marked as read.\n")


def generate_groq_reply(email_body):
    print("💬 Sending to Groq API...")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant replying to emails professionally."},
            {"role": "user", "content": f"Reply to this email:\n\n{email_body}"}
        ],
        "temperature": 0.7,
        "max_tokens": 512,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        reply = data['choices'][0]['message']['content']
        print(f"🤖 Groq replied:\n{reply}\n")
        return reply
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTPError: {e.response.status_code} - {e.response.text}")
        return "Sorry, we couldn’t process your message right now."
    except Exception as e:
        print(f"❌ General error from Groq API: {e}")
        return "Sorry, we couldn’t process your message right now."


def send_email(to_address, subject, body):
    print(f"📤 Sending reply to {to_address}...")
    msg = MIMEText(body)
    msg['Subject'] = "Re: " + subject
    msg['From'] = EMAIL
    msg['To'] = to_address

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent successfully!\n")
    except Exception as e:
        print(f"❌ Failed to send email: {e}\n")


def main():
    print("🚀 Starting Email Auto-Responder (polling every 5 seconds)...\n")
    while True:
        mail, emails = get_unread_emails()

        if not emails:
            print("📭 No unread emails at this time.\n")
            mail.logout()
        else:
            for mail_obj in emails:
                print(f"🔁 Processing email from {mail_obj['sender']}")
                reply = generate_groq_reply(mail_obj['body'])
                send_email(mail_obj['sender'], mail_obj['subject'], reply)

            # Mark all emails as read
            email_ids = [e['id'] for e in emails]
            mark_as_read(mail, email_ids)
            mail.logout()
            print("🎉 Done with all unread emails!\n")

        print("⏳ Waiting 5 seconds before checking again...\n")
        time.sleep(5)  # Check every 5 seconds


if __name__ == "__main__":
    main()
