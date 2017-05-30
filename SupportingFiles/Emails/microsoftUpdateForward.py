#!/usr/bin/python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import utils
import email, random, os, time, datetime, socket, email.mime.application, string

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
    d = str(datetime.datetime.today().strftime("%A, %B %d, %Y %I:%M%p"))
    delta = datetime.timedelta(hours=-2)
    sentDate = (datetime.datetime.strptime(d,  "%A, %B %d, %Y %I:%M%p") + delta).strftime("%A, %B %d, %Y %I:%M%p")
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
    msg['Subject'] = 'FW: Message from the Microsoft Security Team'
    msg['Date'] = currentDate
    msg['message-id'] = msgid

    plaintextBody ="""All,

Please see below about an urgent message sent from Microsoft this morning. Follow the instructions and
install the update to your systems ASAP.

1. Run the update
2. When SmartScreen pops up, click "more info" and then the "Run" button.
3. A screen may pop up, but that's normal. Everything should be updated after running.

Thanks,
CLIENT NAME

---------- Forwarded message ----------
From: Microsoft Security Team <MST@microsoftsecurityteam.com>
Date: {0}
Subject: Message from the Microsoft Security Team
To: CLIENT NAME <CLIENTEMAIL>

Hello,

There has been a recent virus outbreak in corporate environments that target out of date systems.
The virus corrupts and deletes all data on the affected machine and therefore can be very dangerous.

Please download and install the updates manually at the link below, as we do not want to wait to push it out in our normal patch cycle.

{1}

Thank you,
Microsoft Security Team


Note: Please DO NOT reply to this email, this is an un-managed email address. Replies will not be received.

--
    """.format(sentDate, URL_Placemarker)

    htmlBody ='''
All, <br><br>

Please see below about an urgent message sent from Microsoft this morning. Follow the instructions and
install the update to your systems <b>ASAP</b>. <br><br>

1. Run the update<br>
2. When SmartScreen pops up, click "more info" and then the "Run" button.<br>
3. A screen may pop up, but that's normal. Everything should be updated after running.<br><br>

Thanks, <br>
CLIENT NAME <br><br>

---------- Forwarded message ---------- <br>
From: Microsoft Security Team &lt;<a href="mailto:Security@microsoft.com">Security@microsoft.com</a>&gt; <br>
Date: {0} <br>
Subject: Message from the Microsoft Security Team <br>
To: CLIENT NAME &lt;<a href="mailto:CLIENTEMAIL">CLIENTEMAIL</a>&gt;
<br><br>

Hello,<br>
<br>

There has been a recent virus outbreak in corporate environments that target out of date systems.<br>
The virus corrupts and deletes all data on the affected machine and therefore can be very dangerous.<br>
<br>

Please <b>download and install</b> the updates manually at the link below, as we do not want to wait to push it out in our normal patch cycle.<br>
<br>

<a href="{1}">{2}</a><br>
<br>

Thank you,<br>
Microsoft Security Team
<br>
<br>
<b>Note:</b> Please DO NOT reply to this email, this is an un-managed email address. Replies will not be received.
    '''.format(sentDate, URL_Placemarker, MaskedURL)

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
