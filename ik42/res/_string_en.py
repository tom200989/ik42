import sys, os
sys.path.append("..")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

class String_en:
    EN_TR = {  #
        'test_name': "test_name",  #
        'please_input_your_15': "Input 15 digital IMEI number",  #
        'you_must_provide': "You must provide a legal IMEI number",  #
        'digit_imei_is_required': "15 digit IMEI number is required",  #
        'all_operation_are_success': "All operations are successful\nYou can enjoy the internet now.",  #
        'ok': "OK",  #
        'try_again': "Try again",  #
        'copr_tcl_all_rights': "Copyright 2021 TCL All rights reserved",  #
        'the_current_network': "The current network connection timed out!\nPlease try again.",  #
        'unfortunately_the_verification': "Unfortunately, the verification failed!\nYou can plug dongle again and click try again.",  #
    }
