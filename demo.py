import logging
from getpass import getuser as get_pc_name
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3181 import QAP_T3181
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8249 import QAP_T8249
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8250 import QAP_T8250
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T8251 import QAP_T8251
from test_cases.ret.REST_API.Trading_REST.DMA_API.QAP_T3520 import QAP_T3520
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    # Generation id and time for test run
    pc_name = get_pc_name()  # getting PC name
    report_id = bca.create_event(f'[{pc_name}] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # endregion

    # ___WebAdmin REST API configuration block
    # configuration_site_admin_api = ComponentConfiguration("WA_REST_API_Site")
    # configuration_client_accounts_api = ComponentConfiguration("WA_REST_API_Client_Accounts")
    # configuration_risk_limits_admin_api = ComponentConfiguration("WA_REST_API_Risk_Limits")
    # configuration_positions_admin_api = ComponentConfiguration("WA_REST_API_Positions")
    # ___Trading REST API configuration block
    configuration_trading_api_dma = ComponentConfiguration("Trading_REST_API_Dma")
    # configuration_trading_api_md = ComponentConfiguration("Trading_REST_API_MarketData")
    # configuration_trading_api_risk_limit = ComponentConfiguration("Trading_REST_API_RiskLimits")
    #configuration_trading_api_buying_power = ComponentConfiguration("Trading_REST_API_BuyingPower")
    # configuration_trading_api_positions = ComponentConfiguration("Trading_REST_API_Positions")
    # configuration_trading_api_others = ComponentConfiguration("Trading_REST_API_Others")

    try:
        start = datetime.now()
        print(f'start time = {start}')
        QAP_T3520(report_id, configuration_trading_api_dma.data_set,
                            configuration_trading_api_dma.environment).execute()
        # __BuyingPower_SmokeTests__ block
        # QAP_T8249(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8250(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8251(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        print('duration time = ' + str(datetime.now() - start))
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()
