#!/usr/bin/python

import smtplib, base64, random, re, string, csv, time
from Emails import secureUpdateBody
from Emails import microsoftUpdateBody
from Emails import microsoftUpdateForward
from Emails import zixmailSecureEmail
from Emails import googleSupport
from Emails import fedEx
from Emails import onsiteTech
from Emails import itControlsDoc
from Emails import xcel
from Emails import tempTest

# Variable initialization
cleanAddresses = []
email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


# This will build a CSV file of user's email addresses, base64encoded emails, and if message was successfully sent
def buildCSV(address, email_id, success):
    #if (os.path.isfile('addresses.csv')):
     #   print 'addresses.csv exists, please remove or rename'
    #else:
    with open('delivered.csv', 'a') as csvfile:
        a = csv.writer(csvfile, delimiter=',')
        data = [[address, email_id, success]]
        a.writerows(data)


def build_email(address, temp_dict):
    # Builds the phishing message on the fly
    body_file = determine_pretext(temp_dict['scenario'])

    # This needs to be removed
    if temp_dict['link'] != '':
        oldBody = body_file.build_body(temp_dict)
    else:
        oldBody = body_file.build_body(temp_dict)

    # Creates a custom message for each recipient
    PHISHING_URL = temp_dict['url']
    if PHISHING_URL == '':
        PHISHING_URL = 'http://google.com'


    if temp_dict['encoding'] == 'Randomized ID':
        # Randomized chars as user ID
        if temp_dict['encodinglength'] == '':
            temp_dict['encodinglength'] = '4'
        random_range = int(temp_dict['encodinglength'])
        email_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(random_range)])
        newPhishURL = PHISHING_URL + email_id
        #oldBody.replace("EMPADDR",address)
        newBody = string.replace(oldBody,"EMPADDR",address)
        newBody = string.replace(newBody, "URL_Placemarker", newPhishURL)

    else:
        # Base64 encoded email as user ID
        email_id = base64.b64encode(address)
        if temp_dict['scenario'] == 'Secure Update Delivery':
            # Have to remove ?uid= when using this pretext in order to have the database accept the value
            newPhishURL = PHISHING_URL + email_id
        else:
            newPhishURL = PHISHING_URL + "?uid=3D" + email_id
        newBody = string.replace(oldBody,"EMPADDR",address)
        newBody = string.replace(newBody, "URL_Placemarker", newPhishURL)

    return newBody, email_id

def determine_pretext(pretext):
    pretext_file = ''
    # The pretext is passed and the correct file is set
    # for build_email and then deliverance function
    if 'Zixmail Secure Email' in pretext:
        # If scenario 1 is selected do the following
        pretext_file = zixmailSecureEmail
    elif 'Secure Update Delivery' in pretext:
        pretext_file = secureUpdateBody
    elif 'Microsoft Update' in pretext:
        pretext_file = microsoftUpdateBody
    elif 'MS Update Forward' in pretext:
        pretext_file = microsoftUpdateForward
    elif 'Google Support' in pretext:
        pretext_file = googleSupport
    elif 'FedEx Shipment Unsuccessful' in pretext:
        pretext_file = fedEx
    elif 'On-site Tech' in pretext:
        pretext_file = onsiteTech
    elif 'IT Controls Document' in pretext:
        pretext_file = itControlsDoc
    elif 'Xcel' in pretext:
        pretext_file = xcel
    elif 'Test' in pretext:
        pretext_file = tempTest

    return pretext_file

# Sends the email
def deliverance(variable_dict):
    username = variable_dict['smtpusername']
    password = variable_dict['smtppass']
    smtpServer = variable_dict['smtpserver']
    smtpport = variable_dict['smtpport']

    #Should this be smtpSender???
    sender = variable_dict['smtpfrom']

    server = smtplib.SMTP(smtpServer, smtpport)
    if variable_dict['verbose'].lower() == 'true':
        server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    if username != '' and password != '':
        # To be used when smtp servers do not require authentication
        server.login(username,password)

    cleanAddresses = []
    if variable_dict['addressfile'] != '':
        # If sending to bulk list
        emailOpen = open(variable_dict['addressfile'], 'r')
        addresses = emailOpen.readlines()

        print '\nTime started: '
        print (time.strftime("%H:%M:%n\n"))

    # The following removes new line chars and carriage returns from text file
        for element in addresses:
            element = element.strip('\n\r')
            if not email_pattern.match(element):
                print "Email addresses are not in correct format, please check. Hint: one address per line."
                break
            cleanAddresses.append(element)
        for address in cleanAddresses:
            message, email_id = build_email(address, variable_dict)

            try:
                server.sendmail(sender, address, message)
                success='Delivered'
                buildCSV(address, email_id, success) # adds user email address and b64 encoded address to csv
                print 'Successfully sent email to {0}'.format(address)
                time.sleep(5)
            except:
                print "\n\nError: unable to send email to {0}".format(address)
                success='Not Delivered'
                buildCSV(address, email_id, success) # adds user email address and b64 encoded address to csv
        server.quit()
        print 'Time Done: '
        print (time.strftime("%H:%M:%S"))


def temp_deliverance(test_address, test_variable_dict):
    # for use when a test email is being sent
    username = test_variable_dict['smtpusername']
    password = test_variable_dict['smtppass']
    smtpServer = test_variable_dict['smtpserver']
    smtpport = test_variable_dict['smtpport']

    message, email_id = build_email(test_address, test_variable_dict)

    sender = test_variable_dict['smtpfrom']
    server = smtplib.SMTP(smtpServer, smtpport)
    if test_variable_dict['verbose'].lower() == 'true':
        server.set_debuglevel(1)

    server.ehlo()
    server.starttls()
    if username != '' and password != '':
        # To be used when smtp servers do not require authentication
        server.login(username,password)
    try:
        server.sendmail(sender, test_address, message)
        print "Successfully sent test email to {0}".format(test_address)
        time.sleep(5)
    except Exception:
        print "Error: unable to send test email to {0}".format(test_address)

    server.quit()


def test_message(choice, temp_test_email, temp_variable_dict):
    # Used if the user is testing an email scenario
    if choice == '8':
        temp_deliverance(temp_test_email, temp_variable_dict)
    else:
        print('Error, returning to menu')
        return
