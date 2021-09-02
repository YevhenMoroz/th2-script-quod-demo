from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from custom.tenor_settlement_date import spo_ndf, spo


class CaseParamsSellRfq:
    connectivityRFQ = 'fix-ss-rfq-314-luna-standard'
    connectivityDropCopy = "fix-sell-m-314luna-drop"
    rfq_params = None
    rfq_params_swap = None
    quote_cancel = None
    quote_params = None
    quote_params_swap = None
    quote_request_reject_params = None
    order_params = None
    order_multi_leg_params = None
    order_exec_report = None
    order_exec_report_swap = None
    order_pending = None
    order_new = None
    order_filled = None
    order_filled_drop_copy = None
    order_filled_swap = None
    order_rejected = None
    order_algo_rejected = None
    drop_filter_params = None

    def __init__(self, client, case_id , side:str='', leg1_side:str='', leg2_side:str='', orderqty=1, leg1_ordqty='', leg2_ordqty='',
                 ordtype='D', timeinforce='4', currency='EUR',
                 settlcurrency='USD', settltype=0, leg1_settltype=0, leg2_settltype=0, settldate='', leg1_settldate='',
                 leg2_settldate='', symbol='EUR/USD', leg1_symbol='',
                 leg2_symbol='', securitytype='FXSPOT', leg1_securitytype='', leg2_securitytype='',
                 securityid='EUR/USD', securityidsource='8', handlinstr='1', securityexchange='XQFX',
                 product=4, account='', ttl=120, internal_account='QUOD_1'
                 ):
        self.client = client
        self.case_id = case_id
        self.handlinstr = handlinstr
        self.side = side
        self.leg1_side = leg1_side
        self.leg2_side = leg2_side
        self.orderqty = orderqty
        self.leg1_ordqty = leg1_ordqty
        self.leg2_ordqty = leg2_ordqty
        self.ordtype = ordtype
        self.timeinforce = timeinforce
        self.currency = currency
        self.settlcurrency = settlcurrency
        self.settltype = settltype
        self.leg1_settltype = leg1_settltype
        self.leg2_settltype = leg2_settltype
        self.settldate = settldate
        self.leg1_settldate = leg1_settldate
        self.leg2_settldate = leg2_settldate
        self.symbol = symbol
        self.leg1_symbol = leg1_symbol
        self.leg2_symbol = leg2_symbol
        self.securitytype = securitytype
        self.leg1_securitytype = leg1_securitytype
        self.leg2_securitytype = leg2_securitytype
        self.securityidsource = securityidsource
        self.securityid = securityid
        self.securityexchange = securityexchange
        self.product = product
        self.account = account
        self.internal_account = internal_account
        self.ttl = ttl
        self.mdreqid = bca.client_orderid(10)
        self.clordid = bca.client_orderid(9)
        self.quote_reqid = bca.client_orderid(9)

        self.set_new_order_single_params()
        self.set_new_order_multi_leg_params()
        self.set_order_exec_rep_params()
        self.set_rfq_params()
        self.set_rfq_params_swap()
        self.set_quote_params()
        self.set_quote_params_swap()
        self.set_drop_pre_filter_params()

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

    def set_drop_pre_filter_params(self):
        self.drop_filter_params = {
            'header': {
                'MsgType': ('0', "NOT_EQUAL"),
                'TargetCompID': 'QUOD8',
                'SenderCompID': 'QUODFX_UAT'
            },
        }

    def set_quote_params(self):
        self.quote_params = {
            'QuoteReqID': self.rfq_params['QuoteReqID'],
            'OfferPx': '*',
            'BidPx': '*',
            'OfferSize': self.rfq_params['NoRelatedSymbols'][0]['OrderQty'],
            'BidSize': self.rfq_params['NoRelatedSymbols'][0]['OrderQty'],
            'QuoteID': '*',
            'QuoteMsgID': '*',
            'OfferSpotRate': '*',
            'BidSpotRate': '*',
            'ValidUntilTime': '*',
            'Currency': self.currency,
            'QuoteType': self.rfq_params['NoRelatedSymbols'][0]['QuoteType'],
            'Instrument': {
                'Symbol': self.rfq_params['NoRelatedSymbols'][0]['Instrument']['Symbol'],
                'SecurityType': self.rfq_params['NoRelatedSymbols'][0]['Instrument']['SecurityType'],
                'Product': self.product,
            },
            'SettlDate': self.rfq_params['NoRelatedSymbols'][0]['SettlDate'],
            'SettlType': self.rfq_params['NoRelatedSymbols'][0]['SettlType'],
            'Account': '*',

        }

    # QAP_2143

    def set_rfq_params_swap(self):
        self.rfq_params_swap = {
            'QuoteReqID': self.quote_reqid,
            'NoRelatedSymbols': [
                {
                    'Account': self.client,
                    'Side': self.side,
                    'Currency': self.currency,
                    'OrderQty': self.orderqty,
                    'Instrument': {
                        'Symbol': self.symbol,
                        'SecurityType': self.securitytype
                    },
                    'NoLegs': [
                        {
                            'InstrumentLeg': {
                                'LegSymbol': self.leg1_symbol,
                                'LegSecurityType': self.leg1_securitytype
                            },
                            'LegSide': self.leg1_side,
                            'LegSettlType': self.leg1_settltype,
                            'LegSettlDate': self.leg1_settldate,
                            'LegOrderQty': self.leg1_ordqty
                        },
                        {
                            'InstrumentLeg': {
                                'LegSymbol': self.leg2_symbol,
                                'LegSecurityType': self.leg2_securitytype
                            },
                            'LegSide': self.leg2_side,
                            'LegSettlType': self.leg2_settltype,
                            'LegSettlDate': self.leg2_settldate,
                            'LegOrderQty': self.leg2_ordqty
                        }
                    ]
                }
            ]
        }

    def set_quote_params_swap(self):
        self.quote_params_swap = {
            'Account': self.client,
            'QuoteReqID': self.rfq_params['QuoteReqID'],
            'QuoteID': '*',
            'QuoteMsgID': '*',
            'ValidUntilTime': '*',
            'Side': self.side,
            'BidSpotRate': '*',
            'OfferSpotRate': '*',
            'OfferPx': '*',
            'BidPx': '*',
            'OfferSize': self.orderqty,
            'BidSize': self.orderqty,
            'OfferSwapPoints': '*',
            'BidSwapPoints': '*',
            # 'Side': self.side,
            # 'SettlType': self.settltype,
            # 'SettlDate': self.settldate,
            'Currency': self.currency,
            'QuoteType': '1',
            'Instrument': {
                'Symbol': self.symbol,
                'SecurityType': self.securitytype,
                'Product': self.product,
            },
            'NoLegs': [
                {
                    'LegSide': self.leg1_side,
                    'LegBidPx': '*',
                    'LegOfferPx': '*',
                    'LegOrderQty': self.leg1_ordqty,
                    'LegSettlDate': self.leg1_settldate,
                    'LegSettlType': self.leg1_settltype,
                    'InstrumentLeg': {
                        'LegSymbol': '*',
                        'LegSecurityID': self.securityid,
                        'LegSecurityExchange': self.securityexchange,
                        'LegSecurityIDSource': self.securityidsource,
                    },
                    'LegOfferForwardPoints': '*',
                    'LegBidForwardPoints': '*'
                },
                {
                    'LegSide': self.leg2_side,
                    'LegBidPx': '*',
                    'LegOfferPx': '*',
                    'LegOrderQty': self.leg2_ordqty,
                    'LegSettlDate': self.leg2_settldate,
                    'LegSettlType': self.leg2_settltype,
                    'InstrumentLeg': {
                        'LegSymbol': '*',
                        'LegSecurityID': self.securityid,
                        'LegSecurityExchange': self.securityexchange,
                        'LegSecurityIDSource': self.securityidsource,
                    },
                    'LegOfferForwardPoints': '*',
                    'LegBidForwardPoints': '*'
                }
            ]
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

    def set_new_order_multi_leg_params(self):
        self.order_multi_leg_params = {
            'Account': self.client,
            'Side': self.leg2_side,
            'Instrument': {
                'Symbol': self.symbol,
                'SecurityType': self.securitytype,
                'Product': self.product
            },
            # 'SettlDate': tsd.spo(),
            # 'SettlType': '0',
            'QuoteID': '*',
            'ClOrdID': self.clordid,
            'OrdType': 'D',
            'TransactTime': (datetime.utcnow().isoformat()),
            'OrderQty': self.orderqty,
            'Currency': self.currency,
            'SettlCurrency': self.settlcurrency,
            'Price': '*',
            'TimeInForce': self.timeinforce,
            'NoLegs': [
                {
                    'InstrumentLeg': {
                        'LegSymbol': self.leg1_symbol,
                        'LegSecurityType': self.leg1_securitytype
                    },
                    # 'LegSide': self.leg1_side,
                    'LegSettlType': self.leg1_settltype,
                    'LegSettlDate': self.leg1_settldate,
                    # 'LegOrderQty': 1000000
                },
                {
                    'InstrumentLeg': {
                        'LegSymbol': self.leg2_symbol,
                        'LegSecurityType': self.leg2_securitytype
                    },
                    # 'LegSide': 2,
                    'LegSettlType': self.leg2_settltype,
                    'LegSettlDate': self.leg2_settldate,
                    # 'LegOrderQty': 1000000
                },
            ]
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
            'LeavesQty': self.orderqty,

        }
        self.order_exec_report = def_order_exec_report

        # Prepera order perding report

    def set_order_exec_rep_params_swap(self):
        def_order_exec_report = {
            'Account': self.account,
            'Side': self.leg2_side,
            'AvgPx': '*',
            'SettlCurrency': self.settlcurrency,
            'HandlInst': '1',
            'LeavesQty': '0',
            'LastSwapPoints': '*',
            'LastSpotRate': '*',
            'OrdStatus': '2',
            'TradeDate': tsd.today(),
            'SpotSettlDate': tsd.spo(),
            'SettlType': self.settltype,
            'ExecType': 'F',
            'Currency': self.currency,
            'ExecID': '*',
            'OrderID': '*',
            'TimeInForce': self.timeinforce,
            'OrderQty': self.orderqty,
            'LastQty': '*',
            'Instrument': {
                'Symbol': self.symbol,
                'SecurityType': 'FXSWAP',
                'SecurityExchange': 'XQFX',
                'SecurityID': self.symbol,
                'Product': '4',
                'SecurityIDSource': '8',
            },
            'NoParty': [{
                'PartyID': '*',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'CumQty': self.orderqty,
            'TransactTime': '*',
            'LastPx': '*',
            'OrdType': 'D',
            'ClOrdID': self.clordid,
            'OrderCapacity': 'A',
            'QtyType': '0',
            'Price': '*',
            'ExDestination': '*',
            'GrossTradeAmt': '*',
            'NoLegs': [
                {
                    'LegSide': self.leg1_side,
                    'LegLastQty': self.leg1_ordqty,
                    'LegOrderQty': self.leg1_ordqty,
                    'LegLastPx': '*',
                    'LegSettlDate': self.leg1_settldate,
                    'LegSettlType': self.leg1_settltype,
                    'InstrumentLeg': {
                        'LegSymbol': self.leg1_symbol,
                        'LegSecurityType': self.leg1_securitytype,
                        'LegSecurityID': self.leg1_symbol,
                        'LegSecurityExchange': '*',
                        'LegSecurityIDSource': '*',
                    },
                },
                {
                    'LegSide': self.leg2_side,
                    'LegLastQty': self.leg2_ordqty,
                    'LegOrderQty': self.leg2_ordqty,
                    'LegLastPx': '*',
                    'LegSettlDate': self.leg2_settldate,
                    'LegSettlType': self.leg2_settltype,
                    'InstrumentLeg': {
                        'LegSymbol': self.leg2_symbol,
                        'LegSecurityType': self.leg2_securitytype,
                        'LegSecurityID': self.leg2_symbol,
                        'LegSecurityExchange': '*',
                        'LegSecurityIDSource': '*',
                    },
                },
            ]
        }
        self.order_exec_report_swap = def_order_exec_report

        # Prepera order perding report

    def set_quote_request_reject_params(self):
        def_quote_request_reject_params = {
            'QuoteReqID': self.rfq_params['QuoteReqID'],
            'QuoteRequestRejectReason': '99',
            'NoRelatedSymbols': [
                {
                    'SettlType': self.settltype,
                    'OrdType': self.ordtype,
                    'SettlDate': self.settldate,
                    'Currency': self.currency,
                    'Side': self.side,
                    'Instrument': {
                        'SecurityType': self.securitytype,
                        'Symbol': self.symbol,
                    },
                    'QuoteType': '*',
                }
            ],
            'Text': '*'
        }
        self.quote_request_reject_params = def_quote_request_reject_params

    # PREPARING

    # Prepare  requset params
    def prepare_rfq_params(self):
        if self.side == '':
            self.rfq_params['NoRelatedSymbols'][0].pop('Side')

    def prepare_rfq_params_swap(self):
        if self.side == '':
            self.rfq_params_swap['NoRelatedSymbols'][0].pop('Side')
        if self.leg1_side == '':
            self.rfq_params_swap['NoRelatedSymbols'][0]['NoLegs'][0].pop('LegSide')
        if self.leg2_side == '':
            self.rfq_params_swap['NoRelatedSymbols'][0]['NoLegs'][1].pop('LegSide')

    # Prepare  order pending report
    def prepare_order_pending_report(self):
        self.set_order_exec_rep_params()
        self.order_pending = self.order_exec_report
        if self.securitytype == 'FXNDF':
            self.order_pending['Instrument']['MaturityDate'] = '*'
            self.order_pending['Instrument'].pop('Product')
        # self.order_pending['Account'] = self.client
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
        self.order_filled['Instrument']['SecurityType'] = self.securitytype
        self.order_filled['SettlType'] = self.settltype
        self.order_filled['SettlDate'] = self.settldate
        self.order_filled['SpotSettlDate'] = spo()
        self.order_filled['LastQty'] = self.orderqty
        self.order_filled['CumQty'] = self.orderqty
        self.order_filled['LeavesQty'] = '0'
        self.order_filled['TradeDate'] = tsd.today()
        self.order_filled['ExDestination'] = 'XQFX'
        self.order_filled['GrossTradeAmt'] = '*'
        if self.securitytype == 'FXNDF':
            self.order_filled['Instrument']['MaturityDate'] = '*'
            self.order_filled['Instrument'].pop('Product')
            self.order_filled['SpotSettlDate'] = spo_ndf()
        if self.securitytype == 'FXFWD':
            self.order_filled['SpotSettlDate'] = spo()
        # self.order_filled.pop('ExecRestatementReason')
        # Prepare  order filled report

    def prepare_order_filled_taker(self):
        self.set_order_exec_rep_params()
        self.order_filled_drop_copy = self.order_exec_report
        self.order_exec_report['ClOrdID'] = "*"
        self.order_exec_report.pop('OrdType')
        self.order_exec_report.pop('OrderID')
        self.order_exec_report.pop('OrderCapacity')
        self.order_exec_report.pop('QtyType')
        self.order_exec_report.pop('TimeInForce')
        self.order_exec_report.pop('HandlInst')
        self.order_exec_report.pop('NoParty')
        self.order_filled_drop_copy['Account'] = self.internal_account
        self.order_filled_drop_copy['OrdStatus'] = '2'
        self.order_filled_drop_copy['ExecType'] = 'F'
        self.order_filled_drop_copy['Instrument']['SecurityType'] = self.securitytype
        self.order_filled_drop_copy['SettlType'] = self.settltype
        self.order_filled_drop_copy['SettlDate'] = self.settldate
        self.order_filled_drop_copy['SpotSettlDate'] = spo()
        self.order_filled_drop_copy['LastQty'] = self.orderqty
        self.order_filled_drop_copy['CumQty'] = self.orderqty
        self.order_filled_drop_copy['LeavesQty'] = '0'
        self.order_filled_drop_copy['TradeDate'] = tsd.today()
        self.order_filled_drop_copy['GrossTradeAmt'] = '*'
        if self.order_filled_drop_copy == 'FXNDF':
            self.order_filled_drop_copy['Instrument']['MaturityDate'] = '*'
            self.order_filled_drop_copy['Instrument'].pop('Product')
            self.order_filled_drop_copy['SpotSettlDate'] = spo_ndf()
        if self.securitytype == 'FXFWD':
            self.order_filled_drop_copy['SpotSettlDate'] = spo()
    #     # self.order_filled.pop('ExecRestatementReason')
    #     # Prepare  order filled report

    def prepare_order_swap_filled_report(self):
        self.set_order_exec_rep_params_swap()
        self.order_filled_swap = self.order_exec_report_swap
        self.order_filled_swap['NoLegs'][0]['LegLastForwardPoints'] = '*'
        self.order_filled_swap['NoLegs'][1]['LegLastForwardPoints'] = '*'
        if self.leg1_settltype == '0':
            self.order_filled_swap['NoLegs'][0].pop('LegLastForwardPoints')

    # Prepare  order rejected report
    def prepare_order_rejected_report_rfq(self):
        self.set_order_exec_rep_params()
        self.order_rejected = self.order_exec_report
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
        self.prepare_order_rejected_report_rfq()
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
        if self.side == '1':
            self.quote_params['Side'] = '1'
            if self.symbol[0:3] == self.currency:
                self.quote_params.pop('BidSpotRate')
                self.quote_params.pop('BidSize')
                self.quote_params.pop('BidPx')
            if self.symbol[4:] == self.currency:
                self.quote_params.pop('OfferSpotRate')
                self.quote_params.pop('OfferSize')
                self.quote_params.pop('OfferPx')
            if self.rfq_params['NoRelatedSymbols'][0]['Instrument']['SecurityType'] == 'FXFWD' or \
                    self.rfq_params['NoRelatedSymbols'][0]['Instrument']['SecurityType'] == 'FXNDF':
                self.quote_params['OfferForwardPoints'] = '*'
        elif self.side == '2':
            self.quote_params['Side'] = '2'
            if self.symbol[0:3] == self.currency:
                self.quote_params.pop('OfferSpotRate')
                self.quote_params.pop('OfferSize')
                self.quote_params.pop('OfferPx')
            if self.symbol[4:] == self.currency:
                self.quote_params.pop('BidSpotRate')
                self.quote_params.pop('BidSize')
                self.quote_params.pop('BidPx')
            if self.rfq_params['NoRelatedSymbols'][0]['Instrument']['SecurityType'] == 'FXFWD' or \
                    self.rfq_params['NoRelatedSymbols'][0]['Instrument']['SecurityType'] == 'FXNDF':
                self.quote_params['BidForwardPoints'] = '*'
        elif self.side == '':
            if self.rfq_params['NoRelatedSymbols'][0]['Instrument']['SecurityType'] == 'FXFWD' or \
                    self.rfq_params['NoRelatedSymbols'][0]['Instrument']['SecurityType'] == 'FXNDF':
                self.quote_params['OfferForwardPoints'] = '*'
                self.quote_params['BidForwardPoints'] = '*'
        if self.securitytype == 'FXNDF':
            self.quote_params['Instrument']['MaturityDate'] = '*'
            self.quote_params['Instrument'].pop('Product')

    def prepare_quote_report_swap(self):
        # check difference between far and near leg to set offer_size = difference and bid_size = difference for UnEven swap (if we have float with value after dot != 0 we take whole value )
        if self.leg2_ordqty != self.leg1_ordqty:
            size = float(self.leg2_ordqty) - float(self.leg1_ordqty)
            if str(size).split('.')[1] == '0':
                self.quote_params_swap['OfferSize'] = str(size).split('.')[0]
                self.quote_params_swap['BidSize'] = str(size).split('.')[0]
            else:
                self.quote_params_swap['OfferSize'] = str(size)
                self.quote_params_swap['BidSize'] = str(size)

        # check if far leg = BUY => delete BID part from report and points from one of the legs
        if self.leg2_side == '1':
            if self.leg1_settltype=='0':
                self.quote_params_swap['NoLegs'][0].pop('LegOfferForwardPoints')
                self.quote_params_swap['NoLegs'][0].pop('LegBidForwardPoints')
            if self.side == '1':
                # Check if we send Currency 1 or Currency 2
                if self.symbol.split('/')[0] == self.currency:
                    self.quote_params_swap.pop('BidSwapPoints')
                    self.quote_params_swap.pop('BidSize')
                    self.quote_params_swap.pop('BidPx')
                else:
                    self.quote_params_swap.pop('OfferSwapPoints')
                    self.quote_params_swap.pop('OfferSize')
                    self.quote_params_swap.pop('OfferPx')

        # check if far leg = SELL => delete Offer part from report and points from one of the legs
        if self.leg2_side == '2':
            if self.leg1_settltype=='0':
                self.quote_params_swap['NoLegs'][0].pop('LegOfferForwardPoints')
                self.quote_params_swap['NoLegs'][0].pop('LegBidForwardPoints')
            if self.side == '2':
                # Check if we send Currency 1 or Currency 2
                if self.symbol.split('/')[0] == self.currency:
                    self.quote_params_swap.pop('OfferSwapPoints')
                    self.quote_params_swap.pop('OfferSize')
                    self.quote_params_swap.pop('OfferPx')
                else:
                    self.quote_params_swap.pop('BidSwapPoints')
                    self.quote_params_swap.pop('BidSize')
                    self.quote_params_swap.pop('BidPx')

        if self.side == '':
            self.quote_params_swap.pop('Side')
        #If we send request without side at all
        if self.leg1_side == '':
            self.quote_params_swap['NoLegs'][0].pop('LegSide')
            if self.leg1_settltype=='0':
                self.quote_params_swap['NoLegs'][0].pop('LegOfferForwardPoints')
                self.quote_params_swap['NoLegs'][0].pop('LegBidForwardPoints')
        if self.leg2_side == '':
            self.quote_params_swap['NoLegs'][1].pop('LegSide')
        # Specific part only for NDS
        if self.securitytype == 'FXNDS':
            self.quote_params_swap.pop('ValidUntilTime')
            self.quote_params_swap['NoLegs'][1]['InstrumentLeg']['LegMaturityDate'] = '*'

    def prepare_quote_reject_report(self):
        self.set_quote_request_reject_params()
        if self.securitytype=='FXSWAP':
            self.quote_request_reject_params['NoRelatedSymbols'][0].pop('SettlType')
            self.quote_request_reject_params['NoRelatedSymbols'][0].pop('OrdType')
            self.quote_request_reject_params['NoRelatedSymbols'][0].pop('SettlDate')
