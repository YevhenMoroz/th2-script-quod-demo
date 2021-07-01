from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from custom.tenor_settlement_date import get_expire_time
from quod_qa.fx.fx_wrapper.common import parse_settl_type


class CaseParamsSellRfq:

    connectivityRFQ = 'fix-ss-rfq-314-luna-standard'
    rfq_params = None
    rfq_params_swap = None
    quote_cancel= None
    quote_params = None
    # quote_cancel_params = None
    order_params = None
    order_exec_report = None
    order_pending = None
    order_new = None
    order_filled = None
    order_rejected = None
    order_algo_rejected = None

    def __init__(self, client, case_id, side='', orderqty=1, ordtype='D', timeinforce='4', currency='EUR',
                 settlcurrency='USD', settltype=0, settldate='', symbol='EUR/USD', securitytype='FXSPOT',
                 securityid='EUR/USD',securityidsource='8',handlinstr='1', securityexchange='XQFX', product=4,
                 market_depth='0', md_update_type='0', account='', ttl=120, booktype='0'
                 ):
        self.client = client
        self.case_id = case_id
        self.handlinstr = handlinstr
        self.side = side
        self.orderqty = orderqty
        self.ordtype = ordtype
        self.timeinforce = timeinforce
        self.currency = currency
        self.settlcurrency = settlcurrency
        self.settltype = settltype
        self.settldate = settldate
        self.symbol = symbol
        self.securitytype = securitytype
        self.securityidsource = securityidsource
        self.securityid = securityid
        self.securityexchange = securityexchange
        self.product = product
        self.market_depth = market_depth
        self.md_update_type = md_update_type
        self.account = account
        self.ttl = ttl
        self.booktype=booktype
        self.mdreqid = bca.client_orderid(10)
        self.clordid = bca.client_orderid(9)
        self.quote_reqid = bca.client_orderid(9)

        self.set_new_order_single_params()
        self.set_order_exec_rep_params()
        self.set_rfq_params()
        self.set_rfq_params_swap()
        self.set_quote_params()

    def set_rfq_params(self):
        self.rfq_params = {
            'QuoteReqID': self.quote_reqid,
            'NoRelatedSymbols': [{
                'Account': self.client,
                'Side': self.side,
                'Instrument': {
                    'Symbol': self.symbol,
                    'SecurityType': self.securitytype
                },
                'SettlDate': self.settldate,
                'SettlType': self.settltype,
                'Currency': self.currency,
                'QuoteType': '1',
                'OrderQty': self.orderqty,
                'OrdType': 'D'
                # 'ExpireTime': (datetime.now() + timedelta(seconds=self.ttl)).strftime("%Y%m%d-%H:%M:%S.000"),
                # 'TransactTime': (datetime.utcnow().isoformat())
            }
            ]
        }

    # QAP_2143
    def set_rfq_params_swap(self):
        self.rfq_params_swap = {
            'QuoteReqID': self.quote_reqid,
            'NoRelatedSymbols': [
                {
                    'Account': self.client,
                    'Currency': self.currency,
                    'OrderQty': self.orderqty,
                    'Instrument': {
                        'Symbol': self.symbol,
                        'SecurityType': self.securitytype
                    },
                    'NoLegs': [
                        {
                            'InstrumentLeg': {
                                'LegSymbol': 'instrument',
                                'LegSecurityType': 'FXSPOT'
                            },
                            'LegSide': 1,
                            'LegSettlType': 0,
                            'LegSettlDate': 'self.near_leg_settldate',
                            'LegOrderQty': 1000000
                        },
                        {
                            'InstrumentLeg': {
                                'LegSymbol': 'instrument',
                                'LegSecurityType': 'FXFWD'
                            },
                            'LegSide': 2,
                            'LegSettlType': 7,
                            'LegSettlDate': 'self.far_leg_settldate',
                            'LegOrderQty': 1000000
                        }
                    ]
                }
            ]
        }

    def set_quote_params(self):
        self.quote_params = {
            'QuoteReqID': self.rfq_params['QuoteReqID'],
            'OfferPx': '*',
            'BidPx': '*',
            'OfferSize': '*',
            'BidSize': '*',
            'QuoteID': '*',
            'QuoteMsgID': '*',
            'OfferSpotRate': '*',
            'BidSpotRate': '*',
            'ValidUntilTime': '*',
            'Currency': self.currency,
            'QuoteType': self.rfq_params['NoRelatedSymbols'][0]['QuoteType'],
            'Instrument': '*',
            'SettlDate': '*',
            'SettlType': '*',
            'Account': '*',

        }

    def set_quote_cancel_params(self):
        self.quote_cancel = {
            'QuoteReqID': self.rfq_params['QuoteReqID'],
            'QuoteID': '*',
            'QuoteCancelType': '5',
        }

    # Set New Order Single parameters
    def set_new_order_single_params(self):
        self.order_params = {
            'Account': self.client,
            'HandlInst': self.handlinstr,
            'Side': self.side,
            'OrderQty': self.orderqty,
            'TimeInForce': self.timeinforce,
            'Price': '',
            'QuoteID': '',
            'OrdType': self.ordtype,
            'ClOrdID': self.clordid,
            'TransactTime': datetime.utcnow().isoformat(),
            'SettlType': self.settltype,
            'SettlDate': self.settldate,
            'Instrument': {
                'Symbol': self.symbol,
                'SecurityType': self.securitytype,
                'Product': self.product,
            },
            'Currency': self.currency
        }

    # Set parameters for verification new order Pending responce
    def set_order_exec_rep_params(self):
        def_order_exec_report = {
            'HandlInst': self.handlinstr,
            'Side': self.side,
            'TimeInForce': self.timeinforce,
            'OrdType': self.ordtype,
            'OrderCapacity': 'A',
            'Currency': self.currency,
            'Instrument': {
                'Symbol': self.symbol,
                'SecurityIDSource': self.securityidsource,
                'SecurityID': self.securityid,
                'Product': self.product,
                'SecurityExchange': self.securityexchange
            },
            'ExecID': '*',
            'ClOrdID': self.clordid,
            'OrderID': '',
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'OrderQty': self.orderqty,
            'Price': '*',
            'SettlCurrency': self.settlcurrency,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'ExecType': 'A',
            'NoParty': [{
                'PartyID': '*',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'LeavesQty': self.orderqty
        }
        self.order_exec_report = def_order_exec_report

        # Prepera order perding report


    #PREPARING

    # Prepare  requset params
    def prepare_rfq_params(self):
        if self.side=='':
            self.rfq_params['NoRelatedSymbols'][0].pop('Side')

    # Prepare  order pending report
    def prepare_order_pending_report(self):
        self.set_order_exec_rep_params()
        self.order_pending = self.order_exec_report
        self.order_pending['Account'] = self.client
        self.order_pending['OrdStatus'] = 'A'
        self.order_pending['OrderID'] = '*'
        self.order_pending['OrderQty'] = self.order_params['OrderQty']
        self.order_pending['LeavesQty'] = self.order_params['OrderQty']

    # Prepare  order new report
    def prepare_order_new_report(self):
        self.set_order_exec_rep_params()
        self.order_new = self.order_exec_report
        self.order_new['Account'] = self.client
        self.order_new['OrdStatus'] = '0'
        self.order_new['ExecType'] = '0'
        self.order_new['SettlDate'] = self.settldate.split(' ')[0]
        self.order_new['SettlType'] = self.settltype
        self.order_new['ExecRestatementReason'] = '4'

    # Prepare  order filled report
    def prepare_order_filled_report(self):
        self.set_order_exec_rep_params()
        self.order_filled = self.order_exec_report
        self.order_filled['Account'] = self.account
        self.order_filled['OrdStatus'] = '2'
        self.order_filled['ExecType'] = 'F'
        self.order_filled['SpotSettlDate'] = tsd.spo()
        self.order_filled['Instrument']['SecurityType'] = self.securitytype
        self.order_filled['SettlDate'] = self.settldate.split(' ')[0]
        self.order_filled['SettlType'] = self.settltype
        self.order_filled['LastQty'] = self.orderqty
        self.order_filled['CumQty'] = self.orderqty
        self.order_filled['LeavesQty'] = '0'
        self.order_filled['TradeDate'] = '*'
        self.order_filled['ExDestination'] = 'XQFX'
        self.order_filled['GrossTradeAmt'] = '*'
        # self.order_filled.pop('ExecRestatementReason')

    # Prepare  order rejected report
    def prepare_order_rejected_report(self):
        self.set_order_exec_rep_params()
        self.order_rejected = self.order_exec_report
        self.order_rejected['Account'] = self.client
        self.order_rejected['OrdStatus'] = '8'
        self.order_rejected['ExecType'] = '8'
        self.order_rejected['ExecRestatementReason'] = '4'
        self.order_rejected['LeavesQty'] = '0'
        self.order_rejected['SettlDate'] = self.settldate.split(' ')[0]
        self.order_rejected['SettlType'] = self.settltype
        self.order_rejected['OrderQty'] = self.order_params['OrderQty']

    # Prepare  order rejected report Alog
    def prepare_order_algo_rejected_report(self):
        self.set_order_exec_rep_params()
        self.prepare_order_rejected_report()
        self.order_algo_rejected = self.order_rejected
        self.order_algo_rejected.pop('SettlDate')
        self.order_algo_rejected['HandlInst'] = '2'
        self.order_algo_rejected['OrdRejReason'] = '99'
        self.order_algo_rejected['TargetStrategy'] = '*'
        self.order_algo_rejected.pop('ExecRestatementReason')
        self.order_algo_rejected['Instrument'].pop('SecurityIDSource')
        self.order_algo_rejected['Instrument'].pop('SecurityID')
        self.order_algo_rejected.pop('SettlType')

    # Prepare quote no side report
    def prepare_quote_report(self):
        if self.side=='1':
            self.quote_params['Side']='1'
            if self.symbol[0:3]==self.currency:
                self.quote_params.pop('BidSpotRate')
                self.quote_params.pop('BidSize')
                self.quote_params.pop('BidPx')
            if self.symbol[4:]==self.currency:
                self.quote_params.pop('OfferSpotRate')
                self.quote_params.pop('OfferSize')
                self.quote_params.pop('OfferPx')
            if self.rfq_params['NoRelatedSymbols'][0]['Instrument']['SecurityType']=='FXFWD':
                self.quote_params['OfferForwardPoints']='*'
        elif self.side=='2':
            self.quote_params['Side']='2'
            if self.symbol[0:3]==self.currency:
                self.quote_params.pop('OfferSpotRate')
                self.quote_params.pop('OfferSize')
                self.quote_params.pop('OfferPx')
            if self.symbol[4:]==self.currency:
                self.quote_params.pop('BidSpotRate')
                self.quote_params.pop('BidSize')
                self.quote_params.pop('BidPx')
            if self.rfq_params['NoRelatedSymbols'][0]['Instrument']['SecurityType']=='FXFWD':
                self.quote_params['BidForwardPoints']='*'
        elif self.side=='':
            if self.rfq_params['NoRelatedSymbols'][0]['Instrument']['SecurityType']=='FXFWD':
                self.quote_params['OfferForwardPoints'] = '*'
                self.quote_params['BidForwardPoints'] = '*'



    # def prepape_quote_cancel_report(self):
    #     self.quote_cancel_params = {
    #         'QuoteReqID': self.rfq_params['QuoteReqID'],
    #         'QuoteCancelType': '5',
    #         'NoQuoteEntries': [{
    #             'Instrument': {
    #                 'Symbol': self.symbol,
    #                 'SecurityType': self.securitytype
    #             },
    #         },
    #         ],
    #         'QuoteID': '*'
    #     }



