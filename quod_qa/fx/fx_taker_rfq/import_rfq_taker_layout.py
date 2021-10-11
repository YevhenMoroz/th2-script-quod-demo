import logging
import os
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from win_gui_modules.layout_panel_wrappers import WorkspaceModificationRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base


def import_layout(base_request, option_service):
    print('import_layout()')
    modification_request = WorkspaceModificationRequest()
    modification_request.set_default_params(base_request=base_request)
    modification_request.set_filename("rfq_taker_layout.xml")
    modification_request.set_path(str(os.path.dirname(__file__)))
    modification_request.do_import()
    call(option_service.modifyWorkspace, modification_request.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    option_service = Stubs.win_act_options
    try:
        import_layout(case_base_request, option_service)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)