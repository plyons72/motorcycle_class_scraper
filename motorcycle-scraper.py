#!/usr/bin/python3

from bs4 import BeautifulSoup
import smtplib
import time
from urllib.request import urlopen


# URL of the frame containing the table we need to scrape
course_site = "https://app.msi5.com/scripts/i5.exe?book=pamsp&page=CS.CL&c=284&fr=FrLayout.1&page=CS.CL.Select&Mode=PB&SC=CCACNORT&CC=BRC"

while (1):
    # First, get the page
    page = urlopen(course_site)
    soup = BeautifulSoup(page, "html.parser")

    # Now with the frame selected in the soup object, grab the form containing the table
    form = soup.find('form', {'name': 'CL'})

    # Now grab the outer table contained in the form
    container = form.find('table', {'width': '856'})

    # Now grab the div holding the inner table that we want
    table_div = container.find('div', {'id': 'tblSchedule'})

    # Now that we have the correct table, get the body of it
    table_body = table_div.find('table')

    # Instantiate a list to hold all the availability values
    availability = list()

    # Cycle through the first 10 rows in the table and get the availability values for those classes
    for i in range(10):
        seat_name = 'tblSchedule_dfSeats_'
        seat_name += str(i)
        availability.append(table_body.find('input', {'name': seat_name})['value'])

    # Create SMTP object to email myself
    email = smtplib.SMTP('smtp.gmail.com', 587)

    # Start TLS for security
    email.starttls()

    # Gmail credentials
    username = ""
    email = username + "@gmail.com"
    app_password = ""

    # Authentication
    email.login(username, app_password)

    # Subject Text
    SUBJECT = "Motorcycle Class Update"

    # Message Text
    TEXT = "A motorcycle class is available now!!"

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    for i in availability:
        if int(i) > 0:

            # Send the message from you to you
            print("Sending email")
            email.sendmail(email, email, message)

    # Quit the email session
    email.quit()

    # Sleep for 5 minutes and check again
    time.sleep(300)
