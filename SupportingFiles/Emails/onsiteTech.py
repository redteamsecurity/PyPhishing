#!/usr/bin/python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import utils
import email, random, os, time, datetime, socket, email.mime.application, string

''' This file is meant to build the appropriate parts of the phishing message
and will be called by phishing.py. Much more will be added to this to simplify the
idea of building the messages and whatnot. TEST'''


URL_Placemarker = 'URL_Placemarker'

def make_msgid(idstring=None):
    """Returns a string suitable for RFC 2822 compliant Message-ID
    Optional idstring if given is a string used to strengthen the
    uniqueness of the message id.
    """
    timeval = int(time.time()*100)
    pid = os.getpid()
    randint = random.getrandbits(64)
    if idstring is None:
        idstring = ''
    else:
        idstring = '.' + idstring
    msgid = '<%d.%d.%d%s>' % (timeval, pid, randint, idstring)
    return msgid

def build_body(variable_dict):
    MaskedURL = variable_dict['link']
    if MaskedURL == '':
        MaskedURL = 'URL_Placemarker'

    sender_in_header = variable_dict['headerfrom']
    if sender_in_header == '':
        sender_in_header = 'MicrosoftSupport@contoso.com'

    rand_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
    msgid = make_msgid(rand_id)

    client = variable_dict['client']
    if client == '':
        client = 'NO CLIENT'
    d = str(datetime.datetime.today().strftime("%A, %B %Y"))
    delta = datetime.timedelta(days=-1)
    currentDate = utils.formatdate(timeval=None, localtime=True, usegmt=False)

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_in_header
    msg['To'] = 'EMPADDR'
    msg['Subject'] = 'Technician On-site'
    msg['Date'] = currentDate
    msg['Message ID'] = msgid


    plaintextBody ='''We are having a technician from {0} arriving at LOCATION today at TIME, so please ensure they have access to the network room.\n\n
Thanks,
NAME
'''

    htmlBody = '''We are having a technician from {0} arriving at LOCATION today at TIME, so please ensure they have access to the network room.<br>
<br>
Thanks,<br>
NAME<br><br>
'''.format(client)

    # File attachment
    if variable_dict['attachment'] != '':
        filename = variable_dict['attachment']
        fp = open(filename,'rb')
        extension = filename.rsplit('.', 1)[-1]
        att = email.mime.application.MIMEApplication(fp.read(),_subtype=extension)
        fp.close()
        att.add_header('Content-Disposition','attachment',filename=filename)
        msg.attach(att)

    part1 = MIMEText(plaintextBody, 'plain')
    part2 = MIMEText(htmlBody, 'html')


    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    return msg.as_string()
