from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.ret.REST_API.Web_Admin_REST.Users_API.QAP_T3600 import QAP_T3600
from test_cases.ret.REST_API.Web_Admin_REST.Users_API.QAP_T3601 import QAP_T3601
from test_cases.ret.REST_API.Web_Admin_REST.Users_API.QAP_T3603 import QAP_T3603
from test_cases.ret.REST_API.Web_Admin_REST.Users_API.QAP_T3604 import QAP_T3604
from test_cases.ret.REST_API.Web_Admin_REST.Users_API.QAP_T3605 import QAP_T3605
from test_cases.ret.REST_API.Web_Admin_REST.Users_API.QAP_T3607 import QAP_T3607
from test_cases.ret.REST_API.Web_Admin_REST.Users_API.QAP_T3608 import QAP_T3608
from test_cases.ret.REST_API.Web_Admin_REST.Users_API.QAP_T3609 import QAP_T3609
from test_cases.ret.REST_API.Web_Admin_REST.Users_API.QAP_T3620 import QAP_T3620
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event("WA_REST_API_Users", parent_id)
    configuration_admin_api_users = ComponentConfiguration("WA_REST_API_Users")
    try:
        QAP_T3600(report_id, configuration_admin_api_users.data_set,
                  configuration_admin_api_users.environment).execute()
        QAP_T3601(report_id, configuration_admin_api_users.data_set,
                  configuration_admin_api_users.environment).execute()
        QAP_T3603(report_id, configuration_admin_api_users.data_set,
                  configuration_admin_api_users.environment).execute()
        QAP_T3604(report_id, configuration_admin_api_users.data_set,
                  configuration_admin_api_users.environment).execute()
        QAP_T3605(report_id, configuration_admin_api_users.data_set,
                  configuration_admin_api_users.environment).execute()
        QAP_T3607(report_id, configuration_admin_api_users.data_set,
                  configuration_admin_api_users.environment).execute()
        QAP_T3608(report_id, configuration_admin_api_users.data_set,
                  configuration_admin_api_users.environment).execute()
        QAP_T3609(report_id, configuration_admin_api_users.data_set,
                  configuration_admin_api_users.environment).execute()
        QAP_T3620(report_id, configuration_admin_api_users.data_set,
                  configuration_admin_api_users.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
