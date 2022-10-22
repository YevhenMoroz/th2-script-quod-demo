from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3138 import QAP_T3138
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3139 import QAP_T3139
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3140 import QAP_T3140
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3178 import QAP_T3178
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3213 import QAP_T3213
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3353 import QAP_T3353
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3481 import QAP_T3481
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3482 import QAP_T3482
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3488 import QAP_T3488
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3130 import QAP_T3130
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event("WA_REST_API_Positions", parent_id)
    configuration_admin_api_positions = ComponentConfiguration("WA_REST_API_Positions")
    try:
        QAP_T3130(report_id, configuration_admin_api_positions.data_set,
                  configuration_admin_api_positions.environment).execute()
        QAP_T3138(report_id, configuration_admin_api_positions.data_set,
                  configuration_admin_api_positions.environment).execute()
        QAP_T3139(report_id, configuration_admin_api_positions.data_set,
                  configuration_admin_api_positions.environment).execute()
        QAP_T3140(report_id, configuration_admin_api_positions.data_set,
                  configuration_admin_api_positions.environment).execute()
        QAP_T3178(report_id, configuration_admin_api_positions.data_set,
                  configuration_admin_api_positions.environment).execute()
        QAP_T3213(report_id, configuration_admin_api_positions.data_set,
                  configuration_admin_api_positions.environment).execute()
        QAP_T3353(report_id, configuration_admin_api_positions.data_set,
                  configuration_admin_api_positions.environment).execute()
        QAP_T3481(report_id, configuration_admin_api_positions.data_set,
                  configuration_admin_api_positions.environment).execute()
        QAP_T3482(report_id, configuration_admin_api_positions.data_set,
                  configuration_admin_api_positions.environment).execute()
        QAP_T3488(report_id, configuration_admin_api_positions.data_set,
                  configuration_admin_api_positions.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
