import time
from copy import deepcopy
from pathlib import Path
from pkg_resources import resource_filename

from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import check_value_in_db
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiSecurityBlockMessages import RestApiSecurityBlockMessages
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T2668(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.security_block_message = RestApiSecurityBlockMessages()
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.msg_params_security_block = None
        self.msg_params_security_block_default = None
        self.gbp_myr_spot = self.data_set.get_instr_id_by_name("gbp_myr_spot")
        # region SSH
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion
        self.verifier = Verifier()
        self.expected_value_1 = "KExUjnMCR-wK6DgQBZpg8g"
        self.expected_value_2 = "Y"
        self.expected_value_3 = "Y"
        self.expected_value_4 = "DoFmauLpl7JyG4LFlk-GIA"
        self.expected_value_5 = "mYMFCWVhP2-BvmhdkY1yXg"
        self.expected_value_6 = "Y"
        self.expected_value_7 = "Y"
        self.expected_value_8 = "6PmipPm4c296Keb7niIG9g"
        self.expected_value_9 = "XQ7Tj0V3Vg_QZEZhQErOPw"
        self.expected_value_10 = "N"
        self.expected_value_11 = "Y"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-2
        self.security_block_message.find_security_block(self.gbp_myr_spot)
        self.msg_params_security_block = self.rest_manager.send_get_request_filtered(self.security_block_message)
        self.msg_params_security_block = self.rest_manager.parse_response_details(self.msg_params_security_block,
                                                                                  {"listingID": "1208844004"})
        self.msg_params_security_block_default = deepcopy(self.msg_params_security_block)
        self.msg_params_security_block.update({'crossThroughUSDToEUR': "true", 'crossThroughEURToUSD': "true"})
        self.security_block_message.clear_message_params().manage_security_block().set_params(
            self.msg_params_security_block)
        self.rest_manager.send_post_request(self.security_block_message)
        self.sleep(2)
        # endregion
        # region Step 3
        self.ssh_client.send_command("qstart ITK")
        self.sleep(60)
        # endregion
        # region Step 4
        actual_value_1 = check_value_in_db(extracting_value="eurusdintermediateinstrid",
            query=f"SELECT eurusdintermediateinstrid FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        actual_value_2 = check_value_in_db(extracting_value="crossthrougheurtousd",
            query=f"SELECT crossthrougheurtousd FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        actual_value_3 = check_value_in_db(extracting_value="crossthroughusdtoeur",
            query=f"SELECT crossthroughusdtoeur FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        actual_value_4 = check_value_in_db(extracting_value="eurmajorpairinstrid1",
            query=f"SELECT eurmajorpairinstrid1 FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        actual_value_5 = check_value_in_db(extracting_value="eurmajorpairinstrid2",
            query=f"SELECT eurmajorpairinstrid2 FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        actual_value_6 = check_value_in_db(extracting_value="eurdirectquotation1",
            query=f"SELECT eurdirectquotation1 FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        actual_value_7 = check_value_in_db(extracting_value="eurdirectquotation2",
            query=f"SELECT eurdirectquotation2 FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        actual_value_8 = check_value_in_db(extracting_value="usdmajorpairinstrid1",
            query=f"SELECT usdmajorpairinstrid1 FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        actual_value_9 = check_value_in_db(extracting_value="usdmajorpairinstrid2",
            query=f"SELECT usdmajorpairinstrid2 FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        actual_value_10 = check_value_in_db(extracting_value="usddirectquotation1",
            query=f"SELECT usddirectquotation1 FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        actual_value_11 = check_value_in_db(extracting_value="usddirectquotation2",
            query=f"SELECT usddirectquotation2 FROM instrument WHERE instrtype ='SPO' AND instrsymbol = 'GBP/MYR'")
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check value in DB")
        self.verifier.compare_values("eurusdintermediateinstrid", self.expected_value_1, actual_value_1)
        self.verifier.verify()
        self.verifier.compare_values("crossthrougheurtousd", self.expected_value_2, actual_value_2)
        self.verifier.verify()
        self.verifier.compare_values("crossthroughusdtoeur", self.expected_value_3, actual_value_3)
        self.verifier.verify()
        self.verifier.compare_values("eurmajorpairinstrid1", self.expected_value_4, actual_value_4)
        self.verifier.verify()
        self.verifier.compare_values("eurmajorpairinstrid2", self.expected_value_5, actual_value_5)
        self.verifier.verify()
        self.verifier.compare_values("eurdirectquotation1", self.expected_value_6, actual_value_6)
        self.verifier.verify()
        self.verifier.compare_values("eurdirectquotation2", self.expected_value_7, actual_value_7)
        self.verifier.verify()
        self.verifier.compare_values("usdmajorpairinstrid1", self.expected_value_8, actual_value_8)
        self.verifier.verify()
        self.verifier.compare_values("usdmajorpairinstrid2", self.expected_value_9, actual_value_9)
        self.verifier.verify()
        self.verifier.compare_values("usddirectquotation1", self.expected_value_10, actual_value_10)
        self.verifier.verify()
        self.verifier.compare_values("usddirectquotation2", self.expected_value_11, actual_value_11)
        self.verifier.verify()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.security_block_message.clear_message_params().manage_security_block().set_params(
            self.msg_params_security_block_default)
        self.rest_manager.send_post_request(self.security_block_message)
        self.sleep(2)
