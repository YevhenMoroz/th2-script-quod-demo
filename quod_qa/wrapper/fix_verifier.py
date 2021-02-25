from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_common.common_pb2 import Direction

class FixVerifier:

    def __init__(self, TraderConnectivity, case_id):
        self.verifier = Stubs.verifier
        self.TraderConnectivity = TraderConnectivity
        self.case_id = case_id

    def CheckExecutionReport(self, parameters, response, key_parameters = ['ClOrdID', 'OrdStatus'], message_name='Check ExecutionReport'):
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("ExecutionReport", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                self.case_id
            )
        )

    def CheckReject(self, parameters, response, key_parameters = ['ClOrdID', 'OrdStatus'], message_name='Check Reject'):
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("Reject", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                self.case_id
            )
        )

    def CheckNewOrderSingle(self, parameters, response, key_parameters = ['ClOrdID', 'OrdStatus'], message_name='Check NewOrderSingle to buy-side'):
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("NewOrderSingle", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                self.case_id
            )
        )

    def CheckOrderCancelReplaceRequest(self, parameters, response, key_parameters = ['OrigClOrdID'], message_name='Check OrderCancelReplaceRequest to buy-side'):
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("OrderCancelReplaceRequest", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                self.case_id
            )
        )