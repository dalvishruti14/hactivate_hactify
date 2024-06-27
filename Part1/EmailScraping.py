import re
import urllib.request
import time

emailRegex = re.compile(r'''
#example :
#something-.+_@somedomain.com
(
([a-zA-Z0-9_.+]+
@
[a-zA-Z0-9_.+]+)
)
''', re.VERBOSE)

# Extacting Emails
def extractEmailsFromUrlText(urlText, seen_emails):
    extractedEmail = emailRegex.findall(urlText)
    allemails = []
    for email in extractedEmail:
        allemails.append(email[0])
    lenh = len(allemails)
    print("\tNumber of Emails : %s\n" % lenh)
    for email in allemails:
        if email not in seen_emails:
            seen_emails.add(email)
            emailFile.write(email + "\n")  # appending Emails to a file

# HtmlPage Read Func
def htmlPageRead(url, i, seen_emails):
    try:
        start = time.time()
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        urlHtmlPageRead = response.read()
        urlText = urlHtmlPageRead.decode()
        print("%s.%s\tFetched in : %s" % (i, url, (time.time() - start)))
        extractEmailsFromUrlText(urlText, seen_emails)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# EmailsLeechFunction
def emailsLeechFunc(url, i, seen_emails):
    try:
        htmlPageRead(url, i, seen_emails)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            try:
                url = 'http://webcache.googleusercontent.com/search?q=cache:' + url
                htmlPageRead(url, i, seen_emails)
            except Exception as e:
                print(f"Error fetching cached page for {url}: {e}")
        else:
            print(f"HTTP Error {err.code} while fetching {url}")

# Open a file for reading urls
start = time.time()
urlFile = open("urls.txt", 'r')
emailFile = open("emails.txt", 'a')
i = 0
seen_emails = set()

# Iterate opened file for getting single url
for urlLink in urlFile.readlines():
    urlLink = urlLink.strip('\'"')
    i = i + 1
    emailsLeechFunc(urlLink, i, seen_emails)

print("Elapsed Time: %s" % (time.time() - start))

urlFile.close()
emailFile.close()
