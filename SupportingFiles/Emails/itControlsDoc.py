#!/usr/bin/python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import utils
import email, random, os, time, socket, email.mime.application, string

''' This file is meant to build the appropriate parts of the phishing message
and will be called by phishing.py. Much more will be added to this to simplify the
idea of building the messages and whatnot.'''


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
    idhost = socket.getfqdn()
    msgid = '<%d.%d.%d%s@%s>' % (timeval, pid, randint, idstring, idhost)
    return msgid

def build_body(variable_dict):
    currentDate = utils.formatdate(timeval=None, localtime=True, usegmt=False)
    MaskedURL = variable_dict['link']
    if MaskedURL == '':
        MaskedURL = 'URL_Placemarker'

    sender_in_header = variable_dict['headerfrom']
    if sender_in_header == '':
        sender_in_header = 'Support@contoso.com'

    rand_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
    msgid = make_msgid(rand_id)
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_in_header
    msg['To'] = 'EMPADDR'
    msg['Subject'] = 'Can you look at this?'
    msg['Date'] = currentDate
    msg['message-id'] = msgid


    plaintextBody ='''Hey,\n\nCan you look over some of the new IT controls I'm writing up and respond with any changes?\n\nThanks'''

    htmlBody ='''Hey,<br><br>
Can you look over some of the new IT controls I'm writing up and respond with any changes?<br><br>
Thanks<br>'''

    if variable_dict['attachment'] != '':
        # If a document is to be attached
        filename = variable_dict['attachment']
        fp=open(filename,'rb')
        extension = filename.rsplit('.', 1)[-1]
        att = email.mime.application.MIMEApplication(fp.read(),_subtype=extension)
        fp.close()
        att.add_header('Content-Disposition','attachment',filename=filename)
        msg.attach(att)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(plaintextBody, 'plain')
    part2 = MIMEText(htmlBody, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    return msg.as_string()
