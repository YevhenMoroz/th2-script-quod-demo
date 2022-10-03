from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.ret.REST_API.Trading_REST.Others_API.QAP_T3458 import QAP_T3458
from test_cases.ret.REST_API.Trading_REST.Others_API.QAP_T3500 import QAP_T3500
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Trading_REST_API_Others', parent_id)
    configuration_trading_api_others = ComponentConfiguration("Trading_REST_API_Others")
    try:
        QAP_T3458(report_id, configuration_trading_api_others.data_set,
                  configuration_trading_api_others.environment).execute()
        QAP_T3500(report_id, configuration_trading_api_others.data_set,
                  configuration_trading_api_others.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
