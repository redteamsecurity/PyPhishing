#!/usr/bin/python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
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
        sender_in_header = 'Support@goo.com'

    rand_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
    msgid = make_msgid(rand_id)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_in_header
    msg['To'] = 'EMPADDR'
    msg['Subject'] = 'Message from the Microsoft Security Team'
    msg['Date'] = currentDate
    msg['Message ID'] = msgid


    plaintextBody ='''Hello,\n\nThere has been a recent virus outbreak in corporate environments that target out of date systems.\n
The virus corrupts and deletes all data on the affected machine and therefore can be very dangerous.\n
Please download and install the updates manually at the link below, as we do not want to wait to push it out in our normal patch cycle.\n
{0}\n
Thank you,
Microsoft Security Team\n\n
Note: Please DO NOT reply to this email, this is an unmanaged email address. Replies will not be received.

    '''.format(URL_Placemarker)


    # Images need to be hosted on the internet to properly work
    htmlBody ='''
<img src="cid:part1.microsoft@goodattachment" width="20%%" height="5%%" alt="">
<br><br><br>

Hello,<br>
<br>

There has been a recent virus outbreak in corporate environments that target out of date systems.<br>
The virus corrupts and deletes all data on the affected machine and therefore can be very dangerous.<br>
<br>

Please <b>download and install</b> the updates manually at the link below, as we do not want to wait to push it out in our normal patch cycle.<br>
<br>

<a href="{0}">{1}</a><br>
<br>

Thank you,<br>
Microsoft Security Team
<br>
<br>
<b>Note:</b> Please DO NOT reply to this email, this is an unmanaged email address. Replies will not be received.
    '''.format(URL_Placemarker, MaskedURL)


    if variable_dict['attachment'] != '':
            filename = variable_dict['attachment']
            fp=open(filename,'rb')
            extension = filename.rsplit('.', 1)[-1]
            att = email.mime.application.MIMEApplication(fp.read(),_subtype=extension)
            fp.close()
            att.add_header('Content-Disposition','attachment',filename=filename)
            msg.attach(att)

    img_location = os.getcwd() + '/SupportingFiles/images/microsoft.png'
    img_data = open(img_location, 'rb').read()

        # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(plaintextBody, 'plain')
    part2 = MIMEText(htmlBody, 'html')


    image = MIMEImage(img_data)
    image.add_header('Content-Transfer-Encoding','base64')
    image.add_header('Content-ID', '<part1.microsoft@goodattachment>')
    image.add_header('Content-disposition', 'inline')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    msg.attach(image)

    return msg.as_string()

