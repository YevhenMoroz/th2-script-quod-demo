import os
from pathlib import Path

from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.win_gui_wrappers.base_window import decorator_try_except
from stubs import Stubs
from win_gui_modules.layout_panel_wrappers import WorkspaceModificationRequest
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


class LayoutLoader:
    def __init__(self, report_id, session_id):
        self.report_id = report_id
        self.session_id = session_id
        self.case_name = Path(__file__).name[:-3]
        self.case_id = bca.create_event(self.case_name, self.report_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        set_base(self.session_id, self.case_id)

    @decorator_try_except(test_id=os.path.basename(__file__))
    def import_layout(self, file_name, dir_name):
        modification_request = WorkspaceModificationRequest()
        modification_request.set_default_params(base_request=self.base_request)
        modification_request.set_filename(file_name)
        modification_request.set_path(str(os.path.dirname(__file__))+f"/{dir_name}")
        modification_request.do_import()
        call(Stubs.win_act_options.modifyWorkspace, modification_request.build())
