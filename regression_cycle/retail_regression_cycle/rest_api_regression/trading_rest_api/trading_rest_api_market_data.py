from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.ret.REST_API.Trading_REST.MarketData_API.QAP_T3420 import QAP_T3420
from test_cases.ret.REST_API.Trading_REST.MarketData_API.QAP_T3611 import QAP_T3611
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_cases.ret.REST_API.Trading_REST.MarketData_API.QAP_T3190 import QAP_T3190

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Trading_REST_API_MarketData', parent_id)
    configuration_trading_api_md = ComponentConfiguration("Trading_REST_API_MarketData")
    try:
        QAP_T3190(report_id, configuration_trading_api_md.data_set,
                  configuration_trading_api_md.environment).execute()
        QAP_T3420(report_id, configuration_trading_api_md.data_set,
                  configuration_trading_api_md.environment).execute()
        QAP_T3611(report_id, configuration_trading_api_md.data_set,
                  configuration_trading_api_md.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
