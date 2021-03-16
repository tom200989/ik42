import locale
from ik42.res._string_en import *
from ik42.res._string_es import *

class Strings:  # 类名不要以下划线开头

    def __init__(self):
        super().__init__()
        self.test_name = ""
        self.please_input_your_15 = ""
        self.you_must_provide = ""
        self.digit_imei_is_required = ""
        self.all_operation_are_success = ""
        self.ok = ""
        self.try_again = ""
        self.copr_tcl_all_rights = ""
        self.the_current_network = ""
        self.unfortunately_the_verification = ""

        # 获取本地系统语言
        local = locale.getdefaultlocale()[0]
        if 'es' in local:
            self.translation(String_es.ES_TR)
        elif 'en' in local:
            self.translation(String_en.EN_TR)
        elif 'zh' in local:
            self.translation(String_en.EN_TR)

    """翻译"""
    def translation(self, language_dict):
        self.test_name = language_dict['test_name']
        self.please_input_your_15 = language_dict['please_input_your_15']
        self.you_must_provide = language_dict['you_must_provide']
        self.digit_imei_is_required = language_dict['digit_imei_is_required']
        self.all_operation_are_success = language_dict['all_operation_are_success']
        self.ok = language_dict['ok']
        self.try_again = language_dict['try_again']
        self.copr_tcl_all_rights = language_dict['copr_tcl_all_rights']
        self.the_current_network = language_dict['the_current_network']
        self.unfortunately_the_verification = language_dict['unfortunately_the_verification']
