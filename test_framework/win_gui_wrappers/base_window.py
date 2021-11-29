import re
from inspect import signature
from functools import wraps
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier, VerificationMethod
from win_gui_modules.utils import get_base_request
from stubs import Stubs
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.utils import prepare_fe, get_opened_fe, get_base_request
from win_gui_modules.wrappers import set_base


class BaseWindow:
    def __init__(self, case_id, session_id):
        self.case_id = case_id
        self.session_id =session_id
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
        self.verifier = Verifier(self.case_id)

    def open_fe(self, report_id, folder, user, password, is_open=True):
        init_event = create_event("Initialization", parent_id=report_id)
        set_base(self.session_id, self.case_id)
        if not is_open:
            prepare_fe(init_event, self.session_id, folder, user, password)
        else:
            get_opened_fe(self.case_id, self.session_id)

    def switch_user(self, session_id):
        search_fe_req = FEDetailsRequest()
        search_fe_req.set_session_id(session_id)
        search_fe_req.set_parent_event_id(self.case_id)
        Stubs.win_act.moveToActiveFE(search_fe_req.build())
        set_base(session_id, self.case_id)

    @staticmethod
    def split_2lvl_values(split_values: dict):
        print(split_values)
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
    def get_function(decorated_function):
        @wraps(decorated_function)
        def improved_function(*args, **kwargs):
            try:
                return decorated_function(*args, **kwargs)
            except:
                print("Tuple object - \n", args)
                print("Object TestCase - \n", args[0])
                print("Object attributes - \n", args[0].__dict__)
                print("case_id - ", args[0].__dict__['case_id'])

                bca.create_event(f'Fail test event on the step - {decorated_function.__name__.upper()}',
                                 status='FAILED',
                                 parent_id=args[0].__dict__['case_id'])
                print(f"Test {test_id} was failed")
            finally:
                pass

        return improved_function
    return get_function
