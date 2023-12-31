import re
from inspect import signature
from functools import wraps
from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from win_gui_modules.utils import get_base_request


class BaseWindow:
    def __init__(self, case_id, session_id):
        self.case_id = case_id
        self.session_id = session_id
        self.base_request = get_base_request(session_id, case_id)
        self.extraction_id = bca.client_orderid(4)
        self.verifier = Verifier(self.case_id)

    def clear_details(self, details_list: list):
        for detail in details_list:
            if str(signature(detail.__init__)).find("base_request") != -1:
                detail.__init__(self.base_request)
            else:
                detail.__init__()

    def compare_values(self, expected_values: dict, actual_values: dict, event_name: str,
                       verification_method: VerificationMethod = VerificationMethod.EQUALS):
        self.verifier.set_event_name(event_name)
        try:
            for k, v in expected_values.items():
                self.verifier.compare_values("Compare: " + k, v, actual_values[k],
                                             verification_method)
        except KeyError:
            print("Element: " + k + " not found")
        self.verifier.verify()
        # TODO Ask Yevhen
        self.verifier = Verifier(self.case_id)

    @staticmethod
    def split_fees(split_values: dict):
        print(split_values)
        if type(list(split_values.values())[0]) == dict:
            response = BaseWindow.split_fees(list(split_values.values())[0])
            return response
        else:
            print(split_values)
            normal_split_values_arr = list()
            for split_key, split_value in split_values.items():
                split_sentence = split_value.split('\n')
                split_sentence.pop(0)
                split_sentence.pop(len(split_sentence) - 1)
                for split_values1 in split_sentence:
                    # old regular value (\w+=[\w\d/.]+)
                    split_values1 = re.findall('([\w%.]+=[\w\d/%,.]+)', split_values1)
                    split_values1 = split_values1.__str__()
                    split_values1 = split_values1.replace('[', '').replace(']', '').replace("'", '').replace(",", '')
                    split_normal_dictionary = dict(item.split("=") for item in split_values1.split(' '))
                    normal_split_values_arr.append(split_normal_dictionary)
            return normal_split_values_arr

    @staticmethod
    def split_tab_misk(split_values: dict):
        normal_split_values_arr = list()
        for split_key, split_value in split_values.items():
            split_sentence = split_value.split('\n')
            split_sentence.pop(0)
            split_sentence.pop(0)
            split_sentence.pop(len(split_sentence) - 1)
            for split_values1 in split_sentence:
                split_values1 = split_values1.replace('[', '').replace(']', '').replace("'", '').replace(' ', '')
                print(split_values1)
                split_normal_dictionarry = dict(item.split(":") for item in split_values1.split(', '))
                print(split_normal_dictionarry)
                normal_split_values_arr.append(split_normal_dictionarry)
        return normal_split_values_arr

    @staticmethod
    def split_main_tab(split_values: dict):
        if type(list(split_values.values())[0]) == dict:
            response = BaseWindow.split_fees(list(split_values.values())[0])
            return response
        else:
            normal_split_values_arr = list()
            for split_key, split_value in split_values.items():
                split_sentence = split_value.split('\n')
                split_sentence.pop(0)
                split_sentence.pop(len(split_sentence) - 1)
                for split_values1 in split_sentence:
                    split_values1 = split_values1.__str__()
                    split_values1 = split_values1.replace('\r', '')
                    values = split_values1.split(':')
                    split_normal_dictionary = dict({values[0]: values[1]})
                    normal_split_values_arr.append(split_normal_dictionary)
            return normal_split_values_arr
