import time
from datetime import timedelta, datetime

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_PairTrading.QAP_T4249 import QAP_T4249
from test_cases.algo.Algo_PairTrading.QAP_T7850 import QAP_T7850
from test_cases.algo.Algo_PairTrading.QAP_T7851 import QAP_T7851
from test_cases.algo.Algo_PairTrading.QAP_T8064 import QAP_T8064
from test_cases.algo.Algo_PairTrading.QAP_T8119 import QAP_T8119
from test_cases.algo.Algo_PairTrading.QAP_T8298 import QAP_T8298
from test_cases.algo.Algo_PairTrading.QAP_T8578 import QAP_T8578
from test_cases.algo.Algo_PairTrading.QAP_T8581 import QAP_T8581
from test_cases.algo.Algo_PairTrading.QAP_T8818 import QAP_T8818
from test_cases.algo.Algo_PairTrading.QAP_T9174 import QAP_T9174

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

def test_run(parent_id=None, version=None, mode=None):
    if mode == 'Regression':
        report_id = bca.create_event(f"Algo_PairTrading" if version is None else f"Algo_PairTrading | {version}", parent_id)
    else:
        report_id = bca.create_event(f"Algo_PairTrading" if version is None else f"Algo_PairTrading (verification) | {version}", parent_id)

    try:
        start_time = time.monotonic()
        print(f'Algo_PairTrading StartTime is {datetime.utcnow()}')
        # session_id = set_session_id()
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)
        configuration = ComponentConfiguration("Pair_trading")
        QAP_T4249(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7850(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7851(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T8064(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T8119(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8298(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8578(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8581(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8818(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9174(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        end_time = time.monotonic()
        print(f'Algo_PairTrading EndTime is {datetime.utcnow()}, duration is {timedelta(seconds=end_time-start_time)}')
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
