# Phishing-Application

 - Please use this tool ethically and within legal means. The developer and anyone who contributes takes no liability for user's actions while using the tool. Be good.

This application is used to send phishing emails to any number of users. The data is pulled from a user-supplied
text document. The menu is fairly self explanatory. Be sure to test before delivering to a lot of users!

# Usage: 
     > python pyPhishing.py
     > python pyPhishing.py -h
     > python pyPhishing.py -c [config file]

        [Follow menu and be sure to add data to advanced settings]

# Description/Purpose of files:
    > pyPhishing.py
        - Used to drive the application, contains most of the menu logic and data manipulation.

    > SupportingFiles/
        -> deliverEmails.py
                - The second most important file for this application. Contains the logic for sending emails and building
                message bodies.
        -> buildMenu.py
                - Creates an instance of the menu class each time the menu is called. A separate menu for advanced options
                was created to fix some formatting.

    > SupportingFiles/Emails/
        -> zixmailSecureEmail.py, microsoftUpdateBody.py, secureUpdateBody.py, etc.
                - These files contain all of the text for email messages, including headers. If it is desired to change the
                wording in an email message, these files are where you want to look.
