import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3083 import QAP_3083
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3118 import QAP_3118
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3125 import QAP_3125
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3159 import QAP_3159
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3160 import QAP_3160
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3161 import QAP_3161
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3162 import QAP_3162
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3164 import QAP_3164
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3166 import QAP_3166
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3167 import QAP_3167
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3169 import QAP_3169
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3171 import QAP_3171
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3173 import QAP_3173
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3175 import QAP_3175
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3181 import QAP_3181
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3182 import QAP_3182
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3183 import QAP_3183
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3184 import QAP_3184
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3186 import QAP_3186
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3188 import QAP_3188
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3189 import QAP_3189
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3191 import QAP_3191
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3193 import QAP_3193
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3195 import QAP_3195
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3197 import QAP_3197
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T8155 import QAP_T8155
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3216 import QAP_3216
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3272 import QAP_3272
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3273 import QAP_3273
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_3707 import QAP_3707

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None):
    # Generation id and time for test run
    report_id = bca.create_event('Multiple Emulation', parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Multiple emulation
        configuration = ComponentConfiguration("multiple_emulation")
        QAP_3083(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3118(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3125(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3159(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3160(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3161(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3162(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3164(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3166(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3167(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3169(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3171(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3173(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3175(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3181(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3182(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3183(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3184(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3186(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3188(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3189(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3191(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3193(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3195(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3197(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8155(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3216(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3272(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3273(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3707(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()