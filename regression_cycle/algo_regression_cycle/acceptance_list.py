from stubs import Stubs
import logging
from getpass import getuser as get_pc_name
from datetime import datetime
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_TWAP import QAP_T4886
from test_cases.algo.Algo_TWAP.QAP_T4935 import QAP_T4935
from test_cases.algo.Algo_TWAP.QAP_T4988 import QAP_T4988
from test_cases.algo.Algo_TWAP.QAP_T4884 import QAP_T4884
from test_cases.algo.Algo_TWAP.QAP_T4887 import QAP_T4887
from test_cases.algo.Algo_PercentageVolume import QAP_T4879
# from test_cases.algo.Algo_PercentageVolume.QAP_T5083 import QAP_T5083 not automated yet
# from test_cases.algo.Algo_PercentageVolume.QAP_T5085 import QAP_T5085 not automated yet
# from test_cases.algo.Algo_PercentageVolume import QAP_T5113  AttributeError: OtherTabDetails in File "C:\Users\yyutkin\PycharmProjects\th2-script-quod-demo\win_gui_modules\order_book_wrappers.py", line 630, in OtherTabDetails
#     def __init__(self, request: order_book_pb2.ManualExecutionDetails.OtherTabDetails):
from test_cases.algo.Algo_Multilisted.QAP_T4120 import QAP_T4120
from test_cases.algo.Algo_Multilisted.QAP_T4115 import QAP_T4115
from test_cases.algo.Algo_Multilisted.QAP_T4106 import QAP_T4106
from test_cases.algo.Algo_Multilisted.QAP_T4114 import QAP_T4114
from test_cases.algo.Algo_Multilisted.QAP_T4117 import QAP_T4117
# from test_cases.algo.Algo_Multilisted.QAP_T4148 import QAP_T4148 not automated yet
from test_cases.algo.Algo_Iceberg.QAP_T4925 import QAP_T4925
from test_cases.algo.Algo_Iceberg.QAP_T4918 import QAP_T4918
from test_cases.algo.Algo_Iceberg.QAP_T4919 import QAP_T4919

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    pc_name = get_pc_name()  # getting PC name
    report_id = bca.create_event(f'[{pc_name}] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        configuration = ComponentConfiguration("Acceptance_list")
        # TWAP
        # QAP_T4886.execute(report_id) check rules removing
        QAP_T4935(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4988(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4884(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4887(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # POV
        QAP_T4879.execute(report_id)
        # QAP_T5113.execute(report_id)
        # Multilisted
        QAP_T4120(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4115(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4106(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4114(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4117(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Iceberg
        QAP_T4925(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4918(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4919(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
