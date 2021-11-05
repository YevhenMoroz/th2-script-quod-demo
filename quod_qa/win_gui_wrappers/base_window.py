import re
from inspect import signature
from functools import wraps
from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from win_gui_modules.wrappers import set_base


class BaseWindow:
    def __init__(self, case_id, base_request):
        self.case_id = case_id
        self.base_request = base_request
        self.extraction_id = bca.client_orderid(4)
        self.verifier = Verifier(self.case_id)

    def clear_details(self, details_list: list):
        for detail in details_list:
            if str(signature(detail.__init__)).find("base_request") != -1:
                detail.__init__(self.base_request)
            else:
                detail.__init__()

    def compare_values(self, expected_values: dict, actual_values: dict, event_name,
                       verification_method: VerificationMethod = VerificationMethod.EQUALS):
        self.verifier.set_event_name(event_name)
        try:
            for k, v in expected_values.items():
                self.verifier.compare_values("Compare: " + k, v, actual_values[k],
                                             verification_method)
        except KeyError:
            print("Element: " + k + " not found")
        self.verifier.verify()
        self.verifier = Verifier(self.case_id)


def split_2lvl_values(split_values):
    for split_key, split_value in split_values.items():
        normal_split_values_arr = list()
        split_sentence = split_value.split('\n')
        split_sentence.pop(0)
        split_sentence.pop(len(split_sentence) - 1)
        for split_values1 in split_sentence:
            split_values1 = re.findall('(\w+=\w+)', split_values1)
            split_values1 = split_values1.__str__()
            split_values1 = split_values1.replace('[', '').replace(']', '').replace("'", '')
            split_normal_dictionarry = dict(item.split("=") for item in split_values1.split(', '))
            normal_split_values_arr.append(split_normal_dictionarry)
    return normal_split_values_arr


def decorator_try_except(test_id):
    def _safe(f):
        @wraps(f)
        def safe_f(*args, **kwargs):
            try:
                case_id = bca.create_event(test_id, args[0])

                set_base(args[1], case_id)
                # for a in args:
                #     print(str(a))

                return f(*args, **kwargs)
            except:
                print(f"Test {test_id} was failed")
                bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
            finally:
                pass

        return safe_f

        return _safe
