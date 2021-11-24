from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca


class CaseParamsSellEsp:
    # connectivityESP = 'fix-ss-308-mercury-standard'
    connectivityESP = 'fix-sell-esp-m-314luna-stand'
    # mdreqid = None
    # clordid = None
    md_params = None
    order_params = None
    md_subscribe_response = None
    md_reject_response = None
    order_exec_report = None
    order_pending = None
    order_new = None
    order_filled = None
    order_rejected = None
    order_algo_rejected = None

    def __init__(self, client, case_id, side='1', orderqty=1, ordtype='2', timeinforce='4', currency='EUR',
                 settlcurrency='USD', settltype=0, settldate='', symbol='EUR/USD', securitytype='FXSPOT',
                 securityid='EUR/USD',securityidsource='8',handlinstr='1', securityexchange='XQFX', product=4,
                 market_depth='0', md_update_type='0', account='', booktype='0'
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
        self.booktype=booktype
        self.mdreqid = bca.client_orderid(10)
        self.clordid = bca.client_orderid(9)
        self.quote_reqid = bca.client_orderid(9)
        self.set_market_data_params()
        self.set_new_order_single_params()
        self.set_md_subscribe_response()
        self.set_order_exec_rep_params()

    # Set market data request parameters
    def set_market_data_params(self):
        self.md_params = {
            'SenderSubID': self.client,
            'MDReqID': self.mdreqid,
            'MarketDepth': self.market_depth,
            'MDUpdateType': self.md_update_type,
            'BookType': self.booktype,
            'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
            'NoRelatedSymbols': [
                {
                    'Instrument': {
                        'Symbol': self.symbol,
                        'SecurityType': self.securitytype,
                        'Product': self.product
                    },
                    'SettlDate': self.settldate,
                    'SettlType': self.settltype
                }
            ]
        }
        if self.settltype!='B':
            self.md_params['NoRelatedSymbols'][0].pop('SettlDate')

    # Set New Order Single parameters
    def set_new_order_single_params(self):
        self.order_params = {
            'Account': self.client,
            'HandlInst': self.handlinstr,
            'Side': self.side,
            'OrderQty': self.orderqty,
            'TimeInForce': self.timeinforce,
            'Price': '',
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

    # Defaulf band with qty=1M for verification
    def set_md_subscribe_response(self):
        self.md_subscribe_response = {
            'MDReqID': self.mdreqid,
            'Instrument': {
                'Symbol': self.symbol
            },
            'OrigMDArrivalTime':'*',
            'LastUpdateTime': '*',
            'OrigMDTime':'*',
            'MDTime': '*',
            'NoMDEntries': [
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '1000000',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': '',
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 1,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '1000000',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': '',
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 1,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                }


            ]
        }

    def set_md_reject_response(self,text):
        self.md_reject_response = {
            'MDReqID': self.mdreqid,
            'MDReqRejReason': '3',
            'Text': text
        }
        return self


    # Set custom parameters for md verification
    def prepare_md_for_verification(self, qty_count, published=True, which_bands_not_pb=None, priced=True,
                                    which_bands_not_pr=None):
        if len(qty_count) > 0:
            a = len(qty_count)
            band = 0
            row_pub = 0
            row_prc = 0
            check_pub = 0
            check_price = 0
            self.md_subscribe_response['NoMDEntries'].clear()
            md_entry_position = 1
            for qty in qty_count:
                b = qty
                md_entry_type = 0
                while md_entry_type < 2:
                    self.md_subscribe_response['NoMDEntries'].append({
                        'SettlType': self.settltype,
                        'MDEntryPx': '*',
                        'MDEntryTime': '*',
                        'MDEntryID': '*',
                        'MDEntrySize': qty,
                        'QuoteEntryID': '*',
                        'MDOriginType': 1,
                        'SettlDate': self.settldate.split(' ')[0],
                        'MDQuoteType': 1,
                        'MDEntryPositionNo': md_entry_position,
                        'MDEntryDate': '*',
                        'MDEntryType': md_entry_type
                    })
                    if self.securitytype == 'FXFWD':
                        self.md_subscribe_response['NoMDEntries'][band]['MDEntryForwardPoints'] = '*'
                        self.md_subscribe_response['NoMDEntries'][band]['MDEntrySpotRate'] = '*'
                    if published == False:
                        if which_bands_not_pb == None:
                            self.md_subscribe_response['NoMDEntries'][band]['MDQuoteType'] = '0'
                        else:
                            if qty != which_bands_not_pb[row_pub]:
                                self.md_subscribe_response['NoMDEntries'][band]['MDQuoteType'] = '1'
                            if qty == which_bands_not_pb[row_pub]:
                                self.md_subscribe_response['NoMDEntries'][band]['MDQuoteType'] = '0'
                                check_pub += 1

                    if priced == False:
                        if which_bands_not_pr == None:
                            self.md_subscribe_response['NoMDEntries'][band]['QuoteCondition'] = 'B'
                        elif qty == which_bands_not_pr[row_prc]:
                            self.md_subscribe_response['NoMDEntries'][band]['QuoteCondition'] = 'B'
                            check_price += 1

                    md_entry_type += 1
                    band += 1
                md_entry_position += 1
                if check_pub != 0:
                    row_pub += 1
                if check_price != 0:
                    row_prc += 1

    def prepare_md_for_verification_custom(self, no_md_entries):
        self.md_subscribe_response['NoMDEntries'].clear()
        self.md_subscribe_response['NoMDEntries'] = no_md_entries
        return self

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

    # Prepera order pending report
    def prepare_order_pending_report(self):
        self.set_order_exec_rep_params()
        self.order_pending = self.order_exec_report
        self.order_pending['OrdStatus'] = 'A'
        self.order_pending['OrderQty'] = self.order_params['OrderQty']
        self.order_pending['LeavesQty'] = self.order_params['OrderQty']
        # self.order_pending['Account'] = self.order_params['Account']

    # Prepera order new report
    def prepare_order_new_report(self):
        self.set_order_exec_rep_params()
        self.order_new = self.order_exec_report
        # self.order_new['Account'] = self.client
        self.order_new['OrdStatus'] = '0'
        self.order_new['ExecType'] = '0'
        self.order_new['SettlDate'] = self.settldate.split(' ')[0]
        self.order_new['SettlType'] = self.settltype
        self.order_new['ExecRestatementReason'] = '4'

    # Prepera order filled report
    def prepare_order_filled_report(self):
        self.set_order_exec_rep_params()
        self.order_filled = self.order_exec_report
        # self.order_filled['Account'] = self.order_params['Account']
        self.order_filled['Account'] = self.account
        self.order_filled['OrdStatus'] = '2'
        self.order_filled['ExecType'] = 'F'
        self.order_filled['Instrument']['SecurityType'] = self.securitytype
        self.order_filled['SettlDate'] = self.settldate.split(' ')[0]
        self.order_filled['SettlType'] = self.settltype
        self.order_filled['LastQty'] = self.orderqty
        self.order_filled['CumQty'] = self.orderqty
        self.order_filled['LeavesQty'] = '0'
        self.order_filled['LastMkt'] = 'XQFX'
        self.order_filled['TradeDate'] = '*'
        self.order_filled['SpotSettlDate'] = '*'
        self.order_filled['ExDestination'] = 'XQFX'
        self.order_filled['GrossTradeAmt'] = '*'
        # self.order_filled.pop('Client')
        # self.order_filled.pop('ExecRestatementReason')

    # Prepera order rejected report
    def prepare_order_rejected_report_esp(self):
        self.set_order_exec_rep_params()
        self.order_rejected = self.order_exec_report
        self.order_rejected['OrdStatus'] = '8'
        self.order_rejected['ExecType'] = '8'
        self.order_rejected['ExecRestatementReason'] = '4'
        self.order_rejected['LeavesQty'] = '0'
        self.order_rejected['SettlDate'] = self.settldate.split(' ')[0]
        self.order_rejected['SettlType'] = self.settltype
        self.order_rejected['OrderQty'] = self.order_params['OrderQty']

    # Prepera order rejected report Alog
    def prepare_order_algo_rejected_report(self):
        self.set_order_exec_rep_params()
        self.prepare_order_rejected_report_esp()
        self.order_algo_rejected = self.order_rejected
        self.order_algo_rejected.pop('SettlDate')
        self.order_algo_rejected['HandlInst'] = '2'
        self.order_algo_rejected['OrdRejReason'] = '99'
        self.order_algo_rejected['TargetStrategy'] = '*'
        self.order_algo_rejected['StrategyName'] = '*'
        self.order_algo_rejected.pop('ExecRestatementReason')
        self.order_algo_rejected['Instrument'].pop('SecurityIDSource')
        self.order_algo_rejected['Instrument'].pop('SecurityID')
        self.order_algo_rejected.pop('SettlType')
