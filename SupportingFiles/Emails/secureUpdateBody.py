#!/usr/bin/python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import utils
import email, random, os, time, socket, email.mime.application, string

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
    ''' This file is meant to build the appropriate parts of the phishing message
    and will be called by phishing.py. Much more will be added to this to simplify the
    idea of building the messages and whatnot.'''
    MaskedURL = variable_dict['link']
    currentDate = utils.formatdate(timeval=None, localtime=True, usegmt=False)
    if MaskedURL == '':
        MaskedURL = URL_Placemarker

    # Split variable list to access specific vars. Assign if not already assigned.
    client = variable_dict['client']
    sender_in_body = variable_dict['bodysender']
    sender_in_header = variable_dict['headerfrom']
    if sender_in_header == '':
        sender_in_header = 'IT Support <ITSupport@contoso.com>'
    if sender_in_body == '':
        sender_in_body = 'ITSupport@contoso.com'
    if client == '':
        client = 'client'

    rand_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
    msgid = make_msgid(rand_id)

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_in_header
    msg['To'] = 'EMPADDR'
    msg['Subject'] = 'Security Updates'
    msg['Date'] = currentDate
    msg['Message ID'] = msgid

    #MaskedURL = URL_Placemarker  # change 'Secure Link' to desired mask or change line to "MaskedURL = URL_Placemarker" if no masked link desired.
    # Uncomment the following if you wish to send the message with the importance flag set.
    #important = '''X-Priority: 1 (Highest)
    #X-MSMail-Priority: High
    #'''
    currentDate = utils.formatdate(timeval=None, localtime=True, usegmt=False)

    plaintextBody ="""All,For security reasons, the IT department is registering each of the workstations
 with security software to make sure they receive security updates promptly.
Therefore, we are asking each employee to register their workstation.
 To register your workstation, please visit the website below and enter your
Corporate username and password.

Visit this website:
 {0}

Thanks,
{1} IT Department
Email: {2}

""".format(URL_Placemarker, client, sender_in_body)

    htmlBody ='''All,<br><br>For security reasons, the IT department is registering each of the workstations
with security software to make sure they receive security updates promptly. Therefore, we are
asking each employee to register their workstation.<br><br>

To register your workstation, please visit the website below and enter your <b>Corporate</b> username and password.<br><br>
                 Visit this website:<br>
<a href=3D\"{0}\">{1}</a>

<br>
<br>Thanks,<br> {2} IT Department<br>Email: {3}

'''.format(URL_Placemarker, MaskedURL, client, sender_in_body)

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
