import logging
import time

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4832 import QAP_T4832
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4837 import QAP_T4837
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4908 import QAP_T4908
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4818 import QAP_T4818
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4819 import QAP_T4819
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4820 import QAP_T4820
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4888 import QAP_T4888
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4881 import QAP_T4881
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4865 import QAP_T4865
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4864 import QAP_T4864
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4863 import QAP_T4863
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4862 import QAP_T4862
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4860 import QAP_T4860
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4858 import QAP_T4858
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4857 import QAP_T4857
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4855 import QAP_T4855
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4853 import QAP_T4853
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4851 import QAP_T4851
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4852 import QAP_T4852
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4849 import QAP_T4849
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4843 import QAP_T4843
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4845 import QAP_T4845
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4847 import QAP_T4847
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4842 import QAP_T4842
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4841 import QAP_T4841
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4840 import QAP_T4840
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4838 import QAP_T4838
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4836 import QAP_T4836
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4835 import QAP_T4835
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4833 import QAP_T4833
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4830 import QAP_T4830
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4831 import QAP_T4831
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4825 import QAP_T4825
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4817 import QAP_T4817
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4829 import QAP_T4829
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4823 import QAP_T4823
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4827 import QAP_T4827
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T8155 import QAP_T8155
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4812 import QAP_T4812
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4805 import QAP_T4805
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4804 import QAP_T4804
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4875 import QAP_T4875
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4892 import QAP_T4892
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4737 import QAP_T4737
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4709 import QAP_T4709
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4920 import QAP_T4920
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4921 import QAP_T4921
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4922 import QAP_T4922
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4923 import QAP_T4923

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"MultipleEmulation" if version is None else f"MultipleEmulation (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Multiple emulation
        configuration = ComponentConfiguration("Multiple_emulation")
        QAP_T4737(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4804(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4805(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4812(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4817(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4818(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4819(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(10)
        QAP_T4820(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4823(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4825(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4827(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4829(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4830(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4831(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4832(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4833(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4835(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4836(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4837(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4838(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4840(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4841(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4842(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4843(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4845(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4847(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4849(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4851(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4852(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4853(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4855(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4857(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4858(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4860(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4862(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4863(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4864(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4865(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(10)
        QAP_T4875(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4881(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4888(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4892(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4908(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8155(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        #region Additional tests
        QAP_T4709(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4920(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4921(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4922(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4923(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()