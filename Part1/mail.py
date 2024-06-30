import smtplib
import dns.resolver
import re
from colorama import Fore, Style, init

init(autoreset=True)

def is_valid_email(email):
    # Basic regex for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def check_email(email):
    try:
        domain = email.split('@')[1]
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange
        mx_record = str(mx_record)
        
        # Set up the SMTP connection
        server = smtplib.SMTP(timeout=10)
        server.set_debuglevel(0)

        server.connect(mx_record)
        server.helo(server.local_hostname)  # Send HELO command to the server
        server.mail('me@domain.com')  # Send mail from command
        code, message = server.rcpt(email)  # Send rcpt to command
        server.quit()
        
        if code == 250:
            return True
        else:
            return False
    except Exception as e:
        return False

def main():
    live_count = 0
    dead_count = 0
    live_emails = []

    with open('scraped_emails.txt', 'r') as file:
        emails = file.readlines()

    for email in emails:
        email = email.strip()
        if not is_valid_email(email):
            print(f"{Fore.YELLOW}{email} is not a valid email address.")
            continue

        if check_email(email):
            print(f"{Fore.BLACK}{email} is live.")
            live_emails.append(email)
            live_count += 1
        else:
            print(f"{Fore.RED}{email} is dead.")
            dead_count += 1

    # Write live emails to live.txt
    with open('live.txt', 'w') as live_file:
        for live_email in live_emails:
            live_file.write(live_email + '\n')

    print(f"\n{Fore.BLACK}Live emails: {live_count}")
    print(f"{Fore.RED}Dead emails: {dead_count}")

if __name__ == "__main__":
    main()
