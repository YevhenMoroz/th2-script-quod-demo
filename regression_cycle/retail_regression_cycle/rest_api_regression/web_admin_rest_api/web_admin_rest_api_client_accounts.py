from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3637 import QAP_T3637
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3639 import QAP_T3639
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3641 import QAP_T3641
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3646 import QAP_T3646
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3647 import QAP_T3647
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3667 import QAP_T3667
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3668 import QAP_T3668
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3669 import QAP_T3669
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3804 import QAP_T3804
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3806 import QAP_T3806

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event("WA_REST_API_Client_Accounts", parent_id)
    configuration_admin_api_client_accounts = ComponentConfiguration("WA_REST_API_Client_Accounts")
    try:
        QAP_T3637(report_id, configuration_admin_api_client_accounts.data_set,
                  configuration_admin_api_client_accounts.environment).execute()
        QAP_T3639(report_id, configuration_admin_api_client_accounts.data_set,
                  configuration_admin_api_client_accounts.environment).execute()
        QAP_T3641(report_id, configuration_admin_api_client_accounts.data_set,
                  configuration_admin_api_client_accounts.environment).execute()
        QAP_T3646(report_id, configuration_admin_api_client_accounts.data_set,
                  configuration_admin_api_client_accounts.environment).execute()
        QAP_T3647(report_id, configuration_admin_api_client_accounts.data_set,
                  configuration_admin_api_client_accounts.environment).execute()
        QAP_T3667(report_id, configuration_admin_api_client_accounts.data_set,
                  configuration_admin_api_client_accounts.environment).execute()
        QAP_T3668(report_id, configuration_admin_api_client_accounts.data_set,
                  configuration_admin_api_client_accounts.environment).execute()
        QAP_T3669(report_id, configuration_admin_api_client_accounts.data_set,
                  configuration_admin_api_client_accounts.environment).execute()
        QAP_T3804(report_id, configuration_admin_api_client_accounts.data_set,
                  configuration_admin_api_client_accounts.environment).execute()
        QAP_T3806(report_id, configuration_admin_api_client_accounts.data_set,
                  configuration_admin_api_client_accounts.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
