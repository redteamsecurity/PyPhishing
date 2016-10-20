#!/usr/bin/python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
    d = str(datetime.datetime.today().strftime("%A, %B %d %Y"))
    delta = datetime.timedelta(days=-1)
    oldDate = (datetime.datetime.strptime(d,  "%A, %B %d %Y") + delta).strftime("%A, %B %d %Y")
    currentDate = utils.formatdate(timeval=None, localtime=True, usegmt=False)


    MaskedURL = variable_dict['link']
    if MaskedURL == '':
        MaskedURL = 'URL_Placemarker'

    sender_in_header = variable_dict['headerfrom']
    if sender_in_header == '':
        sender_in_header = 'Support@rt-sec.net'

    rand_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
    msgid = make_msgid(rand_id)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = 'Delivery Support <{0}>'.format(sender_in_header)
    msg['To'] = 'EMPADDR'
    msg['Subject'] = 'Undeliverable Package'
    msg['Date'] = currentDate
    msg['Message ID'] = msgid


    # Create the body of the message (a plain-text and an HTML version).
    text ='''*Fed**Ex*\n\n
Not possible to make delivery.\n\nOur company's courier couldn't make the delivery.\n\nTracking Updates\n\n
FedEx 1995-2016 | Global Home | Terms of Use | Security and Privacy
'''.format(oldDate)

    html = """\
    <html>
      <head></head>
      <body>
        <p>
        <div style="max-width:680px;color:#555555;font:13px Arial;border:solid 1px #dfdfdf;padding:20px">
            <b style="color:#4d148c;font-size:32px;font-weight:bold">Fed</b>
            <b style="color:#adafb1;font-size:32px;font-weight:bold">Ex</b><br>
            <br>{0}<br>
            <span style="color:#222222;font-weight:bold">Not possible to make delivery.
            </span><br>
            <br>
            Our company's courier couldn't make the delivery.<br>
            <a href={1} >Tracking Updates</a><br><br><br>
            <div style=3D"font-size:11px">&#169; FedEx 1995-2016 |
                <a style="color:#555555;text-decoration:none">Global Home</a> |
                <a style="color:#555555;text-decoration:none">Terms of Use</a> |
                <a style="color:#555555;text-decoration:none">Security and Privacy</a>
            </div>
        </div>
        </p>
      </body>
    </html>
    """.format(oldDate, URL_Placemarker)

    # File attachment
    if variable_dict['attachment'] != '':
        filename = variable_dict['attachment']
        fp = open(filename,'rb')
        extension = filename.rsplit('.', 1)[-1]
        att = email.mime.application.MIMEApplication(fp.read(),_subtype=extension)
        fp.close()
        att.add_header('Content-Disposition','attachment',filename=filename)
        msg.attach(att)


    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')


    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    return msg.as_string()
