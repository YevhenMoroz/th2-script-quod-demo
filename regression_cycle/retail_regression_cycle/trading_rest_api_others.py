from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Others_Trading_API', parent_id)
    configuration_trading_api_others = ComponentConfiguration("Others_Trading_Api")
    try:
        pass
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
