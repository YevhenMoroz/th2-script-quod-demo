from quod_qa.fx.fx_mm_esp.methods.CaseParams import CaseParams
from datetime import datetime
from custom import basic_custom_actions as bca






class NewOrderSingle():
    new_order=None
    price=0
    checkpoint=None
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
                'Product': self.case_params.product,
            },
            'Currency': self.case_params.currency
        }

        self.new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new FOK order', self.case_params.connectivity, self.case_params.case_id,
                bca.message_to_grpc('NewOrderSingle', order_params, self.case_params.connectivity)
            ))


    # Check Execution Repors for order
    def verify_order(self,ord_status,account):
        self.verify_order_pending()
        self.verify_order_new()
        self.verify_last_ex_report(ord_status,account)

    def verify_order_pending(self,):
        self.checkpoint = self.new_order.checkpoint_id
        ex_rep_pending = {
            'Account': self.case_params.account,
            'HandlInst': self.case_params.handlinstr,
            'Side': self.case_params.side,
            'TimeInForce': self.case_params.timeinforce,
            'OrdType': self.case_params.ordtype,
            'OrderCapacity': 'A',
            'Currency': self.case_params.currency,
            'Instrument': {
                'Symbol': self.case_params.symbol,
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
            },
            'ExecID': '*',
            'ClOrdID': self.case_params.clordid,
            'OrderID': self.new_order.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'SettlDate': self.case_params.settldate,
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

    def verify_last_ex_report(self,ord_status,account):
        order_status=self.check_order_status(ord_status)
        last_ex_report = {
            'Account': account,
            'HandlInst': self.case_params.handlinstr,
            'Side': self.case_params.side,
            'TimeInForce': self.case_params.timeinforce,
            'OrdType': self.case_params.ordtype,
            'OrderCapacity': 'A',
            'Currency': self.case_params.currency,
            'Instrument': {
                'Symbol': self.case_params.symbol,
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
                'Execution Report with OrdStatus = Filled',
                bca.filter_to_grpc('ExecutionReport', last_ex_report, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params.connectivity, self.case_params.case_id
            ),
            timeout=3000
        )

    def check_order_status(ord_status):
        if ord_status=='Filled':
            return '2'
        elif ord_status=='Rejected':
            return '8'
        else:
            return '0'