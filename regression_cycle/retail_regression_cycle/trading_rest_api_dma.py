from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.ret.REST_API.Trading_REST.DMA_API.QAP_T3520 import QAP_T3520
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Trading_REST_API_Dma', parent_id)
    configuration_trading_api_dma = ComponentConfiguration("Trading_REST_API_Dma")
    try:
        QAP_T3520(report_id, configuration_trading_api_dma.data_set,
                  configuration_trading_api_dma.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
