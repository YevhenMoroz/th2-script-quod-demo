import logging
from getpass import getuser as get_pc_name
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.ret.REST_API.Trading_REST.BuyingPower_API.QAP_T3316 import QAP_T3316
from test_cases.ret.REST_API.Trading_REST.DMA_API.QAP_T3343 import QAP_T3343
from test_cases.ret.REST_API.Trading_REST.DMA_API.QAP_T3520 import QAP_T3520
from test_cases.ret.REST_API.Trading_REST.Risk_Limits_API.QAP_T3505 import QAP_T3505
from test_cases.ret.REST_API.Trading_REST.Risk_Limits_API.QAP_T3506 import QAP_T3506
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3642 import QAP_T3642
from test_cases.ret.REST_API.Web_Admin_REST.Client_Accounts_API.QAP_T3646 import QAP_T3646
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3139 import QAP_T3139
from test_cases.ret.REST_API.Web_Admin_REST.Positions_API.QAP_T3140 import QAP_T3140
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3128 import QAP_T3128
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T3203 import QAP_T3203
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T8618 import QAP_T8618
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T8620 import QAP_T8620
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T8621 import QAP_T8621
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T8622 import QAP_T8622
from test_cases.ret.REST_API.Web_Admin_REST.Risk_Limits_API.QAP_T8623 import QAP_T8623
from test_cases.ret.REST_API.Web_Admin_REST.risk_limit_dimension_deleter import RiskLimitDimensionDeleter
from test_cases.ret.REST_API.Web_Admin_REST.Users_API.QAP_T3609 import QAP_T3609
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

    # region ___WebAdmin REST API configuration block
    configuration_admin_api_site = ComponentConfiguration("WA_REST_API_Site")
    configuration_admin_api_users = ComponentConfiguration("WA_REST_API_Users")
    configuration_client_accounts_api = ComponentConfiguration("WA_REST_API_Client_Accounts")
    configuration_admin_api_risk_limits = ComponentConfiguration("WA_REST_API_Risk_Limits")
    configuration_admin_api_positions = ComponentConfiguration("WA_REST_API_Positions")
    # endregion

    # region ___Trading REST API configuration block
    configuration_trading_api_dma = ComponentConfiguration("Trading_REST_API_Dma")
    # configuration_trading_api_md = ComponentConfiguration("Trading_REST_API_MarketData")
    configuration_trading_api_risk_limit = ComponentConfiguration("Trading_REST_API_RiskLimits")
    configuration_trading_api_buying_power = ComponentConfiguration("Trading_REST_API_BuyingPower")
    #configuration_trading_api_positions = ComponentConfiguration("Trading_REST_API_Positions")
    # configuration_trading_api_others = ComponentConfiguration("Trading_REST_API_Others")
    # endregion

    try:
        start = datetime.now()
        print(f'start time = {start}')

        # region Trading API __BuyingPower__ block
        # QAP_T3315(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T3316(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # endregion

        # region Trading API __BuyingPower_SmokeTests__ block
        # QAP_T8207(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8208(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8209(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8210(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8211(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8212(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8213(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8218(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8223(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8249(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # QAP_T8250(report_id, configuration_trading_api_buying_power.data_set,
        #           configuration_trading_api_buying_power.environment).execute()
        # endregion

        # region Trading API __DMA__ block
        # QAP_T3343(report_id, configuration_trading_api_dma.data_set,
        #                     configuration_trading_api_dma.environment).execute()
        # QAP_T3520(report_id, configuration_trading_api_dma.data_set,
        #           configuration_trading_api_dma.environment).execute()
        # QAP_T3521(report_id, configuration_trading_api_dma.data_set,
        #                     configuration_trading_api_dma.environment).execute()
        # endregion

        # region Trading API __RiskLimit__ block
        # QAP_T3141(report_id, configuration_trading_api_risk_limit.data_set,
        #           configuration_trading_api_risk_limit.environment).execute()
        # QAP_T3505(report_id, configuration_trading_api_risk_limit.data_set,
        #           configuration_trading_api_risk_limit.environment).execute()
        # QAP_T3506(report_id, configuration_trading_api_risk_limit.data_set,
        #           configuration_trading_api_risk_limit.environment).execute()
        # endregion

        # region Admin API __Site__ block
        # QAP_T3580(report_id, configuration_admin_api_sute.data_set,
        #           configuration_admin_api_sute.environment).execute()
        # QAP_T3583(report_id, configuration_admin_api_sute.data_set,
        #           configuration_admin_api_sute.environment).execute()
        # QAP_T3581(report_id, configuration_admin_api_sute.data_set,
        #           configuration_admin_api_sute.environment).execute()
        # endregion

        # region Admin API __Users__ block
        # QAP_T3600(report_id, configuration_users_admin_api.data_set,
        #           configuration_users_admin_api.environment).execute()
        # QAP_T3601(report_id, configuration_users_admin_api.data_set,
        #           configuration_users_admin_api.environment).execute()
        # QAP_T3603(report_id, configuration_users_admin_api.data_set,
        #           configuration_users_admin_api.environment).execute()
        # QAP_T3604(report_id, configuration_users_admin_api.data_set,
        #           configuration_users_admin_api.environment).execute()
        # QAP_T3607(report_id, configuration_users_admin_api.data_set,
        #           configuration_users_admin_api.environment).execute()
        # QAP_T3609(report_id, configuration_admin_api_users.data_set,
        #           configuration_admin_api_users.environment).execute()
        # QAP_T3622(report_id, configuration_users_admin_api.data_set,
        #           configuration_users_admin_api.environment).execute()
        # endregion

        # region Admin API __RiskLimit__ block
        # RiskLimitDimensionDeleter(report_id, configuration_admin_api_risk_limits.data_set,
        #                           configuration_admin_api_risk_limits.environment).execute()
        # QAP_T3128(report_id, configuration_admin_api_risk_limits.data_set,
        #           configuration_admin_api_risk_limits.environment).execute()
        # QAP_T3203(report_id, configuration_admin_api_risk_limits.data_set,
        #           configuration_admin_api_risk_limits.environment).execute()
        # QAP_T8618(report_id, configuration_admin_api_risk_limits.data_set,
        #           configuration_admin_api_risk_limits.environment).execute()
        # QAP_T8620(report_id, configuration_admin_api_risk_limits.data_set,
        #           configuration_admin_api_risk_limits.environment).execute()
        # QAP_T8621(report_id, configuration_admin_api_risk_limits.data_set,
        #           configuration_admin_api_risk_limits.environment).execute()
        # QAP_T8622(report_id, configuration_admin_api_risk_limits.data_set,
        #           configuration_admin_api_risk_limits.environment).execute()
        # QAP_T8623(report_id, configuration_admin_api_risk_limits.data_set,
        #           configuration_admin_api_risk_limits.environment).execute()
        # endregion

        # region Admin API __Position__ block

        # QAP_T3139(report_id, configuration_admin_api_positions.data_set,
        #           configuration_admin_api_positions.environment).execute()
        # QAP_T3140(report_id, configuration_admin_api_positions.data_set,
        #           configuration_admin_api_positions.environment).execute()
        # endregion

        # region Admin API __Client/Accounts__ block
        QAP_T3642(report_id, configuration_client_accounts_api.data_set,
                  configuration_client_accounts_api.environment).execute()
        # QAP_T3646(report_id, configuration_client_accounts_api.data_set,
        #           configuration_client_accounts_api.environment).execute()
        # endregion

        print('duration time = ' + str(datetime.now() - start))
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()
