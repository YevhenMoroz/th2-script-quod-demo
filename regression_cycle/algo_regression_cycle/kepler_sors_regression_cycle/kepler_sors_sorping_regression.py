import logging
import time

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10336 import QAP_T10336
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10393 import QAP_T10393
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10416 import QAP_T10416
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10420 import QAP_T10420
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10421 import QAP_T10421
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10428 import QAP_T10428
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10912 import QAP_T10912
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10913 import QAP_T10913
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10948 import QAP_T10948
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10950 import QAP_T10950
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10981 import QAP_T10981
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10989 import QAP_T10989
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10990 import QAP_T10990
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T10991 import QAP_T10991
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4957 import QAP_T4957
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4959 import QAP_T4959
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9011 import QAP_T9011
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9166 import QAP_T9166
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9274 import QAP_T9274
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9305 import QAP_T9305
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9308 import QAP_T9308
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9309 import QAP_T9309
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9354 import QAP_T9354
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9355 import QAP_T9355
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9356 import QAP_T9356
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9357 import QAP_T9357
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9358 import QAP_T9358
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9359 import QAP_T9359
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9364 import QAP_T9364
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9365 import QAP_T9365
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4080 import QAP_T4080
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4224 import QAP_T4224
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4797 import QAP_T4797
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4798 import QAP_T4798
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4799 import QAP_T4799
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4800 import QAP_T4800
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4803 import QAP_T4803
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4806 import QAP_T4806
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4807 import QAP_T4807
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4873 import QAP_T4873
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4874 import QAP_T4874
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4876 import QAP_T4876
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4877 import QAP_T4877
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4905 import QAP_T4905
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4906 import QAP_T4906
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4932 import QAP_T4932
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T9198 import QAP_T9198
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4939 import QAP_T4939
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4940 import QAP_T4940
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4941 import QAP_T4941
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4944 import QAP_T4944
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4963 import QAP_T4963
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4966 import QAP_T4966
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4967 import QAP_T4967
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4969 import QAP_T4969
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4970 import QAP_T4970
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4971 import QAP_T4971
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4972 import QAP_T4972
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4973 import QAP_T4973
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4974 import QAP_T4974
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4975 import QAP_T4975
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4976 import QAP_T4976
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4977 import QAP_T4977
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4978 import QAP_T4978
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4979 import QAP_T4979
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4980 import QAP_T4980
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4981 import QAP_T4981
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4982 import QAP_T4982
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4983 import QAP_T4983
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4984 import QAP_T4984
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4985 import QAP_T4985
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4989 import QAP_T4989
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4995 import QAP_T4995
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4996 import QAP_T4996
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4997 import QAP_T4997
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4998 import QAP_T4998
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4999 import QAP_T4999
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5000 import QAP_T5000
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5001 import QAP_T5001
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5002 import QAP_T5002
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5003 import QAP_T5003
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5004 import QAP_T5004
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5063 import QAP_T5063
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5072 import QAP_T5072
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5073 import QAP_T5073
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5074 import QAP_T5074
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5076 import QAP_T5076
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5075 import QAP_T5075
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8704 import QAP_T8704
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8706 import QAP_T8706
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8788 import QAP_T8788
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8790 import QAP_T8790
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8815 import QAP_T8815
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8832 import QAP_T8832
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8855 import QAP_T8855
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8858 import QAP_T8858
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8862 import QAP_T8862
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8863 import QAP_T8863
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8878 import QAP_T8878
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T8879 import QAP_T8879


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Sorping" if version is None else f"SORPING (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region SORPING
        configuration = ComponentConfiguration("Sorping")
        QAP_T4080(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4224(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4797(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4798(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4799(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4800(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(10)
        QAP_T4803(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4806(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4807(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4873(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4874(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4876(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4877(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4905(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4906(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4932(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4939(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4940(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4941(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4944(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4957(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4959(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4963(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4966(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4967(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4969(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4970(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4971(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4972(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4973(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4974(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4975(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4976(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4977(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4978(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4979(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4980(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4981(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4982(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4983(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4984(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4985(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4989(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4995(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4996(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4997(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4998(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T4999(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T5000(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T5001(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T5002(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(10)
        QAP_T5003(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(10)
        QAP_T5004(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T5063(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T5072(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T5073(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(10)
        QAP_T5074(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T5075(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T5076(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8704(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8706(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8788(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8790(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8815(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8832(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8855(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8858(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8862(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8863(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(10)
        QAP_T8878(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T8879(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9011(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9166(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9198(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9274(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9305(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9308(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9309(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9354(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9355(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9356(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9357(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9358(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9359(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9364(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T9365(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10336(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10393(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10416(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10420(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10421(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10428(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10912(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10913(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10981(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10989(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10990(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(3)
        QAP_T10991(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()