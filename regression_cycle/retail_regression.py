import logging
from xml.etree import ElementTree

from stubs import Stubs, ROOT_DIR
from custom import basic_custom_actions as bca
from regression_cycle.retail_regression_cycle import trading_rest_api_dma, trading_rest_api_market_data,\
    trading_rest_api_risk_limits, trading_rest_api_buying_power, trading_rest_api_others, \
    webadmin_rest_api_client_accounts, webadmin_rest_api_positions,  webadmin_rest_api_risk_limits
from test_framework.mobile_android_core.utils.driver import AppiumDriver
from regression_cycle.retail_regression_cycle.mobile_account import Mobile_Account
from regression_cycle.retail_regression_cycle.mobile_loginlogout import Mobile_LoginLogout
from regression_cycle.retail_regression_cycle.mobile_market import Mobile_Market
from regression_cycle.retail_regression_cycle.mobile_orderticket_orderbook import Mobile_OrderTicket_OrderBook
from regression_cycle.retail_regression_cycle.mobile_others import Mobile_Others
from regression_cycle.retail_regression_cycle.mobile_portfolio import Mobile_Portfolio

def test_run(parent_id=None):
    try:
        report_id = bca.create_event('Retail regression_cycle', parent_id)
        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()
        version = root.find(".//version").text
        logging.getLogger().setLevel(logging.WARN)

        # region __TradingRestApi__ block
        # if eval(root.find(".//component[@name='Trading_REST_API_Dma']").attrib["run"]):
        #     trading_rest_api_dma.test_run(report_id)
        # if eval(root.find(".//component[@name='Trading_REST_API_MarketData']").attrib["run"]):
        #     trading_rest_api_market_data.test_run(report_id)
        # if eval(root.find(".//component[@name='Trading_REST_API_Positions']").attrib["run"]):
        #     pass
        # if eval(root.find(".//component[@name='Trading_REST_API_RiskLimits']").attrib["run"]):
        #     trading_rest_api_risk_limits.test_run(report_id)
        # if eval(root.find(".//component[@name='Trading_REST_API_BuyingPower']").attrib["run"]):
        #     trading_rest_api_buying_power.test_run(report_id)
        # if eval(root.find(".//component[@name='Trading_REST_API_Others']").attrib["run"]):
        #     trading_rest_api_others.test_run(report_id)
        # # endregion
        #
        # # region __WebAdminRestApi__ block
        # if eval(root.find(".//component[@name='WA_REST_API_Site']").attrib["run"]):
        #     pass
        # if eval(root.find(".//component[@name='WA_REST_API_Users']").attrib["run"]):
        #     pass
        # if eval(root.find(".//component[@name='WA_REST_API_Client_Accounts']").attrib["run"]):
        #     webadmin_rest_api_client_accounts.test_run(report_id)
        # if eval(root.find(".//component[@name='WA_REST_API_Risk_Limits']").attrib["run"]):
        #     webadmin_rest_api_risk_limits.test_run(report_id)
        # if eval(root.find(".//component[@name='WA_REST_API_Positions']").attrib["run"]):
        #     webadmin_rest_api_positions.test_run(report_id)
        # if eval(root.find(".//component[@name='WA_REST_API_Others']").attrib["run"]):
        #     pass
        # endregion

        # # region __MobileAndroidRegression__ block
        driver = AppiumDriver()
        if eval(root.find(".//component[@name='Mobile_Account']").attrib["run"]):
            Mobile_Account(driver, report_id, version).execute()
        if eval(root.find(".//component[@name='Mobile_LoginLogout']").attrib["run"]):
            Mobile_LoginLogout(driver, report_id, version).execute()
        if eval(root.find(".//component[@name='Mobile_Market']").attrib["run"]):
            Mobile_Market(driver, report_id, version).execute()
        # if eval(root.find(".//component[@name='Mobile_OrderTicket_OrderBook']").attrib["run"]):
        #     Mobile_OrderTicket_OrderBook(driver, report_id, version).execute()
        if eval(root.find(".//component[@name='Mobile_Portfolio']").attrib["run"]):
            Mobile_Portfolio(driver, report_id, version).execute()
        # if eval(root.find(".//component[@name='Mobile_Others']").attrib["run"]):
        #     Mobile_Others(driver, report_id, version).execute()
        # # endregion

        # TODO: Add additional blocks for WebTrading and MobileTrading

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
