from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3181 import QAP_T3181
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3193 import QAP_T3193
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3194 import QAP_T3194
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3195 import QAP_T3195
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3208 import QAP_T3208
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3209 import QAP_T3209
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3216 import QAP_T3216
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3259 import QAP_T3259
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3260 import QAP_T3260
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3302 import QAP_T3302
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8217 import QAP_T8217
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8218 import QAP_T8218
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8219 import QAP_T8219
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8220 import QAP_T8220
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8221 import QAP_T8221
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8222 import QAP_T8222
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8223 import QAP_T8223
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8246 import QAP_T8246
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8247 import QAP_T8247
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8248 import QAP_T8248
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8249 import QAP_T8249
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8250 import QAP_T8250
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8251 import QAP_T8251
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3315 import QAP_T3315
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3316 import QAP_T3316
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8107 import QAP_T8107
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8207 import QAP_T8207
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8208 import QAP_T8208
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8209 import QAP_T8209
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8210 import QAP_T8210
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8211 import QAP_T8211
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8212 import QAP_T8212
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8213 import QAP_T8213
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8214 import QAP_T8214
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8216 import QAP_T8216
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event("Trading_REST_API_BuyingPower", parent_id)
    configuration_trading_api_buying_power = ComponentConfiguration("Trading_REST_API_BuyingPower")
    try:
        QAP_T3181(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3193(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3194(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3195(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3208(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3209(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3216(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3259(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3260(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3302(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3315(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T3316(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8107(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8207(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8208(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8209(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8210(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8211(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8212(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8213(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8214(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8216(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8217(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8218(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8219(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8220(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8221(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8222(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8223(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8246(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8247(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8248(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8249(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8250(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
        QAP_T8251(report_id, configuration_trading_api_buying_power.data_set,
                  configuration_trading_api_buying_power.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
