import os
from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.win_gui_wrappers.base_window import decorator_try_except
from stubs import Stubs
from win_gui_modules.layout_panel_wrappers import WorkspaceModificationRequest
from win_gui_modules.utils import call


class Test(TestCase):
    def __init__(self,  report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name

    @decorator_try_except(test_id=os.path.basename(__file__))
    def import_layout(self):
        modification_request = WorkspaceModificationRequest()
        modification_request.set_default_params(base_request=self.base_request)
        modification_request.set_filename(self.file_name)
        modification_request.set_path(str(os.path.dirname(__file__)))
        modification_request.do_import()
        call(Stubs.win_act_options.modifyWorkspace, modification_request.build())

    def execute(self):
        self.import_layout()
