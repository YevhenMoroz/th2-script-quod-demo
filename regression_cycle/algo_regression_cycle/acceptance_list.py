from stubs import Stubs, ROOT_DIR
from xml.etree import ElementTree

from win_gui_modules.utils import set_session_id
import logging
from getpass import getuser as get_pc_name
from datetime import datetime
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_TWAP.QAP_T4886 import QAP_T4886
from test_cases.algo.Algo_TWAP.QAP_T4935 import QAP_T4935
from test_cases.algo.Algo_TWAP.QAP_T4988 import QAP_T4988
from test_cases.algo.Algo_TWAP.QAP_T4884 import QAP_T4884
from test_cases.algo.Algo_TWAP.QAP_T4887 import QAP_T4887
from test_cases.algo.Algo_PercentageVolume.QAP_T4879 import QAP_T4879
from test_cases.algo.Algo_PercentageVolume.QAP_T4890 import QAP_T4890
from test_cases.algo.Algo_PercentageVolume.QAP_T4911 import QAP_T4911
from test_cases.algo.Algo_PercentageVolume import QAP_T4950
# from test_cases.algo.Algo_PercentageVolume.QAP_T5083 import QAP_T5083 # not automated yet
# from test_cases.algo.Algo_PercentageVolume.QAP_T5085 import QAP_T5085 # not automated yet
from test_cases.algo.Algo_PercentageVolume import QAP_T5113
from test_cases.algo.Algo_Multilisted import QAP_T4093
from test_cases.algo.Algo_Multilisted.QAP_T4091 import QAP_T4091
from test_cases.algo.Algo_Multilisted.QAP_T4120 import QAP_T4120
from test_cases.algo.Algo_Multilisted.QAP_T4115 import QAP_T4115
from test_cases.algo.Algo_Multilisted.QAP_T4106 import QAP_T4106
from test_cases.algo.Algo_Multilisted.QAP_T4114 import QAP_T4114
from test_cases.algo.Algo_Multilisted.QAP_T4117 import QAP_T4117
# from test_cases.algo.Algo_Multilisted.QAP_T4148 import QAP_T4148 not automated yet
from test_cases.algo.Algo_Iceberg.QAP_T4925 import QAP_T4925
from test_cases.algo.Algo_Iceberg.QAP_T4918 import QAP_T4918
from test_cases.algo.Algo_Iceberg.QAP_T4919 import QAP_T4919
from test_cases.algo.algo_acceptance_list import QAP_T4949 # Cannot find reference 'wrapper' in 'imported module test_cases'
from test_cases.algo.algo_acceptance_list import QAP_T4948 # Cannot find reference 'wrapper' in 'imported module test_cases'

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()



def test_run(parent_id=None, version=None):
    # pc_name = get_pc_name()  # getting PC name
    tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
    root = tree.getroot()
    full_ver = root.find(".//version").text
    ver = full_ver[-3:]
    # report_id_main = bca.create_event(f'[{pc_name}] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    report_id = bca.create_event('PDAT Acceptance v.' + ver + ' | ' + full_ver)
    logger.info(f"Root event was created (id = {report_id.id})")
    # session_id = set_session_id(pc_name) # grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated

    try:
        configuration = ComponentConfiguration("Acceptance_list")
        # TWAP
        QAP_T4886(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4935(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4988(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4884(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4887(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # POV
        QAP_T4879(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4890(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4911(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T5113.execute(report_id, session_id) # session ID error (line 44)
        # Iceberg
        QAP_T4925(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4918(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4919(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Multilisted
        QAP_T4120(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4106(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4114(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4117(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4115(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4091(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # TradLim and CumTradLim
        # QAP_T4949.execute(report_id, session_id) # session ID error (line 44)
        # QAP_T4948.execute(report_id, session_id) # session ID error (line 44)
    except Exception:
        logging.error("Error execution", exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
