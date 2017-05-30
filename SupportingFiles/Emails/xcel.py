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
    d = str(datetime.datetime.today().strftime("%A, %B %d %Y"))
    delta = datetime.timedelta(days=-1)
    oldDate = (datetime.datetime.strptime(d,  "%A, %B %d %Y") + delta).strftime("%A, %B %d %Y")
    currentDate = utils.formatdate(timeval=None, localtime=True, usegmt=False)

    MaskedURL = variable_dict['link']
    if MaskedURL == '':
        MaskedURL = 'URL_Placemarker'

    sender_in_header = variable_dict['headerfrom']
    if sender_in_header == '':
        sender_in_header = 'team@connectsurvey.com'

    rand_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(15)])
    msgid = make_msgid(rand_id)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_in_header
    msg['To'] = 'EMPADDR'
    msg['Subject'] = 'Please Help Xcel Energy Serve You Better'
    msg['Date'] = currentDate
    msg['message-id'] = msgid


    # Would be good to find a way to use first name here.
    plaintextBody ='''
Dear EMPADDR,

[image: $50 Visa Gift Card] Thank you for speaking with ConnectSmart after
setting up your utility services. We are committed to providing the best
quality service. To better serve you, please take a moment to answer a
short survey

{0}

regarding your recent customer service experience. Your responses are very important
to us and will be kept strictly confidential.

How to get your $50

*Step 1:* Take our short survey
*Step 2:* Be automatically entered to win a $50 Visa Gift Card!


 [image: Click Here to Take this Survey]
{1}



If you have any questions please contact us at customercare@allconnectsurvey.com
or call 1-800-255-2666. Thank you for your participation in this survey. We
look forward to your response.


Best regards,
Your friends at ConnectSmart
Note: This offer is presented by Allconnect Inc. and is not affiliated with
your utility provider.

Copyright 2008 Allconnect, Inc
4 Concourse PKWY, Suite 410 Atlanta, GA 30328
Allconnect respects your privacy. As an Allconnect customer, you agreed
that we may contact you via email at EMPADDR.

'''.format(URL_Placemarker, URL_Placemarker)


    htmlBody = '''
<table width="663"><tbody>
    <tr>
        <td><img src="http://www.allconnect.com/25879/img/header/email_logo.gif">
        </td>
    </tr>
    <tr>
        <td>
            <p style="FONT-SIZE:20px;MARGIN-LEFT:5px">
                <font face="Arial, Helvetica, sans-serif">
                    Dear EMPADDR,<br><br>
                </font>
            </p>
            <p style="MARGIN-LEFT:5px;LINE-HEIGHT:26px">
                <font face="Arial, Helvetica, sans-serif" size="3"><img height="128
                    " alt="$50 Visa Gift Card" width="209" align="right" src="http://image.allconnect-email.com/86e7c8b3-f.jpg"> Thank you for speaking with
                    ConnectSmart after setting up your utility services. We are committed to providing
                    the best quality service. To better serve you, please take a moment to
                </font>
                <font size="3">
                    <a href="{0}" target="_blank">
                    answer a short survey
                    </a>
                </font>
                <font face="Arial, Helvetica, sans-serif" size="3">regarding your recent customer service experience.
                    Your responses are very important to us and will be kept strictly confidential.
                    <br><br>
                </font>
            </p>
            <p style="FONT-WEIGHT:bold;FONT-SIZE:32px;MARGIN-LEFT:0px;COLOR:#4d93bf">
                <font face="Arial, Helvetica, sans-serif" size="5">How to get your $50<br>
                </font>
            </p>
            <p style="MARGIN-LEFT:0px;LINE-HEIGHT:24px">
                <font face="Arial, Helvetica, sans-serif" size="3"><b>Step 1:</b> Take our short survey
                    <br><b>Step 2:</b> Be automatically entered to win a $50 Visa Gift Card!
                </font>
            </p>
            <p style="MARGIN-LEFT:0px;LINE-HEIGHT:24px">
                <font face="Arial, Helvetica, sans-serif" size="3"><br>
                </font>
                <a href="{1}" target="_blank">
                    <img height="43" alt="Click Here to Take this Survey" width="137" align="left" border="0" src="
                        http://image.allconnect-email.com/5f5637ae-8.jpg"></a></p><p style="MARGIN-LEFT:0px;LINE-HEIGHT:26px">
                        <font face="Arial, Helvetica, sans-serif" size="3">
                            <br><br>If you have any questions please contact us at
                            <a href="mailto:customercare@allconnect.com" target="_blank">customercare@allconnect.com
                            </a> or call
                            <a href="tel:1-800-255-2666" value="+18002454666" target="_blank">1-800-245-4666
                            </a>. Thank you for your participation in this survey. We look forward to your response.
                        </font>
            </p>
            <p style="FONT-SIZE:20px;MARGIN-LEFT:0px">
                <font face="Arial, Helvetica, sans-serif"><br>Best regards,<br>Your friends at ConnectSmart<br>
                </font>
                <font face="Arial" size="1">Note: This offer is presented by Allconnect Inc and is not affiliated with your utility provider.
                </font>
            </p>
        </td>
    </tr>
    <tr>
        <td height="20"><br>
        </td>
    </tr>
    <tr>
        <td>
            <font face="Arial" size="1">Copyright 2008 Allconnect, Inc
                <br>4 Concourse PKWY, Suite 410 Atlanta, GA 30328<br>
                Allconnect respects your
                <a href="http://www.allconnect.com/pages/privacy_policy.html" target="_blank">privacy
                </a>. As an Allconnect customer, you agreed that we may contact you via email at
                <a href="mailto:kurt.muhl@gmail.com" target="_blank">EMPADDR
                </a>.<span style="FONT-SIZE:7.5pt;FONT-FAMILY:Arial">If you no longer wish to receive emails,please select the link below:<br>
                <a href="https://www.allconnect.com/account/emailPreferences.html?=" target="_blank">https://www.allconnect.com/account/emailPreferences.html
                </a></span>
            </font>
        </td>
    </tr>
</tbody>
</table>
</center>
<br></div><br></div></div>
'''.format(oldDate, URL_Placemarker, URL_Placemarker)

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
