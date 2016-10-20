#!/usr/bin/python

########################################
#                                      #
#                                      #
#     Used to create the build         #
#     menues for each instance obj     #
#                                      #
#                                      #
########################################

import readline
readline.parse_and_bind('tab: complete')


def dict_to_list(temporaryDict):
    # Takes in a dictionary and creates a list (crappy shortcut but will work for now)
    tempList = []
    tempList.insert(0, temporaryDict['scenario'])
    tempList.insert(1, temporaryDict['link'])
    tempList.insert(2, temporaryDict['encoding'])
    tempList.insert(3, temporaryDict['addressfile'])
    a = [] # had to create a list to put in tempList (backwards as hell, i know)
    a.insert(0, temporaryDict['headerfrom'])
    a.insert(1, temporaryDict['smtpfrom'])
    a.insert(2, temporaryDict['client'])
    a.insert(3, temporaryDict['bodysender'])
    a.insert(4, temporaryDict['url'])
    a.insert(5, temporaryDict['verbose'])
    a.insert(6, temporaryDict['attachment'])
    tempList.insert(4, a)
    b = []
    b.insert(0, temporaryDict['smtpserver'])
    b.insert(1, temporaryDict['smtpusername'])
    b.insert(2, temporaryDict['smtppass'])
    b.insert(3, temporaryDict['smtpport'])
    tempList.insert(5, b)

    return tempList

class create_menu:
    '''This is used to build an instance of the menu object
       and can be called from the main program to instantiate the menu
       with passed variables.'''
    def __init__(self, menu, text, variable_dict):
        if type(variable_dict) == dict:
            # Sometimes a blank string is passed and that needs to be accounted for
            variable_list = dict_to_list(variable_dict) # Shortcut so I didn't have to build the menu shit again
        else:
            variable_list = variable_dict
        self.text = text
        self.menu = menu
        self.variable = variable_list
        var_list_length = len(variable_list)
        o = 0

        # Build the menu
        for i, option in enumerate(menu):
            option_length = len(option)
            menunum = i + 1
            if menunum < 10:

                # If there are variables passed, it prints them
                if o < var_list_length:
                    if type(variable_list[o]) is type(list()):
                        # Print the variables differently if a list
                        variable_string = ''

                        for item in variable_list[o]:
                            variable_string = variable_string + ', ' + item
                        variable_string = variable_string[2:]
                        print('  %s)  %s' %(menunum, option))  + ((30-option_length)*' ') + '|  ' + variable_string

                    else:
                        print('  %s)  %s' %(menunum, option))  + ((30-option_length)*' ') + '|  ' + variable_list[o]
                    o += 1

                else:
                    print('  %s)  %s' %(menunum, option))  + ((28-option_length)*' ') + '  |    '


            elif menunum >= 10 and menunum < 99:
                # To be used when the list exceeds 10 options
                # could probably be more graceful (but it works)
                if o < var_list_length:
                    if type(variable_list[o]) is type(list()):
                        variable_string = ''

                        for item in variable_list[o]:
                            variable_string = variable_string + ', ' + item
                        variable_string = variable_string[2:]
                        print(' %s)  %s' %(menunum, option))  + ((30-option_length)*' ') + '|  ' + variable_string

                    else:
                        print(' %s)  %s' %(menunum, option))  + ((30-option_length)*' ') + '|  ' + variable_list[o]
                    o += 1

                else:
                    print(' %s)  %s' %(menunum, option))  + ((28-option_length)*' ') + '  |    '

            else:
                print('  %s)  %s' %(menunum, option))
        if '99' not in text:
            print '\n 99) Exit or Return to Main Menu'
        return

class create_advanced_menu:
    '''This is used to build an instance of the menu object
       and can be called from the main program to instantiate the advanced
       menu with passed variables.'''
    def __init__(self, menu, text, variable_list):
        self.text = text
        self.menu = menu
        self.variable = variable_list
        var_list_length = len(variable_list)
        o = 0

        # Build the menu
        for i, option in enumerate(menu):
            option_length = len(option)
            menunum = i + 1
            if menunum < 10:

                # If there are variables passed, it prints them
                if o < var_list_length:
                    if type(variable_list[o]) is type(list()):
                        # Print the variables differently if a list
                        variable_string = ''
                        for item in variable_list[o]:
                            variable_string = variable_string + ' ' + item
                        variable_string = variable_string
                        print('  > %s' %( option))  + ((55-option_length)*' ') + '|  ' + variable_string

                    else:
                        print('  > %s' %(option)) + ((55-option_length)*' ') + '|  ' + variable_list[o]
                    o += 1
                else:
                    print('  > %s' %(option ))  + ((52-option_length)*' ') + '  |    '
            else:

                print('  %s)  %s' %(menunum, option))
        if '99' not in text:
            print '\n 99) Exit or Return to Main Menu'
        return

def setpromt(text):
    return text + ' >> '
