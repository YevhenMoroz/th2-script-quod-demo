import logging
import time
from datetime import timedelta
from xml.etree import ElementTree

from custom import basic_custom_actions as bca
from regression_cycle.web_trading_cycle.run_account_summary import RunAccountSummary
from regression_cycle.web_trading_cycle.run_login_and_logout import RunLoginAndLogout
from regression_cycle.web_trading_cycle.run_order_ticket_and_book import RunOrderTicketAndBook
from regression_cycle.web_trading_cycle.run_other import RunOther
from regression_cycle.web_trading_cycle.run_positions import RunPositions
from regression_cycle.web_trading_cycle.run_trades import RunTrades
from regression_cycle.web_trading_cycle.run_user_profile import RunUserProfile
from regression_cycle.web_trading_cycle.run_watch_list import RunWatchList
from stubs import Stubs, ROOT_DIR

logging.basicConfig(format='%(asctime)s - %(message)s')
logging.getLogger().setLevel(logging.WARN)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Web Trading regression_cycle', parent_id)
    tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
    root = tree.getroot()
    try:
        start_time = time.monotonic()
        if eval(root.find(".//component[@name='WebTrading_Login_And_Logout']").attrib["run"]):
            RunLoginAndLogout(report_id).execute()
        if eval(root.find(".//component[@name='WebTrading_OrderTicket_And_Book']").attrib["run"]):
            RunOrderTicketAndBook(report_id).execute()
        if eval(root.find(".//component[@name='WebTrading_Other']").attrib["run"]):
            RunOther(report_id).execute()
        if eval(root.find(".//component[@name='WebTrading_Positions']").attrib["run"]):
            RunPositions(report_id).execute()
        if eval(root.find(".//component[@name='WebTrading_Trades']").attrib["run"]):
            RunTrades(report_id).execute()
        if eval(root.find(".//component[@name='WebTrading_UserProfile']").attrib["run"]):
            RunUserProfile(report_id).execute()
        if eval(root.find(".//component[@name='WebTrading_WatchList']").attrib["run"]):
            RunWatchList(report_id).execute()
        if eval(root.find(".//component[@name='WebTrading_Account_Summary']").attrib["run"]):
            RunAccountSummary(report_id).execute()


        end_time = time.monotonic()
        print("Test cases completed\n" +
              "~Total elapsed execution time~ = " + str(timedelta(seconds=end_time - start_time)))

    except Exception as e:
        print(e.__class__.__name__)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
