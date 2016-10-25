#!/usr/bin/python

########################################
#                                      #
#                                      #
#  Used to drive the program           #
#  and send emails to users            #
#                                      #
#  Now GIT Enabled :)                  #
#                                      #
#  Created by Matt Grandy              #
#  Email: grandy[at]redteamsecure.com  #
#                                      #
#                                      #
########################################

import os
import ConfigParser
import argparse
import sys

from SupportingFiles import menuText
from SupportingFiles.buildMenu import *
from SupportingFiles import deliverEmails

# Initialize variables
argument_list = ['','','','', '','']
answerList = []
advanced_answer_list = ['','','','','http://google.com']
smtp_answer_list = ['','','','']
argument_list.insert(4, advanced_answer_list)

parser = argparse.ArgumentParser(prog=sys.argv[0],description=' -c <config file>')
parser.add_argument('-c', '--config', dest='configFile', help='specify a configuration file to use')
parser.add_argument('-v', '--verbose', dest='verboseFlag', action='store_true', help='Specify if you want verbose sending of emails')

args = parser.parse_args()


def importConfig():
    # Imports a given config file (this can be used if a -c flag given)
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(open(argument_dict['importfile']))
    options_len = len(config.options("Configs"))
    starter = 0
    for options in config.options("Configs"):
        if starter <= options_len:
            argument_dict[options] = config.get("Configs",options)
            starter = starter + 1

def exportConfig():
    # Exports a configuration file with a user-supplied name
    while 1:
        exportFile = raw_input(setpromt('\nName of desired config file:\n'))
        argument_dict['exportfile'] = exportFile
        if os.path.isfile(argument_dict['exportfile']):
            print '\nFile exists, chose a different name\n'
            continue
        elif exportFile in ['99', 'back', 'exit']:
            break
        else:
            exportFile = open(argument_dict['exportfile'], 'w')
            exportFile.write('[Configs]\n')
            for key, value in argument_dict.items():
                exportFile.write('\n' + str(key) + ' = ' + str(value))
            exportFile.close()
            print '\nFile exported successfully'
            break

def build_empty_dictionary():
    # Builds an empty dictionary with required keys
    tempDict = {}
    tempDict['scenario'] = ''
    tempDict['importfile'] = ''
    tempDict['exportfile'] = ''
    tempDict['verbose'] = str(args.verboseFlag)
    tempDict['link'] = ''
    tempDict['encoding'] = ''
    tempDict['encodinglength'] = ''
    tempDict['addressfile'] = ''
    tempDict['headerfrom'] = ''
    tempDict['smtpfrom'] = ''
    tempDict['client'] = 'no_client'
    tempDict['bodysender'] = ''
    tempDict['url'] = 'https://google.com'
    tempDict['attachment'] = ''
    tempDict['smtpserver'] = ''
    tempDict['smtpusername'] = ''
    tempDict['smtppass'] = ''
    tempDict['smtpport'] = '25'
    return tempDict

argument_dict = build_empty_dictionary()
# Call the configuration check if supplied -c flag
if (args.configFile != None):
    if os.path.isfile(args.configFile):
        argument_dict['importfile'] = args.configFile
        importConfig()
    else:
        print('404: File not found')
else:
    pass

while 1:

    ##############################
    #          Main Menu         #
    ##############################

    print('\n\n############################  MAIN MENU  #############################\n')
    print('                                    |  Selection:')
    create_menu(menuText.main_menu, '1', argument_dict)
    print('\n######################################################################')
    main_menu_choice = raw_input(setpromt(menuText.menu_text))
    if main_menu_choice == '99' or main_menu_choice.lower() == 'exit':
        break

    elif main_menu_choice == '1': # Pick scenario

        ##############################
        #          Scenario          #
        ##############################
        print
        show_scenario_menu = create_menu(menuText.scenario_menu, menuText.menu_text, '')
        print
        scenario_menu_choice = raw_input(setpromt('Select a pretext\n'))
        try:scenario_menu_choice_text = menuText.scenario_menu[int(scenario_menu_choice)-1]
        except: pass

        # The following will pull the length from the munuText file and determines if the user
        # chooses within that list.
        if scenario_menu_choice in (str(range(len(menuText.scenario_menu)+1))):
            argument_dict['scenario'] = scenario_menu_choice_text
            continue
        elif scenario_menu_choice in ['99','back','exit']:
            pass
        else:
            print 'Unknown pretext'
            continue


    if main_menu_choice == '2':

        ##############################
        #        Masked Link         #
        ##############################

        print('\n\n')
        masked_menu_choice = raw_input(setpromt('Use masked link? (y/n)\n'))
        if masked_menu_choice == 'y':
            masked_menu_string = raw_input(setpromt('\nWhat you want the link to appear as: \n'))
            argument_dict['link'] = masked_menu_string
        else:
            argument_dict['link'] = ''


    if main_menu_choice =='3':

        ################################
        #        Coding Scheme         #
        ################################

        print
        show_encoding_menu = create_menu(menuText.encoding_menu, menuText.menu_text, '')
        print
        encoding_menu_choice = raw_input(setpromt('Select an encoding scheme\n'))
        try:encoding_menu_choice_text = menuText.encoding_menu[int(encoding_menu_choice)-1]
        except: pass

        # Makes sure the selection is within the given list
        if encoding_menu_choice in ['1','2']:
            argument_dict['encoding'] = encoding_menu_choice_text
            if encoding_menu_choice == '2':
                encoding_length = raw_input(setpromt('Desired length of list? Max 32 characters\n'))
                # set a default value to make things easier
                if encoding_length == '':
                    encoding_length = '4'
                try: encoding_length_int = int(encoding_length)
                except: pass
                if int(encoding_length_int) > 32:
                    print '\nEncoding length too long, try again.\n'
                else:
                    argument_dict['encodinglength'] = encoding_length_int

        elif encoding_menu_choice in ['99', 'back', 'exit']:
            pass
        else:
            print 'Unknown encoding choice'


    if main_menu_choice =='4':

        ########################################
        #         Attach Address File          #
        ########################################

        while 1:
            print
            addresses_file = raw_input(setpromt('\nPlease input a text file with addresses to phish, one address per line\n'))

            if os.path.isfile(addresses_file):
                address_file_temp = open(addresses_file, 'r')
                for line in address_file_temp:
                    if ',' in line: # This needs to be re-done!
                        print '\nUnknown character in address file, please reformat file to one address per line, no characters other than _, -, ., @\n'
                        break
                    else:
                        print('File exists, using {0} for list of users to phish').format(addresses_file)
                        argument_dict['addressfile'] = addresses_file
                        break
                break
            elif addresses_file in ['99', 'back']:
                break
            else:
                print('404: File not found')


    if main_menu_choice =='5':
        # Have to create a list from the dictionary with advanced settings. Because I'm lazy
        advanced_answer_list.insert(0,argument_dict['headerfrom'])
        advanced_answer_list.insert(1,argument_dict['smtpfrom'])
        advanced_answer_list.insert(2,argument_dict['client'])
        advanced_answer_list.insert(3,argument_dict['bodysender'])
        advanced_answer_list.insert(4,argument_dict['url'])
        advanced_answer_list.insert(5,argument_dict['verbose'])
        advanced_answer_list.insert(6, argument_dict['attachment'])

        ##############################
        #     Advanced Settings      #
        ##############################
        while 1:

            print('\n\n@@@@@@@@@@@@@@@@@@@@@@@  ADVANCED MENU  @@@@@@@@@@@@@@@@@@@@@@@')
            print('\nUse Metasploit syntax: set [variable] [value] or unset [variable]')
            print('Example: set headerfrom matt@gmail.com or matt <matt@gmail.com>\n')
            print('    Description                             Variable       |  Selection')
            print('-------------------------------------------------------------------------')
            show_advanced_menu = create_advanced_menu(menuText.advanced_menu, menuText.menu_text, advanced_answer_list)
            print('\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

            advanced_menu_list = []
            advanced_menu_string = raw_input(setpromt('\nChange settings\n'))
            advanced_menu_list = advanced_menu_string.split()
            advanced_menu_list = advanced_menu_string.split(' ', 2)

            # Breaks on whitespace, then checks each index for a specific variable name
            # if it is typed correctly, the variable is added, removed, or replaced.
            if advanced_menu_list[0].lower() == 'set' or advanced_menu_list[0].lower() == 'unset':
                if advanced_menu_list[1].lower() == 'headerfrom':
                    if advanced_menu_list[0].lower() == 'unset':
                        argument_dict['headerfrom'] = ''
                    else:
                        argument_dict['headerfrom'] = advanced_menu_list[2]
                    # Still need to account for re-setting
                    try: del advanced_answer_list[0]
                    except: pass
                    advanced_answer_list.insert(0,argument_dict['headerfrom'])

                elif advanced_menu_list[1].lower() == 'smtpfrom':
                    # This one is what the SMTP server sees as "mail from"
                    if advanced_menu_list[0].lower() == 'unset':
                        argument_dict['smtpfrom'] = ''
                    else:
                        argument_dict['smtpfrom'] = advanced_menu_list[2]
                    try: del advanced_answer_list[1]
                    except: pass
                    advanced_answer_list.insert(1,argument_dict['smtpfrom'])

                elif advanced_menu_list[1].lower() == 'client':
                    if advanced_menu_list[0].lower() == 'unset':
                        argument_dict['client'] = ''
                    else:
                        argument_dict['client'] = advanced_menu_list[2]
                    try: del advanced_answer_list[2]
                    except: pass
                    advanced_answer_list.insert(2,argument_dict['client'])

                elif advanced_menu_list[1].lower() == 'bodysender':
                    if advanced_menu_list[0].lower() == 'unset':
                        argument_dict['bodysender'] = ''
                    else:
                        argument_dict['bodysender'] = advanced_menu_list[2]
                    try: del advanced_answer_list[3]
                    except: pass
                    advanced_answer_list.insert(3,argument_dict['bodysender'])

                elif advanced_menu_list[1].lower() == 'url':
                    if advanced_menu_list[0].lower() == 'unset':
                        argument_dict['url'] = ''
                    else:
                        argument_dict['url'] = advanced_menu_list[2]
                    try: del advanced_answer_list[4]
                    except: pass
                    advanced_answer_list.insert(4,argument_dict['url'])

                elif advanced_menu_list[1].lower() == 'verbose':
                    if advanced_menu_list[0].lower() == 'unset':
                        argument_dict['verbose'] = ''
                    else:
                        if advanced_menu_list[2].lower() in ['true', 'false']:
                            argument_dict['verbose'] = advanced_menu_list[2]
                        else: print '\nPlease specify either "True" or "False".\n'
                    try: del advanced_answer_list[5]
                    except: pass
                    advanced_answer_list.insert(5,argument_dict['verbose'])

                elif advanced_menu_list[1].lower() == 'attachment':
                    if advanced_menu_list[0].lower() == 'unset':
                        argument_dict['attachment'] = ''
                        try: del advanced_answer_list[6]
                        except: pass
                        advanced_answer_list.insert(6,argument_dict['attachment'])
                    else:
                        if os.path.isfile(advanced_menu_list[2]):
                            argument_dict['attachment'] = advanced_menu_list[2]
                            try: del advanced_answer_list[6]
                            except: pass
                            advanced_answer_list.insert(6,argument_dict['attachment'])
                        else:
                            print '404, file not found'
                            continue
                else:
                    print('Unknown command, try again ')


            elif  advanced_menu_list[0] in ['99', 'back', 'exit']:
                break
            else:
                print('Unknown command, try again ')



    if main_menu_choice =='6':

        #####################################
        #             SMTP Creds            #
        #####################################


        smtp_answer_list.insert(0,argument_dict['smtpserver'])
        smtp_answer_list.insert(1,argument_dict['smtpport'])
        smtp_answer_list.insert(2,argument_dict['smtpusername'])
        smtp_answer_list.insert(3,argument_dict['smtppass'])


        while 1:

            print('\n\n$$$$$$$$$$$$$$$$$$$$$$$$  SMTP MENU  $$$$$$$$$$$$$$$$$$$$$$$$')
            print('\nUse Metasploit syntax: set [variable] [value]')
            print('Example: set server smtp.google.com\n')
            print('    Description                             Variable       |  Selection')
            print('-------------------------------------------------------------------------')
            show_smtp_menu = create_advanced_menu(menuText.mail_settings_menu, menuText.menu_text, smtp_answer_list)
            print('\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            smtp_menu_list = []
            smtp_menu_string = raw_input(setpromt('\nChange settings\n'))
            smtp_menu_list = smtp_menu_string.split()
            smtp_menu_list = smtp_menu_string.split(' ', 2)

            # Breaks on whitespace, then checks each index for a specific variable name
            # if it is typed correctly, the variable is added or replaced.
            if smtp_menu_list[0].lower() == 'set' or smtp_menu_list[0].lower() == 'unset':
                if smtp_menu_list[1].lower() == 'server':
                    if smtp_menu_list[0].lower() == 'unset':
                        argument_dict['smtpserver'] = ''
                    else:
                        argument_dict['smtpserver'] = smtp_menu_list[2]
                    try: del smtp_answer_list[0]
                    except: pass
                    smtp_answer_list.insert(0,argument_dict['smtpserver'])

                elif smtp_menu_list[1].lower() == 'port':
                    if smtp_menu_list[0].lower() == 'unset':
                        argument_dict['smtpport'] = ''
                        try: del smtp_answer_list[1]
                        except: pass
                        smtp_answer_list.insert(1,argument_dict['smtpport'])
                    else:
                        if ((smtp_menu_list[2]).isdigit()):
                            argument_dict['smtpport'] = smtp_menu_list[2]
                            try: del smtp_answer_list[1]
                            except: pass
                            smtp_answer_list.insert(1,argument_dict['smtpport'])
                        else:
                            print 'Port entered was not a digit'
                            continue

                elif smtp_menu_list[1].lower() == 'username':
                    if smtp_menu_list[0].lower() == 'unset':
                        argument_dict['smtpusername'] =  ''
                    else:
                        argument_dict['smtpusername'] = smtp_menu_list[2]
                    try: del smtp_answer_list[2]
                    except: pass
                    smtp_answer_list.insert(2,argument_dict['smtpusername'])

                elif smtp_menu_list[1].lower() == 'password':
                    if smtp_menu_list[0].lower() == 'unset':
                        argument_dict['smtppass'] = ''
                    else:
                        argument_dict['smtppass'] = smtp_menu_list[2]
                    try: del smtp_answer_list[3]
                    except: pass
                    smtp_answer_list.insert(3,argument_dict['smtppass'])

                else:
                    print('Unknown command, try again ')

            elif  smtp_menu_list[0] in ['99', 'back', 'exit']:
                break
            else:
                print('Unknown command, try again ')


    if main_menu_choice =='7':

        ########################################
        #        Import/export Config          #
        ########################################

        while 1:
            print
            impExpAns = raw_input(setpromt('\nWould you like to import or export a config file (import/export)\n'))
            if impExpAns.lower() in ['import', 'export']:
                if impExpAns == 'import':
                    # If the user would like to import a configuration file
                    importFile = raw_input(setpromt('\nPath to config file:\n'))
                    if os.path.isfile(importFile):
                        print('File exists, using {0} for config file').format(importFile)
                        argument_dict['importfile'] = importFile
                        importConfig()
                        break
                    else:
                        print('404: File not found')
                elif impExpAns == 'export':
                    # Exports the current configuration to a file
                    exportConfig()
                    break

            elif impExpAns in ['99', 'back', 'exit']:
                break
            else:
                print('\nPlease either use "import" or "export".')


    if main_menu_choice =='8':

        ##############################
        #      Testing of email      #
        ##############################

        # THIS NEEDS TO BE REMOVED TO ACCOUNT FOR SERVERS WITHOUT AUTHENTICATION
        if argument_dict['smtpserver'] == '':
            print('\nPlease enter SMTP server before sending emails!')
            continue

        else:
            test_email_address = raw_input(setpromt('\nPlease input an email address to test\n'))

            if test_email_address in ['99', 'back']:
                continue
            else:
                deliverEmails.test_message(main_menu_choice, test_email_address, argument_dict)


    if main_menu_choice =='9':

        ##############################
        #      Sending of email      #
        ##############################

        # THIS NEEDS TO BE REMOVED TO ACCOUNT FOR SERVERS WITHOUT AUTHENTICATION
        if argument_dict['smtpserver'] == '':
            print('\nPlease enter SMTP server before sending emails!')
            continue

        verification = raw_input(setpromt('\n\nAre you sure you want to send? (YES/no)\n'))
        if verification == 'YES':
            deliverEmails.deliverance(argument_dict)

        elif verification.lower() in ['99','no','back']:
            continue
        else:
            print "Unknown command, returning to main menu"
            continue
    #if main_menu_choice not in range(1,9):
    #    print '\nUnrecognized choice, please make another selection\n'
    else:
        continue
