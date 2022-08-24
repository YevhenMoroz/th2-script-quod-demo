from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_Multilisted import QAP_T4122, QAP_T4091, QAP_T4084, QAP_T4085, QAP_T4086, QAP_T4116,\
    QAP_T4087, QAP_T4876, QAP_T4088, QAP_T4089, QAP_T4090
from test_cases.algo.Algo_Multilisted.QAP_T4139 import QAP_T4139
from test_cases.algo.Algo_Multilisted.QAP_T4138 import QAP_T4138
from test_cases.algo.Algo_Multilisted.QAP_T4137 import QAP_T4137
from test_cases.algo.Algo_Multilisted.QAP_T4136 import QAP_T4136
from test_cases.algo.Algo_Multilisted.QAP_T4135 import QAP_T4135
from test_cases.algo.Algo_Multilisted.QAP_T4132 import QAP_T4132
from test_cases.algo.Algo_Multilisted.QAP_T4131 import QAP_T4131
from test_cases.algo.Algo_Multilisted.QAP_T4130 import QAP_T4130
from test_cases.algo.Algo_Multilisted.QAP_T4129 import QAP_T4129
from test_cases.algo.Algo_Multilisted.QAP_T4128 import QAP_T4128
from test_cases.algo.Algo_Multilisted.QAP_T4127 import QAP_T4127
from test_cases.algo.Algo_Multilisted.QAP_T4126 import QAP_T4126
from test_cases.algo.Algo_Multilisted.QAP_T4124 import QAP_T4124
from test_cases.algo.Algo_Multilisted.QAP_T4123 import QAP_T4123
from test_cases.algo.Algo_Multilisted.QAP_T4122 import QAP_T4122
from test_cases.algo.Algo_Multilisted.QAP_T4121 import QAP_T4121
from test_cases.algo.Algo_Multilisted.QAP_T4120 import QAP_T4120
from test_cases.algo.Algo_Multilisted.QAP_T4119 import QAP_T4119
from test_cases.algo.Algo_Multilisted.QAP_T4118 import QAP_T4118
from test_cases.algo.Algo_Multilisted.QAP_T4117 import QAP_T4117
from test_cases.algo.Algo_Multilisted.QAP_T4116 import QAP_T4116
from test_cases.algo.Algo_Multilisted.QAP_T4115 import QAP_T4115
from test_cases.algo.Algo_Multilisted.QAP_T4114 import QAP_T4114
from test_cases.algo.Algo_Multilisted.QAP_T4111 import QAP_T4111
from test_cases.algo.Algo_Multilisted.QAP_T4110 import QAP_T4110
from test_cases.algo.Algo_Multilisted.QAP_T4109 import QAP_T4109
from test_cases.algo.Algo_Multilisted.QAP_T4108 import QAP_T4108
from test_cases.algo.Algo_Multilisted.QAP_T4106 import QAP_T4106
from test_cases.algo.Algo_Multilisted.QAP_T4104 import QAP_T4104
from test_cases.algo.Algo_Multilisted.QAP_T4102 import QAP_T4102
from test_cases.algo.Algo_Multilisted.QAP_T4099 import QAP_T4099
from test_cases.algo.Algo_Multilisted.QAP_T4098 import QAP_T4098
from test_cases.algo.Algo_Multilisted.QAP_T4097 import QAP_T4097
from test_cases.algo.Algo_Multilisted.QAP_T4096 import QAP_T4096
from test_cases.algo.Algo_Multilisted.QAP_T4094 import QAP_T4094

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

def test_run(parent_id= None):
    report_id = bca.create_event('Algo', parent_id)
    try:
        configuration = ComponentConfiguration("Multilisted")
        QAP_T4139(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4138(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4137(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4136(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4135(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4132(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4131(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4130(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4129(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4128(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4127(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4126(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4124(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4123(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4122(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4121(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4120(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4119(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4118(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4117(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4116(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4115(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4114(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4111(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4110(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4109(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4108(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4106(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4104(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4102(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4099(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4098(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4097(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4096(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4094(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4091.execute(report_id)
        QAP_T4090.execute(report_id)
        QAP_T4089.execute(report_id)
        QAP_T4088.execute(report_id)
        QAP_T4087.execute(report_id)
        QAP_T4086.execute(report_id)
        QAP_T4085.execute(report_id)
        QAP_T4084.execute(report_id)
        QAP_T4876.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
