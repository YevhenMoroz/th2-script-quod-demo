import time

from custom import basic_custom_actions as bca
from stubs import Stubs

class FixClientBuy():
    fix_act = Stubs.fix_act
    case_params_buy = None

    def __init__(self, case_params_buy):
        self.case_params_buy=case_params_buy


    def send_market_data_spot(self):
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                self.case_params_buy.connectivity,
                self.case_params_buy.case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', self.case_params_buy.market_d_params_spot,
                                    self.case_params_buy.connectivity)))
        time.sleep(2)

    def send_market_data_fwd(self):
        tenor = self.case_params_buy.defaultmdsymbol[11:15]
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send Market Data '+tenor,
                self.case_params_buy.connectivity,
                self.case_params_buy.case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', self.case_params_buy.market_d_params_fwd,
                                    self.case_params_buy.connectivity)))
        time.sleep(2)
