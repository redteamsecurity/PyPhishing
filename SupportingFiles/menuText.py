#!/usr/bin/python

########################################
#                                      #
#                                      #
#     Used to create the textual       #
#     menues for the application       #
#                                      #
#                                      #
########################################



menu_text =  '\n Select from the menu \n'

variable_menu = ['\n Set a variable in the format: "set [variable] [data] "',
                 'Example: set smtpfrom it@microsoft.com']

main_menu = ['Choose a Pretext',
             'Masked Link?',
             'User Coding Scheme',
             'Attach Address File',
             'Advanced Settings',
             'SMTP Credentials',
             'Import/Export Config File',
             'Test',
             'Send Out!!']

scenario_menu = ['Zixmail Secure Email',
                 'Secure Update Delivery',
                 'Microsoft Update',
                 'MS Update Forward',
                 'Google Support',
                 'FedEx Shipment Unsuccessful',
                 'On-site Tech',
                 'IT Controls Document',
                 'Xcel',
                 'Test']

masked_menu = ['Use a masked Link? (yes,no)',
               'What do you want it to appear as?']

encoding_menu = ['Base64 encoded email',
                 'Randomized ID']

advanced_menu = ['Sender in email header                  (headerfrom)',
                 'Sender in SMTP settings                 (smtpfrom)',
                 'Client name for message variables       (client)',
                 'Email address to use within email body  (bodysender)',
                 'URL to direct users to (unmasked)       (url)',
                 'Set verbosity (true/false)              (verbose)',
                 'Attach file to email                    (attachment)']

mail_settings_menu = ['Mail server (ex. smtp.google.com)       (server)',
                      'SMTP Port (default is 25)               (port)',
                      'SMTP Username                           (username)',
                      'SMTP Password                           (password)']
