from pathlib import Path
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import check_value_in_db, execute_db_command
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T2726(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        # region SSH
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion
        self.update_db_1 = f"UPDATE INSTRUMENT SET usddirectquotation1 = NULL " \
                           f"WHERE instrtype = 'SPO' AND instrsymbol = 'GBP/SEK';"
        self.update_db_2 = f"UPDATE INSTRUMENT SET usddirectquotation2 = NULL " \
                           f"WHERE instrtype = 'SPO' AND instrsymbol = 'GBP/SEK';"
        self.update_db_3 = f"UPDATE INSTRUMENT SET eurdirectquotation1 = NULL " \
                           f"WHERE instrtype = 'SPO' AND instrsymbol = 'GBP/SEK';"
        self.update_db_4 = f"UPDATE INSTRUMENT SET eurdirectquotation2 = NULL " \
                           f"WHERE instrtype = 'SPO' AND instrsymbol = 'GBP/SEK';"
        self.update_db_5 = f"UPDATE INSTRUMENT SET usdmajorpairinstrid1 = NULL " \
                           f"WHERE instrtype = 'SPO' AND instrsymbol = 'GBP/SEK';"
        self.update_db_6 = f"UPDATE INSTRUMENT SET usdmajorpairinstrid2 = NULL " \
                           f"WHERE instrtype = 'SPO' AND instrsymbol = 'GBP/SEK';"
        self.update_db_7 = f"UPDATE INSTRUMENT SET eurusdintermediateinstrid = NULL " \
                           f"WHERE instrtype = 'SPO' AND instrsymbol = 'GBP/SEK';"
        self.verifier = Verifier()
        self.expected_value_1 = "N"
        self.expected_value_2 = "Y"
        self.expected_value_3 = "Y"
        self.expected_value_4 = "Y"
        self.expected_value_5 = "6PmipPm4c296Keb7niIG9g"
        self.expected_value_6 = "OfE6V00PaJWIZSM04tiWPA"
        self.expected_value_7 = "KExUjnMCR-wK6DgQBZpg8g"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        execute_db_command(self.update_db_1, self.update_db_2, self.update_db_3, self.update_db_4, self.update_db_5,
                           self.update_db_6)
        self.ssh_client.send_command("qstart ITK")
        self.sleep(60)
        # region Step 1-2
        # Cross Through EUR To USD and Through USD To EUR are already set in WA. Check this in WA if test is failed.
        # endregion
        # region Step 4
        actual_value_1 = check_value_in_db(extracting_value="usddirectquotation1",
                                           query=f"SELECT usddirectquotation1 FROM instrument "
                                                 f"WHERE instrtype ='SPO' AND instrsymbol = 'GBP/SEK'")
        actual_value_2 = check_value_in_db(extracting_value="usddirectquotation2",
                                           query=f"SELECT usddirectquotation2 FROM instrument "
                                                 f"WHERE instrtype ='SPO' AND instrsymbol = 'GBP/SEK'")
        actual_value_3 = check_value_in_db(extracting_value="eurdirectquotation1",
                                           query=f"SELECT eurdirectquotation1 FROM instrument "
                                                 f"WHERE instrtype ='SPO' AND instrsymbol = 'GBP/SEK'")
        actual_value_4 = check_value_in_db(extracting_value="eurdirectquotation2",
                                           query=f"SELECT eurdirectquotation2 FROM instrument "
                                                 f"WHERE instrtype ='SPO' AND instrsymbol = 'GBP/SEK'")
        actual_value_5 = check_value_in_db(extracting_value="usdmajorpairinstrid1",
                                           query=f"SELECT usdmajorpairinstrid1 FROM instrument "
                                                 f"WHERE instrtype ='SPO' AND instrsymbol = 'GBP/SEK'")
        actual_value_6 = check_value_in_db(extracting_value="usdmajorpairinstrid2",
                                           query=f"SELECT usdmajorpairinstrid2 FROM instrument "
                                                 f"WHERE instrtype ='SPO' AND instrsymbol = 'GBP/SEK'")
        actual_value_7 = check_value_in_db(extracting_value="eurusdintermediateinstrid",
                                           query=f"SELECT eurusdintermediateinstrid FROM instrument "
                                                 f"WHERE instrtype ='SPO' AND instrsymbol = 'GBP/SEK'")
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check values in DB")
        self.verifier.compare_values("usddirectquotation1", self.expected_value_1, actual_value_1)
        self.verifier.compare_values("usddirectquotation2", self.expected_value_2, actual_value_2)
        self.verifier.compare_values("eurdirectquotation1", self.expected_value_3, actual_value_3)
        self.verifier.compare_values("eurdirectquotation2", self.expected_value_4, actual_value_4)
        self.verifier.compare_values("usdmajorpairinstrid1", self.expected_value_5, actual_value_5)
        self.verifier.compare_values("usdmajorpairinstrid2", self.expected_value_6, actual_value_6)
        self.verifier.compare_values("eurusdintermediateinstrid", self.expected_value_7, actual_value_7)
        self.verifier.verify()
        # endregion
