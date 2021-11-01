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
