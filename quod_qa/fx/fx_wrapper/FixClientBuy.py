import time

from custom import basic_custom_actions as bca
from stubs import Stubs

class FixClientBuy():
    fix_act = Stubs.fix_act
    case_params_buy = None

    def __init__(self, case_params_buy):
        self.case_params_buy=case_params_buy


    def send_market_data_spot(self, even_name_custom=''):
        even_name = 'Send Market Data SPOT  '
        if even_name_custom!='':
            even_name=even_name_custom
        print(even_name, self.case_params_buy.market_d_params_spot)
        self.fix_act.sendMessage(
            bca.convert_to_request(
                even_name,
                self.case_params_buy.connectivity,
                self.case_params_buy.case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', self.case_params_buy.market_d_params_spot,
                                    self.case_params_buy.connectivity)))
        time.sleep(2)

    def send_market_data_fwd(self, even_name_custom=''):
        tenor = self.case_params_buy.defaultmdsymbol[11:15]
        even_name = 'Send Market Data FORWARD   '
        if even_name_custom!='':
            even_name=even_name_custom
        print(even_name,self.case_params_buy.market_d_params_fwd)
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send Market Data '+tenor,
                self.case_params_buy.connectivity,
                self.case_params_buy.case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', self.case_params_buy.market_d_params_fwd,
                                    self.case_params_buy.connectivity)))
        time.sleep(2)
