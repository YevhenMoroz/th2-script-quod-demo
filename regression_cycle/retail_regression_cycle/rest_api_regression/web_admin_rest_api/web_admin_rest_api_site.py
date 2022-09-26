from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.ret.REST_API.Web_Admin_REST.Site_API.QAP_T3571 import QAP_T3571
from test_cases.ret.REST_API.Web_Admin_REST.Site_API.QAP_T3572 import QAP_T3572
from test_cases.ret.REST_API.Web_Admin_REST.Site_API.QAP_T3580 import QAP_T3580
from test_cases.ret.REST_API.Web_Admin_REST.Site_API.QAP_T3581 import QAP_T3581
from test_cases.ret.REST_API.Web_Admin_REST.Site_API.QAP_T3583 import QAP_T3583
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event("WA_REST_API_Site", parent_id)
    configuration_admin_api_site = ComponentConfiguration("WA_REST_API_Site")
    try:
        QAP_T3571(report_id, configuration_admin_api_site.data_set,
                  configuration_admin_api_site.environment).execute()
        QAP_T3572(report_id, configuration_admin_api_site.data_set,
                  configuration_admin_api_site.environment).execute()
        QAP_T3580(report_id, configuration_admin_api_site.data_set,
                  configuration_admin_api_site.environment).execute()
        QAP_T3581(report_id, configuration_admin_api_site.data_set,
                  configuration_admin_api_site.environment).execute()
        QAP_T3583(report_id, configuration_admin_api_site.data_set,
                  configuration_admin_api_site.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
