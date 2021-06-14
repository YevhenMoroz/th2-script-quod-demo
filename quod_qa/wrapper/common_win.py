from stubs import Stubs
from win_gui_modules.utils import prepare_fe_2, get_opened_fe


def prepare_fe(case_id, session_id):
    print(f'prepare_fe(frontend_is_open={Stubs.frontend_is_open})')

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

#   TODO: find common default values for fe_dir, fe_pass, fe_user
# def prepare_fe(case_id, session_id, fe_dir: str, fe_user: str, fe_pass: str):
#     print(f'prepare_fe(frontend_is_open={Stubs.frontend_is_open})')
#
#     if not Stubs.frontend_is_open:
#         prepare_fe_2(case_id, session_id, fe_dir, fe_user, fe_pass)
#     else:
#         get_opened_fe(case_id, session_id)
