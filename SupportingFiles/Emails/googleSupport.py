#!/usr/bin/python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import utils
import email, random, os, time, datetime, socket, email.mime.application, string

''' This file is meant to build the appropriate parts of the Google phishing message
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
    delta = datetime.timedelta(days=-4)
    oldDate = (datetime.datetime.strptime(d,  "%A, %B %d %Y") + delta).strftime("%A, %B %d %Y")
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
    msg['Subject'] = 'Returned email message'
    msg['Date'] = currentDate
    msg['Message ID'] = msgid


    plaintextBody = '''Google Support\nEMPADDR\nLynn Bisson (Google Support) has sent you a message:\n
{0}\nUndeliverable messages.\nMore information\n_____________________________\n
This e-mail was sent to EMPADDR.\nDon't want occasional updates about Google activity? Change what email
Google Team sends you.
'''.format(oldDate)

    htmlBody = '''<div style="background:#fff">
    <div style="max-width:700px">
        <table cellspacing="0" cellpadding="0" style="font-family:arial;font-size:13px;color:#666;border:solid 1px #f2f2f2;width:100%">
            <tr>
                <td style="background:#f7f7f7;padding:0px">
                    <table cellspacing="0" cellpadding="0" border="0">
                        <tr>
                            <td style="padding-left:10px">
                                <img src="cid:part1.google@goodattachment" width="120px" height="50px" alt="">
                            <td style="font-size:18px;color:#ccc;padding-left:10px">Support
                            </td>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding:10px">
                    <a style="color:#245dc1;font-size:18px;text-decoration:none">EMPADDR<br>
                    </a>
                    <br>
                    <span style="color:#333;font-weight:bold">Lynn Bisson
                    </span> (Google Support) has sent you a message:<br><br>
                    {0}
                    <br>
                   Undeliverable messages.<br>
                   <a style="color:#245dc1">More information
                   </a>
                </td>
            </tr>
            <tr>
                <td style="padding:10px">
                    <a href={1} style="font-family:arial;display:inline-block;padding:7px 15px;background:#5284d4;color:#fff;font-size:13px;font-weight:bold;border:solid 1px #245dc1;white-space:nowrap;text-decoration:none">View Messages
                    </a>
                </td>
            </tr>
            <tr>
                <td style="font-size:11px;padding:10px">
                   <hr noshade size="1" color="#f2f2f2">This e-mail was sent to
                    <a style="color:#245dc1;text-decoration:none">EMPADDR
                    </a>.
                     <br>Don't want occasional updates about Google activity?
                </td>
            </tr>
        </table>
    </div>
</div>

'''.format(oldDate, URL_Placemarker, URL_Placemarker)


    if variable_dict['attachment'] != '':
            filename = variable_dict['attachment']
            fp=open(filename,'rb')
            extension = filename.rsplit('.', 1)[-1]
            att = email.mime.application.MIMEApplication(fp.read(),_subtype=extension)
            fp.close()
            att.add_header('Content-Disposition','attachment',filename=filename)
            msg.attach(att)

    img_location = os.getcwd() + '/SupportingFiles/images/google.png'
    img_data = open(img_location, 'rb').read()

        # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(plaintextBody, 'plain')
    part2 = MIMEText(htmlBody, 'html')


    image = MIMEImage(img_data)
    image.add_header('Content-Transfer-Encoding','base64')
    image.add_header('Content-ID', '<part1.google@goodattachment>')
    image.add_header('Content-disposition', 'inline')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    msg.attach(image)

    return msg.as_string()
