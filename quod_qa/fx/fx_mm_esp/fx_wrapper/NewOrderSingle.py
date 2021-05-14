from quod_qa.fx.fx_mm_esp.fx_wrapper.CaseParams import CaseParams
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs





class NewOrderSingle():
    new_order=None
    price=0
    checkpoint=None
    case_params = None
    fix_act = Stubs.fix_act
    verifier = Stubs.verifier
    # check_order_status=None

    def __init__(self, case_params=CaseParams):
        self.case_params=case_params

    # Send New Order Single
    def send_new_order_single(self,price):
        self.price=price
        order_params = {
            'Account': self.case_params.account,
            'HandlInst': self.case_params.handlinstr,
            'Side': self.case_params.side,
            'OrderQty': self.case_params.orderqty,
            'TimeInForce': self.case_params.timeinforce,
            'Price': price,
            'OrdType': self.case_params.ordtype,
            'ClOrdID': self.case_params.clordid,
            'TransactTime': datetime.utcnow().isoformat(),
            'SettlType': self.case_params.settltype,
            'SettlDate': self.case_params.settldate,
            'Instrument': {
                'Symbol': self.case_params.symbol,
                'SecurityType': self.case_params.securitytype,
                'Product': self.case_params.product,
            },
            'Currency': self.case_params.currency
        }
        tif = self.prepeare_tif()
        self.new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new order ' + tif, self.case_params.connectivity, self.case_params.case_id,
                bca.message_to_grpc('NewOrderSingle', order_params, self.case_params.connectivity)
            ))
        return self




    def verify_order_pending(self,):
        self.checkpoint = self.new_order.checkpoint_id
        ex_rep_pending = {
            'HandlInst': self.case_params.handlinstr,
            'Side': self.case_params.side,
            'TimeInForce': self.case_params.timeinforce,
            'OrdType': self.case_params.ordtype,
            'OrderCapacity': 'A',
            'Currency': self.case_params.currency,
            'Instrument': {
                'Symbol': self.case_params.symbol,
                'SecurityIDSource': self.case_params.securityidsource,
                'SecurityID': self.case_params.securityid,
                'Product': self.case_params.product,
                'SecurityExchange': self.case_params.securityexchange
            },
            'ExecID': '*',
            'ClOrdID': self.case_params.clordid,
            'OrderID': self.new_order.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'OrderQty': self.case_params.orderqty,
            'Price': self.price,
            'SettlCurrency': self.case_params.settlcurrency,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'ExecType': 'A',
            'NoParty': [{
                'PartyID': '*',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'LeavesQty': self.case_params.orderqty
        }
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Pending',
                bca.filter_to_grpc('ExecutionReport', ex_rep_pending, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params.connectivity, self.case_params.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_new(self):
        ex_rep_new = {
            # 'Account': self.case_params.account,
            'HandlInst': self.case_params.handlinstr,
            'Side': self.case_params.side,
            'TimeInForce': self.case_params.timeinforce,
            'OrdType': self.case_params.ordtype,
            'OrderCapacity': 'A',
            'Currency': self.case_params.currency,
            'Instrument': {
                'Symbol': self.case_params.symbol,
                'SecurityIDSource': self.case_params.securityidsource,
                'SecurityID': self.case_params.securityid,
                'Product': self.case_params.product,
                'SecurityExchange': self.case_params.securityexchange
            },
            'ExecID': '*',
            'ClOrdID': self.case_params.clordid,
            'OrderID': self.new_order.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'SettlDate': self.case_params.settldate.split(' ')[0],
            'SettlType': self.case_params.settltype,
            'QtyType': '0',
            'OrderQty': self.case_params.orderqty,
            'Price': self.price,
            'SettlCurrency': self.case_params.settlcurrency,
            'AvgPx': '0',
            'OrdStatus': '0',
            'ExecType': '0',
            'NoParty': [{
                'PartyID': '*',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'LeavesQty': self.case_params.orderqty,
            'ExecRestatementReason':'4'
        }
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = New',
                bca.filter_to_grpc('ExecutionReport', ex_rep_new, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params.connectivity, self.case_params.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_filled(self, account):
        final_ex_report = {
            'Account': account,
            'HandlInst': self.case_params.handlinstr,
            'Side': self.case_params.side,
            'TimeInForce': self.case_params.timeinforce,
            'OrdType': self.case_params.ordtype,
            'OrderCapacity': 'A',
            'Currency': self.case_params.currency,
            'Instrument': {
                'Symbol': self.case_params.symbol,
                'SecurityType':self.case_params.securitytype,
                'SecurityIDSource': self.case_params.securityidsource,
                'SecurityID':self.case_params.securityid,
                'Product': self.case_params.product,
                'SecurityExchange': self.case_params.securityexchange
            },
            'ClOrdID': self.case_params.clordid,
            'OrderID': '*',
            'ExecID': '*',
            'TransactTime': '*',
            'LastSpotRate': self.price,
            'LastQty': self.case_params.orderqty,
            'CumQty': self.case_params.orderqty,
            'QtyType': '0',
            'Price': self.price,
            'OrderQty': self.case_params.orderqty,
            'LastPx': self.price,
            'AvgPx': self.price,
            'OrdStatus': '2',
            'ExecType': 'F',
            'LeavesQty': '0',
            'SettlType': self.case_params.settltype,
            'SettlDate': self.case_params.settldate.split(' ')[0],
            'SettlCurrency': self.case_params.settlcurrency,
            'TradeDate': '*',
            'ExDestination': 'XQFX',
            'GrossTradeAmt': '*',
            'NoParty': [{
                'PartyID': '*',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }]
        }
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled' ,
                bca.filter_to_grpc('ExecutionReport', final_ex_report, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params.connectivity, self.case_params.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_rejected(self,text):
        final_ex_report = {
            'HandlInst': self.case_params.handlinstr,
            'Side': self.case_params.side,
            'TimeInForce': self.case_params.timeinforce,
            'OrdType': self.case_params.ordtype,
            'OrderCapacity': 'A',
            'Currency': self.case_params.currency,
            'Instrument': {
                'Symbol': self.case_params.symbol,
                'SecurityIDSource': self.case_params.securityidsource,
                'SecurityID': self.case_params.securityid,
                'Product': self.case_params.product,
                'SecurityExchange': self.case_params.securityexchange
            },
            'ClOrdID': self.case_params.clordid,
            'OrderID': '*',
            'ExecID': '*',
            'TransactTime': '*',
            'LastQty': '*',
            'CumQty': '0',
            'QtyType': '0',
            'Price': self.price,
            'OrderQty': self.case_params.orderqty,
            'LastPx': '0',
            'Text':text,
            'AvgPx': '0',
            'OrdStatus': '8',
            'ExecType': '8',
            'ExecRestatementReason':'4',
            'LeavesQty': '0',
            'SettlType': self.case_params.settltype,
            'SettlDate': self.case_params.settldate.split(' ')[0],
            'SettlCurrency': self.case_params.settlcurrency,
            'NoParty': [{
                'PartyID': '*',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }]
        }
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Rejected',
                bca.filter_to_grpc('ExecutionReport', final_ex_report, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params.connectivity, self.case_params.case_id
            ),
            timeout=3000
        )
        return self

    def check_order_status(self, ord_status):
        if ord_status=='Filled':
            return '2'
        elif ord_status=='Rejected':
            return '8'
        else:
            return '0'

    def prepeare_tif(self):
        if self.case_params.timeinforce == '4':
            return 'Fill or Kill'
        elif self.case_params.timeinforce == '3':
            return 'Immediate or Cancel'
        elif self.case_params.timeinforce == '0':
            return 'Day'
        elif self.case_params.timeinforce == '1':
            return 'Good till Cancel'
        pass