from custom import basic_custom_actions as bca
from quod_qa.fx.fx_wrapper.common import check_order_status, prepeare_tif
from stubs import Stubs
import time


class FixClientSellRfq():
    fix_act = Stubs.fix_act
    verifier = Stubs.verifier
    quote = None
    case_params_sell_rfq = None
    new_order = None
    quote_response = None
    price =''
    quote_id=''

    def __init__(self, case_params_sell_rfq):
        self.case_params_sell_rfq = case_params_sell_rfq

    # ACTIONS

    # Send RFQ
    def send_request_for_quote(self):
        self.case_params_sell_rfq.prepare_rfq_params()
        print('RFQ' , self.case_params_sell_rfq.rfq_params)
        self.quote = self.fix_act.placeQuoteFIX(
            bca.convert_to_request(
                'Send Request For Quote',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteRequest', self.case_params_sell_rfq.rfq_params,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    # Send RFQ swap
    def send_request_for_quote_swap(self):
        self.quote = self.fix_act.placeQuoteFIX(
            bca.convert_to_request(
                'Send Request For Quote',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteRequest', self.case_params_sell_rfq.rfq_params_swap,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    def send_quote_cancel(self):
        self.case_params_sell_rfq.set_quote_cancel_params()
        self.case_params_sell_rfq.quote_cancel['QuoteID']=self.case_params_sell_rfq.quote_params['QuoteID']
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send QuoteCancel',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteCancel', self.case_params_sell_rfq.quote_cancel,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    # Send New Order Single
    def send_new_order_single(self, price, side=''):
        tif = prepeare_tif(self.case_params_sell_rfq.timeinforce)
        self.price = price
        self.case_params_sell_rfq.order_params['Price'] = self.price
        self.case_params_sell_rfq.order_params['QuoteID'] = self.quote_id
        if side!='':
            self.case_params_sell_rfq.order_params['Side'] = side
        print('Send an order', self.case_params_sell_rfq.order_params)
        self.new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new order ' + tif, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('NewOrderSingle', self.case_params_sell_rfq.order_params,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    def send_new_order_single_timeout(self, price):
        tif = prepeare_tif(self.case_params_sell_rfq.timeinforce)
        self.case_params_sell_rfq.order_params['Price'] = price
        self.new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new order ' + tif, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('NewOrderSingle', self.case_params_sell_rfq.order_params,
                                    self.case_params_sell_rfq.connectivityRFQ), 5
            ))
        return self

    # Extract filed by name
    def extruct_filed(self, field):
        extract_value = self.quote.response_messages_list[0].fields[field].simple_value
        return extract_value



    # VERIFICATION

    # Check Market Data respons was received
    def verify_quote_pending(self,offer_forward_points='',bid_forward_points='', bid_size='',offer_size='', offer_px='',bid_px='', bid_spot_rate=''):
        self.case_params_sell_rfq.prepare_quote_report()
        self.quote_id=self.extruct_filed('QuoteID')
        self.case_params_sell_rfq.quote_params['QuoteID'] = self.quote_id
        self.case_params_sell_rfq.quote_params['QuoteMsgID'] = self.quote_id
        self.case_params_sell_rfq.quote_params['Account'] = self.case_params_sell_rfq.rfq_params['NoRelatedSymbols'][0]['Account']
        self.case_params_sell_rfq.quote_params['SettlType'] = self.case_params_sell_rfq.rfq_params['NoRelatedSymbols'][0]['SettlType']
        self.case_params_sell_rfq.quote_params['SettlDate'] = self.case_params_sell_rfq.rfq_params['NoRelatedSymbols'][0]['SettlDate']
        if 'Side' in self.case_params_sell_rfq.quote_params.keys() == False:
            self.case_params_sell_rfq.quote_params['OfferPx'] = '*'
            self.case_params_sell_rfq.quote_params['OfferSize'] = '*'
            self.case_params_sell_rfq.quote_params['BidPx'] = '*'
            self.case_params_sell_rfq.quote_params['BidSize'] = '*'
        if offer_forward_points!='':
            self.case_params_sell_rfq.quote_params['OfferForwardPoints'] = offer_forward_points
        if bid_forward_points!='':
            self.case_params_sell_rfq.quote_params['BidForwardPoints'] = bid_forward_points
        if bid_size!='':
            self.case_params_sell_rfq.quote_params['BidSize'] = bid_size
        if offer_size!='':
            self.case_params_sell_rfq.quote_params['OfferSize'] = offer_size
        if offer_px!='':
            self.case_params_sell_rfq.quote_params['OfferPx'] = offer_px
        if bid_px!='':
            self.case_params_sell_rfq.quote_params['BidPx'] = bid_px
        if bid_spot_rate!='':
            self.case_params_sell_rfq.quote_params['BidSpotRate'] = bid_spot_rate

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive quote',
                bca.filter_to_grpc('Quote', self.case_params_sell_rfq.quote_params, ['QuoteReqID']),
                self.quote.checkpoint_id,
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id
                                  )
        )
        return self

    def verify_quote_cancel(self):
        self.case_params_sell_rfq.prepape_quote_cancel_report()
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                "Checking QuoteCancel",
                bca.filter_to_grpc("QuoteCancel", self.case_params_sell_rfq.quote_cancel_params),
                self.quote.checkpoint_id,
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id
            )
        )
        return self


    def verify_order_pending(self, price='', qty='',side=''):
        self.case_params_sell_rfq.prepare_order_pending_report()
        self.case_params_sell_rfq.order_pending['Price'] = self.price
        if price != '':
            self.case_params_sell_rfq.order_pending['Price'] = price
        if qty != '':
            self.case_params_sell_rfq.order_pending['OrderQty'] = qty
            self.case_params_sell_rfq.order_pending['LeavesQty'] = qty
            self.case_params_sell_rfq.order_pending['OrderID'] = self.new_order.response_messages_list[0].fields[
            'OrderID'].simple_value
        if side!='':
            self.case_params_sell_rfq.order_pending['Side'] = side
        self.checkpoint = self.new_order.checkpoint_id
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Pending',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_pending, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self


    def verify_order_new(self):
        self.case_params_sell_rfq.prepare_order_new_report()
        self.case_params_sell_rfq.order_new['Price'] = self.price
        self.case_params_sell_rfq.order_new['OrderID'] = self.new_order.response_messages_list[0].fields[
            'OrderID'].simple_value
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = New',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_new, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self


    def verify_order_filled(self, price='', qty='', side=''):
        self.case_params_sell_rfq.prepare_order_filled_report()
        self.case_params_sell_rfq.order_filled['Price'] = self.price
        self.case_params_sell_rfq.order_filled['LastPx'] = self.price
        self.case_params_sell_rfq.order_filled['AvgPx'] = self.price
        if side!='':
            self.case_params_sell_rfq.order_filled['Side'] = side
        self.case_params_sell_rfq.order_filled['LastSpotRate'] = self.price
        self.case_params_sell_rfq.order_filled['OrderID'] = self.new_order.response_messages_list[0].fields[
            'OrderID'].simple_value

        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled SPOT',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self


    def verify_order_filled_fwd(self, price='', qty='', fwd_point='', last_spot_rate='',side=''):
        self.case_params_sell_rfq.prepare_order_filled_report()
        self.case_params_sell_rfq.order_filled['Price'] = self.price
        self.case_params_sell_rfq.order_filled['LastPx'] = self.price
        self.case_params_sell_rfq.order_filled['AvgPx'] = self.price
        self.case_params_sell_rfq.order_filled['LastSpotRate'] = '*'
        self.case_params_sell_rfq.order_filled['Price'] = self.price
        self.case_params_sell_rfq.order_filled['OrderID'] = self.new_order.response_messages_list[0].fields['OrderID'].simple_value
        self.case_params_sell_rfq.order_filled['LastForwardPoints'] = '*'
        if price != '':
            self.case_params_sell_rfq.order_filled['Price'] = price
            self.case_params_sell_rfq.order_filled['LastPx'] = price
            self.case_params_sell_rfq.order_filled['AvgPx'] = price
            self.case_params_sell_rfq.order_filled['Price'] = price
        if fwd_point != '':
            self.case_params_sell_rfq.order_filled['LastSpotRate'] = last_spot_rate
            self.case_params_sell_rfq.order_filled['LastForwardPoints'] = fwd_point
        if side!='':
            self.case_params_sell_rfq.order_filled['Side'] = side

        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled FORWARD',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self


    def verify_order_rejected(self, text='', price='', qty=''):
        self.case_params_sell_rfq.prepare_order_rejected_report()
        self.case_params_sell_rfq.order_rejected['OrderID'] = self.new_order.response_messages_list[0].fields[
            'OrderID'].simple_value
        self.case_params_sell_rfq.order_rejected['Price'] = self.price
        self.case_params_sell_rfq.order_rejected['Text'] = text
        if qty != '':
            self.case_params_sell_rfq.order_rejected['OrderQty'] = qty
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Rejected',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_rejected, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self


    def verify_order_algo_rejected(self, text):
        self.case_params_sell_rfq.prepare_order_algo_rejected_report()
        self.case_params_sell_rfq.order_algo_rejected['Price'] = self.price
        self.case_params_sell_rfq.order_algo_rejected['Text'] = text

        self.verifier.submitCheckRule(
        request=bca.create_check_rule(
            'Execution Report with OrdStatus = Rejected',
            bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_algo_rejected,
                               ['ClOrdID', 'OrdStatus']),
            self.checkpoint, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id
        ),
            timeout=3000
        )
        return self
