from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from getpass import getuser as get_pc_name
import time
from datetime import timedelta, datetime

from test_cases.algo.Algo_Multilisted.QAP_T8142 import QAP_T8142
from test_cases.algo.Algo_Multilisted.QAP_T4053 import QAP_T4053
from test_cases.algo.Algo_Multilisted.QAP_T4043 import QAP_T4043
from test_cases.algo.Algo_Multilisted.QAP_T4058 import QAP_T4058
from test_cases.algo.Algo_Multilisted.QAP_T4059 import QAP_T4059
from test_cases.algo.Algo_Multilisted.QAP_T4137 import  QAP_T4137
from test_cases.algo.Algo_Multilisted.QAP_T4121 import  QAP_T4121
from test_cases.algo.Algo_Multilisted.QAP_T4106 import  QAP_T4106
from test_cases.algo.Algo_Multilisted.QAP_T4104 import  QAP_T4104
from test_cases.algo.Algo_Multilisted.QAP_T4102 import  QAP_T4102
# from test_cases.algo.Algo_Multilisted.QAP_T4103 import  QAP_T4103
# from test_cases.algo.Algo_Multilisted.QAP_T4102 import  QAP_T4102
# from test_cases.algo.Algo_Multilisted.QAP_T4105 import  QAP_T4105
from test_cases.algo.Algo_Multilisted.QAP_T4084 import QAP_T4084
# from test_cases.algo.Algo_Multilisted import  QAP_T4148
from test_cases.algo.Algo_Multilisted import  QAP_T4093
from test_cases.algo.Algo_Multilisted.QAP_T4095 import QAP_T4095
from test_cases.algo.Algo_Multilisted.QAP_T4139 import QAP_T4139
from test_cases.algo.Algo_Multilisted.QAP_T4114 import QAP_T4114
from test_cases.algo.Algo_Multilisted.QAP_T4136 import QAP_T4136
from test_cases.algo.Algo_Multilisted.QAP_T4131 import QAP_T4131
from test_cases.algo.Algo_Multilisted.QAP_T4132 import QAP_T4132
from test_cases.algo.Algo_Multilisted.QAP_T4135 import QAP_T4135
from test_cases.algo.Algo_Multilisted.QAP_T4085 import QAP_T4085
# from test_cases.algo.Algo_Multilisted.QAP_T4142 import  QAP_T4142
from test_cases.algo.Algo_Multilisted.QAP_T4086 import QAP_T4086
# from test_cases.algo.Algo_Multilisted.QAP_T4143 import  QAP_T4143
from test_cases.algo.Algo_Multilisted.QAP_T4088 import QAP_T4088
# from test_cases.algo.Algo_Multilisted import QAP_T4145
from test_cases.algo.Algo_Multilisted.QAP_T4089 import QAP_T4089
# from test_cases.algo.Algo_Multilisted.QAP_T4146 import QAP_T4146
from test_cases.algo.Algo_Multilisted.QAP_T4090 import QAP_T4090
# from test_cases.algo.Algo_Multilisted.QAP_T4147 import QAP_T4147
from test_cases.algo.Algo_Multilisted.QAP_T4087 import QAP_T4087
# from test_cases.algo.Algo_Multilisted.QAP_T4144 import QAP_T4144
from test_cases.algo.Algo_Multilisted.QAP_T4120 import QAP_T4120
from test_cases.algo.Algo_Multilisted.QAP_T4115 import QAP_T4115
from test_cases.algo.Algo_Multilisted.QAP_T4116 import QAP_T4116
from test_cases.algo.Algo_Multilisted.QAP_T4138 import QAP_T4138
from test_cases.algo.Algo_Multilisted.QAP_T4117 import QAP_T4117
from test_cases.algo.Algo_Multilisted.QAP_T4118 import QAP_T4118
from test_cases.algo.Algo_Multilisted.QAP_T4129 import QAP_T4129
from test_cases.algo.Algo_Multilisted.QAP_T4130 import QAP_T4130
from test_cases.algo.Algo_Multilisted.QAP_T4128 import QAP_T4128
from test_cases.algo.Algo_Multilisted.QAP_T4094 import QAP_T4094
from test_cases.algo.Algo_Multilisted.QAP_T4119 import QAP_T4119
# from test_cases.algo.Algo_Multilisted.QAP_T4100 import QAP_T4100
# from test_cases.algo.Algo_Multilisted.QAP_T4101 import QAP_T4101
from test_cases.algo.Algo_Multilisted.QAP_T4099 import QAP_T4099
from test_cases.algo.Algo_Multilisted.QAP_T4098 import QAP_T4098
from test_cases.algo.Algo_Multilisted.QAP_T4097 import QAP_T4097
from test_cases.algo.Algo_Multilisted.QAP_T4096 import QAP_T4096
from test_cases.algo.Algo_Multilisted.QAP_T4091 import QAP_T4091
from test_cases.algo.Algo_Multilisted.QAP_T4140 import QAP_T4140
from test_cases.algo.Algo_Multilisted.QAP_T4110 import QAP_T4110
from test_cases.algo.Algo_Multilisted.QAP_T4111 import QAP_T4111
from test_cases.algo.Algo_Multilisted.QAP_T4127 import QAP_T4127
from test_cases.algo.Algo_Multilisted.QAP_T4126 import QAP_T4126
# from test_cases.algo.Algo_Multilisted.QAP_T4141 import QAP_T4141
from test_cases.algo.Algo_Multilisted.QAP_T4122 import QAP_T4122
from test_cases.algo.Algo_Multilisted.QAP_T4107 import QAP_T4107
from test_cases.algo.Algo_Multilisted.QAP_T4108 import QAP_T4108
from test_cases.algo.Algo_Multilisted.QAP_T4124 import QAP_T4124
from test_cases.algo.Algo_Multilisted.QAP_T4109 import QAP_T4109
from test_cases.algo.Algo_Multilisted.QAP_T4123 import QAP_T4123
from test_cases.algo.Algo_Multilisted.QAP_T4092 import QAP_T4092
from test_cases.algo.Algo_Multilisted.QAP_T4876 import QAP_T4876
from test_cases.algo.Algo_Multilisted.QAP_T8431 import QAP_T8431
from test_cases.algo.Algo_Multilisted.QAP_T8432 import QAP_T8432
from test_cases.algo.Algo_Multilisted.QAP_T4100 import QAP_T4100
from test_cases.algo.Algo_Multilisted.QAP_T4101 import QAP_T4101

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

def test_run(parent_id= None, version = None, mode = None):
    if mode == 'Regression':
        report_id = bca.create_event(f"Algo_Multilisted" if version is None else f"Algo_Multilisted | {version}", parent_id)
    else:
        report_id = bca.create_event(f"Algo_Multilisted" if version is None else f"Algo_Multilisted (verification) | {version}", parent_id)

    try:
        start_time = time.monotonic()
        print(f'Algo_Multilisted StartTime is {datetime.utcnow()}')

        configuration = ComponentConfiguration("Multilisted")
        QAP_T4053(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4137(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4121(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4106(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4104(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4102(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4084(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T4093.execute(report_id) session ID not filled
        QAP_T4095(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4139(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4114(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4136(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4131(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4132(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4135(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4085(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4086(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4088(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4089(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4090(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4087(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4120(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4138(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4117(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4118(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4129(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4130(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4128(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4094(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4119(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4099(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4098(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4097(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4096(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4091(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4110(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4111(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4127(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4126(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4122(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4107(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4108(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4124(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4109(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4123(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4092(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4115(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4116(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8432(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8431(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4876(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8142(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4058(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4059(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4140(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4100(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4101(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        if __name__ == '__main__':
            QAP_T4043(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        end_time = time.monotonic()
        print(f'Algo_Multilisted EndTime is {datetime.utcnow()}, duration is {timedelta(seconds=end_time-start_time)}')

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
