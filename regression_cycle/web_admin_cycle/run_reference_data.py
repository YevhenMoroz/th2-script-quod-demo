import time
import traceback
from datetime import timedelta

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_1727 import QAP_1727
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_1729 import QAP_1729
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_1731 import QAP_1731
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_1732 import QAP_1732
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_1733 import QAP_1733
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_1736 import QAP_1736
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_1737 import QAP_1737
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_2154 import QAP_2154
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_2302 import QAP_2302
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_2504 import QAP_2504
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_2904 import QAP_2904
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_2905 import QAP_2905
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_2940 import QAP_2940
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_2971 import QAP_2971
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_3136 import QAP_3136
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_3399 import QAP_3399
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_4709 import QAP_4709
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_4861 import QAP_4861
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_4862 import QAP_4862
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_755 import QAP_755
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_756 import QAP_756
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_758 import QAP_758
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_759 import QAP_759
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_760 import QAP_760
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_761 import QAP_761
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_762 import QAP_762
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_763 import QAP_763


class ReferenceData:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            # QAP_755(self.web_driver_container, self.second_lvl_id).run()
            # QAP_756(self.web_driver_container, self.second_lvl_id).run()
            # QAP_758(self.web_driver_container, self.second_lvl_id).run()
            # QAP_759(self.web_driver_container, self.second_lvl_id).run()
            # QAP_760(self.web_driver_container, self.second_lvl_id).run()
            QAP_761(self.web_driver_container, self.second_lvl_id).run()
            # QAP_762(self.web_driver_container, self.second_lvl_id).run()
            # QAP_763(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1727(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1729(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1731(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1732(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1733(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1736(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1737(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2154(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2302(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2504(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2904(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2905(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2940(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2971(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3136(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3399(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4709(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4861(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4862(self.web_driver_container, self.second_lvl_id).run()
            end_time = time.monotonic()
            print("Reference data ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
