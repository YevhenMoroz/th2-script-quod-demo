from custom import basic_custom_actions as bca
from quod_qa.fx.fx_wrapper.common import check_order_status, prepeare_tif
from stubs import Stubs
import time


class FixClientSellRfq():
    fix_act = Stubs.fix_act
    verifier = Stubs.verifier
    quote = None
    case_params_sell_rfq = None
    new_order=None
    quote_response=None
    price=''

    def __init__(self, case_params_sell_rfq):
        self.case_params_sell_rfq=case_params_sell_rfq

    #ACTIONS

    #Send RFQ
    def send_request_for_quote(self):
        self.case_params_sell_rfq.prepare_rfq_params()
        self.quote = self.fix_act.placeQuoteFIX(
            bca.convert_to_request(
                'Send Request For Quote',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteRequest', self.case_params_sell_rfq.rfq_params, self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    #Send RFQ
    def send_request_for_quote_swap(self):
        self.quote = self.fix_act.placeQuoteFIX(
            bca.convert_to_request(
                'Send Request For Quote',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteRequest', self.case_params_sell_rfq.rfq_params_swap, self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    #Send New Order Single
    def send_new_order_single(self,price):
        tif = prepeare_tif(self.case_params_sell_rfq.timeinforce)
        self.case_params_sell_rfq.order_params['Price'] = price
        self.new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new order ' + tif, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('NewOrderSingle', self.case_params_sell_rfq.order_params, self.case_params_sell_rfq.connectivityESP)
            ))
        return self

    def send_new_order_single_timeout(self,price):
        tif = prepeare_tif(self.case_params_sell_rfq.timeinforce)
        self.case_params_sell_rfq.order_params['Price'] = price
        self.new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new order ' + tif, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('NewOrderSingle', self.case_params_sell_rfq.order_params, self.case_params_sell_rfq.connectivityESP),5
            ))
        return self

    #Extract filed by name
    def extruct_filed(self, field, band_number=1):
        if field.lower()=='price':
            self.price = self.subscribe.response_messages_list[0].fields['NoMDEntries'] \
                .message_value.fields['NoMDEntries'].list_value.values[band_number] \
                .message_value.fields['MDEntryPx'].simple_value
            return self.price
        elif field.lower()=='mdentryid':
            mdEntryId = self.subscribe.response_messages_list[0].fields['NoMDEntries'] \
                .message_value.fields['NoMDEntries'].list_value.values[band_number] \
                .message_value.fields['MDEntryID'].simple_value
            return mdEntryId
        elif field.lower()=='mdentryforwardpoints':
            mdentryforwardpoints = self.subscribe.response_messages_list[0].fields['NoMDEntries'] \
                .message_value.fields['NoMDEntries'].list_value.values[band_number] \
                .message_value.fields['MDEntryForwardPoints'].simple_value
            return mdentryforwardpoints


    #VERIFICATION

    # Check Market Data respons was received
    def verify_quote_pending(self):
        time.sleep(3)
        self.quote_response = self.verifier.submitCheckRule(
            bca.create_check_rule('Receive quote',
                bca.filter_to_grpc('Quote', self.case_params_sell_rfq.quote_params, ['QuoteReqID']),
                self.quote.checkpoint_id,
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id
            )
        )
        return self

    def verify_order_pending(self,price='', qty=''):
        self.case_params_sell_rfq.prepape_order_pending_report()
        self.case_params_sell_rfq.order_pending['Price'] = self.price
        if price != '':
            self.case_params_sell_rfq.order_pending['Price'] = price
        if qty !='':
            self.case_params_sell_rfq.order_pending['OrderQty']=qty
            self.case_params_sell_rfq.order_pending['LeavesQty']=qty
        self.case_params_sell_rfq.order_pending['OrderID']=self.new_order.response_messages_list[0].fields['OrderID'].simple_value
        self.checkpoint = self.new_order.checkpoint_id
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Pending',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_pending, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_new(self):
        self.case_params_sell_rfq.prepape_order_new_report()
        self.case_params_sell_rfq.order_new['Price']=self.price
        self.case_params_sell_rfq.order_new['OrderID']=self.new_order.response_messages_list[0].fields['OrderID'].simple_value
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = New',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_new, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_filled(self,price='', qty=''):
        self.case_params_sell_rfq.prepape_order_filled_report()
        self.case_params_sell_rfq.order_filled['Price']=self.price
        self.case_params_sell_rfq.order_filled['LastPx']=self.price
        self.case_params_sell_rfq.order_filled['AvgPx']=self.price
        self.case_params_sell_rfq.order_filled['LastSpotRate']=self.price
        self.case_params_sell_rfq.order_filled['OrderID']=self.new_order.response_messages_list[0].fields['OrderID'].simple_value


        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled SPOT',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_filled_fwd(self,price='', qty='',fwd_point='',last_spot_rate=''):
        self.case_params_sell_rfq.prepape_order_filled_report()
        self.case_params_sell_rfq.order_filled['Price']=self.price
        self.case_params_sell_rfq.order_filled['LastPx']=self.price
        self.case_params_sell_rfq.order_filled['AvgPx']=self.price
        self.case_params_sell_rfq.order_filled['LastSpotRate']= '*'
        self.case_params_sell_rfq.order_filled['Price'] = self.price
        self.case_params_sell_rfq.order_filled['OrderID']=self.new_order.response_messages_list[0].fields['OrderID'].simple_value
        self.case_params_sell_rfq.order_filled['LastForwardPoints'] = '*'
        if price != '':
            self.case_params_sell_rfq.order_filled['Price'] = price
            self.case_params_sell_rfq.order_filled['LastPx'] = price
            self.case_params_sell_rfq.order_filled['AvgPx'] = price
            self.case_params_sell_rfq.order_filled['Price'] = price
        if fwd_point != '':
            self.case_params_sell_rfq.order_filled['LastSpotRate'] = last_spot_rate
            self.case_params_sell_rfq.order_filled['LastForwardPoints'] = fwd_point



        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled FORWARD',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_rejected(self,text='',price='', qty=''):
        self.case_params_sell_rfq.prepape_order_rejected_report()
        self.case_params_sell_rfq.order_rejected['OrderID']=self.new_order.response_messages_list[0].fields['OrderID'].simple_value
        self.case_params_sell_rfq.order_rejected['Price']=self.price
        self.case_params_sell_rfq.order_rejected['Text']=text
        if qty !='':
            self.case_params_sell_rfq.order_rejected['OrderQty']=qty
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Rejected',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_rejected, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_algo_rejected(self,text):
        self.case_params_sell_rfq.prepape_order_algo_rejected_report()
        self.case_params_sell_rfq.order_algo_rejected['Price']=self.price
        self.case_params_sell_rfq.order_algo_rejected['Text']=text

        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Rejected',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_algo_rejected, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self