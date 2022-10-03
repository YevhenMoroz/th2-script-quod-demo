from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.ret.REST_API.Trading_REST.Risk_Limits_API.QAP_T3141 import QAP_T3141
from test_cases.ret.REST_API.Trading_REST.Risk_Limits_API.QAP_T3505 import QAP_T3505
from test_cases.ret.REST_API.Trading_REST.Risk_Limits_API.QAP_T3506 import QAP_T3506
from test_cases.ret.REST_API.Trading_REST.Risk_Limits_API.QAP_T7744 import QAP_T7744
from test_cases.ret.REST_API.Trading_REST.Risk_Limits_API.QAP_T7745 import QAP_T7745
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Trading_REST_API_RiskLimits', parent_id)
    configuration_trading_api_risk_limits = ComponentConfiguration("Trading_REST_API_RiskLimits")
    try:
        QAP_T3141(report_id, configuration_trading_api_risk_limits.data_set,
                  configuration_trading_api_risk_limits.environment).execute()
        QAP_T3505(report_id, configuration_trading_api_risk_limits.data_set,
                  configuration_trading_api_risk_limits.environment).execute()
        QAP_T3506(report_id, configuration_trading_api_risk_limits.data_set,
                  configuration_trading_api_risk_limits.environment).execute()
        QAP_T7744(report_id, configuration_trading_api_risk_limits.data_set,
                  configuration_trading_api_risk_limits.environment).execute()
        QAP_T7745(report_id, configuration_trading_api_risk_limits.data_set,
                  configuration_trading_api_risk_limits.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
