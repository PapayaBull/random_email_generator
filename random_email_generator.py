import requests
import random
import string
import time

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_guerrilla_mail():
    """Create a random Guerrilla Mail email address."""
    url = "https://api.guerrillamail.com/ajax.php"
    
    try:
        random_local_part = generate_random_string()
        params = {
            'f': 'set_email_user',
            'email_user': random_local_part
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if 'email_addr' not in data:
            raise ValueError("Failed to get the email address from Guerrilla Mail")

        temp_email = data['email_addr']
        
        return temp_email, data['sid_token']
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None

def check_email(sid_token):
    """Check for new emails using Guerrilla Mail."""
    url = "https://api.guerrillamail.com/ajax.php"
    
    try:
        params = {
            'f': 'get_email_list',
            'sid_token': sid_token,
            'offset': 0
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        emails = response.json().get('list', [])
        
        return emails
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def read_email(email_id, sid_token):
    """Read an email by ID using Guerrilla Mail."""
    url = "https://api.guerrillamail.com/ajax.php"
    
    try:
        params = {
            'f': 'fetch_email',
            'sid_token': sid_token,
            'email_id': email_id
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        email = response.json()
        
        return email
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
temp_email, sid_token = create_guerrilla_mail()
if temp_email:
    print("Generated Temporary Email:", temp_email)
    
    # Wait for a while to receive emails
    print("Waiting for emails...")
    time.sleep(10)
    
    emails = check_email(sid_token)
    if emails:
        print(f"Received {len(emails)} emails.")
        for email in emails:
            print(f"Email ID: {email['mail_id']}")
            print(f"From: {email['mail_from']}")
            print(f"Subject: {email['mail_subject']}")
            print(f"Date: {email['mail_date']}")
            print("Body Snippet:", email['mail_excerpt'])
            print()
            
            # Optionally, read the full email
            full_email = read_email(email['mail_id'], sid_token)
            if full_email:
                print("Full Email Body:")
                print(full_email['mail_body'])
                print("-" * 40)
    else:
        print("No emails received.")
