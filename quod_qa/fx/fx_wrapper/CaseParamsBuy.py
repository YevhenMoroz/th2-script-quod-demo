from datetime import datetime
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from stubs import Stubs
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

class CaseParamsBuy():

    connectivity = 'fix-fh-314-luna'
    simulator = Stubs.test_sim
    market_d_params_spot=None
    market_d_params_fwd=None

    def __init__(self,case_id,defaultmdsymbol='EUR/USD:SPO:REG:HSBC',symbol='EUR/USD'
                 ,securityType='FXSPOT',settldate=tsd.spo()):
        self.case_id=case_id
        self.defaultmdsymbol=defaultmdsymbol
        self.symbol=symbol
        self.securityType=securityType
        self.settldate=settldate

        self.set_market_data_spot()
        self.set_market_data_fwd()

    def set_market_data_spot(self):
        self.market_d_params_spot = {
            "MDReqID": self.simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol=self.defaultmdsymbol,
                    connection_id=ConnectionID(session_alias=self.connectivity))).MDRefID,
            'Instrument': {
                'Symbol': self.symbol,
                'SecurityType': self.securityType
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19597,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': self.settldate,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19609,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': self.settldate,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19594,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': self.settldate,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19612,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': self.settldate,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19591,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    'SettlDate': self.settldate,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19615,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    'SettlDate': self.settldate,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }

    def set_market_data_fwd(self):
        self.market_d_params_fwd={
            "MDReqID": self.simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol=self.defaultmdsymbol,
                    connection_id=ConnectionID(session_alias=self.connectivity))).MDRefID,
            'Instrument': {
                'Symbol': self.symbol,
                'SecurityType': self.securityType
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19503,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryForwardPoints": '0.0000001',
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19603,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryForwardPoints": '0.0000001',
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19502,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    "MDEntryForwardPoints": '0.0000002',
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19604,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    "MDEntryForwardPoints": '0.0000002',
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19501,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    "MDEntryForwardPoints": '0.0000003',
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19605,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    "MDEntryForwardPoints": '0.0000003',
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }

    def prepare_custom_md_spot(self, no_md_entries):
        self.market_d_params_spot['NoMDEntries'].clear()
        self.market_d_params_spot['NoMDEntries']=no_md_entries
        return self

    def prepare_custom_md_fwd(self,no_md_entries):
        self.market_d_params_fwd['NoMDEntries'].clear()
        self.market_d_params_fwd['NoMDEntries']=no_md_entries
        return self
