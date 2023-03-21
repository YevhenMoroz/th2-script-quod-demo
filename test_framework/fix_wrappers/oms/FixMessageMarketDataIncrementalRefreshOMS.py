from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

from stubs import Stubs
from test_framework.data_sets.constants import TradingPhases
from test_framework.fix_wrappers.FixMessageMarketDataIncrementalRefresh import FixMessageMarketDataIncrementalRefresh
from datetime import datetime


class FixMessageMarketDataIncrementalRefreshAlgo(FixMessageMarketDataIncrementalRefresh):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_market_data_incr_refresh(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '704',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3_000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_incr_refresh_ltq(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '704',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '3',
                    'SecurityTradingStatus': '3',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self


    def set_market_data_incr_refresh_indicative(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '704',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': 'Q',
                    'MDEntryPx': '40',
                    'MDEntrySize': '1000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '3',
                    'SecurityTradingStatus': '3',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_close_price(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '704',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '5',
                    'MDEntryPx': '40',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '5',
                    'SecurityTradingStatus': '3',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def get_MDReqID(self, symbol: str, session_alias: str):
        list_MDRefID = Stubs.simulator_equity.getAllMDRefID(request=RequestMDRefID(
            symbol=symbol,
            connection_id=ConnectionID(session_alias=session_alias)
        )).PairsMDRefID
        for field in list_MDRefID:
            if field.symbol == symbol:
                return field.MDRefID
        return None

    def update_MDReqID(self, symbol: str, session_alias: str, type=None) -> FixMessageMarketDataIncrementalRefresh:
        md_req_id = self.get_MDReqID(symbol, session_alias)
        if md_req_id is None:
            raise Exception(f'No MDReqID at TH2 simulator for symbol {symbol} at {session_alias}')
        self.change_parameter("MDReqID", md_req_id)
        return self

    def set_phase(self, phase: TradingPhases) -> FixMessageMarketDataIncrementalRefresh:
        str_phase = ""
        if phase == TradingPhases.PreClosed:
            str_phase = '4'
        elif phase == TradingPhases.PreOpen:
            str_phase = '2'
        elif phase == TradingPhases.Open:
            str_phase = '3'
        elif phase == TradingPhases.Closed:
            str_phase = '1'
        elif phase == TradingPhases.AtLast:
            str_phase = '5'
        elif phase == TradingPhases.Expiry:
            str_phase = '9'
        elif phase == TradingPhases.Auction:
            str_phase = '6'
        super().update_value_in_repeating_group("NoMDEntriesIR",  "TradingSessionSubID", str_phase)
        return self

    def set_market_data_incr_refresh_open_px(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '704',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '4',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '3',
                    'SecurityTradingStatus': '3',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_incr_refresh_close_px(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '704',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '5',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '3',
                    'SecurityTradingStatus': '3',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_incr_refresh_high_px(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '704',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '7',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '3',
                    'SecurityTradingStatus': '3',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_incr_refresh_intraday_auc(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '704',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': 'Q',
                    'MDEntryPx': '40',
                    'MDEntrySize': '1000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '6',
                    'SecurityTradingStatus': '6',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_incr_refresh_open_auc(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '704',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': 'Q',
                    'MDEntryPx': '40',
                    'MDEntrySize': '1000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '2',
                    'SecurityTradingStatus': '3',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_incr_refresh_low_px(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '704',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '8',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '3',
                    'SecurityTradingStatus': '3',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self
