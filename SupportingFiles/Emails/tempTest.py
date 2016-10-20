#!/usr/bin/env python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import utils
import email, random, os, time, datetime, socket, email.mime.application, string

date = str(datetime.datetime.today().strftime("%A, %B %d, %Y"))
currentDate = utils.formatdate(timeval=None, localtime=True, usegmt=False)

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

    sender_in_header = variable_dict['headerfrom']
    if sender_in_header == '':
        sender_in_header = 'Support@contoso.com'

    rand_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
    msgid = make_msgid(rand_id)
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_in_header
    msg['To'] = 'EMPADDR'
    msg['Subject'] = 'Check this out'
    msg['Date'] = currentDate
    msg['Message ID'] = msgid


    # Create the body of the message (a plain-text and an HTML version).
    text = 'Hey,\n\nCan you look over the new IT breakdown document that\'s attached? Let me know if there are any errors or anything that needs to be changed.\n\nThanks'
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hey,<br><br>
           Can you look over the new IT breakdown document that's attached? Let me know if there are any errors or anything that needs to be changed.<br><br>
           Thanks
        </p>
      </body>
    </html>
    """

    if variable_dict['attachment'] != '':
        filename = variable_dict['attachment']
        fp=open(filename,'rb')
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
