from xml.etree import ElementTree

from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_Iceberg import QAP_3055, QAP_3054, QAP_3029, QAP_3056
from test_framework.core.environment import Environment
from test_framework.data_sets.environment_type import EnvironmentType
from test_framework.example_of_test_cases.QAP_4612_example import QAP_4612_example
from test_framework.data_sets.algo_data_set.algo_data_set import AlgoDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.oms_data_set.oms_data_set import OmsDataSet
from test_framework.data_sets.ret_data_set.ret_data_set import RetDataSet
from test_framework.data_sets.base_data_set import BaseDataSet

logging.basicConfig(format='%(asctime)s - %(message)s')
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']


def test_run(parent_id=None):
    logging.getLogger().setLevel(logging.WARN)


    try:
        report_id = bca.create_event('Algo', parent_id)
        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()
        environment = Environment.get_instance(EnvironmentType[root.find(".//component[@name='iceberg']/environment").text])
        data_set = eval(root.find(".//component[@name='iceberg']/data_set").text)()
        # example for demo
        QAP_4612_example(report_id=report_id, data_set=data_set, environment=environment).execute()

        # QAP_3056.execute(report_id=report_id)
        # QAP_3055.execute(report_id=report_id)
        # QAP_3054.execute(report_id=report_id)
        # QAP_3029.execute(report_id=report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
