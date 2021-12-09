import logging

from th2_grpc_act_gui_quod.ar_operations_pb2 import ExtractOrderTicketValuesRequest, ExtractDirectVenueExecutionRequest
from th2_grpc_common.common_pb2 import Direction

from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca

from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, ContextActionType
from win_gui_modules.application_wrappers import CloseApplicationRequest
from win_gui_modules.wrappers import set_base
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ExtractRatesTileTableValuesRequest
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import get_base_request, call, close_fe, prepare_fe


class TestCase:
    def __init__(self, report_id, session_id):
        # Logger setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Services setup
        self.common_act = Stubs.win_act
        self.ar_service = Stubs.win_act_aggregated_rates_service
        self.cp_service = Stubs.win_act_cp_service
        self.ob_act = Stubs.win_act_order_book

        # Case parameters setup
        self.case_id = bca.create_event('QAP-2715', report_id)
        self.session_id = session_id
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        self.base_details = BaseTileDetails(base=self.base_request)

        self.tile_1 = BaseTileDetails(base=self.base_request, window_index=0)
        self.tile_2 = BaseTileDetails(base=self.base_request, window_index=1)

        self.venue = "Multi Commodity Exchange"
        self.user = Stubs.custom_config['qf_trading_fe_user']
        self.quote_id = None
        self.api = Stubs.api_service

    def test_get(self):
        connectivity = 'rest_wa315luna'
        params = {}
        checkpoint1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(self.case_id))
        checkpoint_id1 = checkpoint1.checkpoint
        Stubs.api_service.sendMessage(request=SubmitMessageRequest(message=bca.wrap_message(content=params,
                                                                                            message_type='FindAllLocation',
                                                                                            session_alias='rest_wa315luna'),
                                                                   parent_event_id=self.case_id))

        content = [
            {
                "locationName": "INDIA",
                "zoneID": 1,
                "locationID": 1,
                "alive": "true"
            },
            {
                "locationName": "EAST-LOCATION-B",
                "zoneID": 1,
                "locationID": 3,
                "alive": "true"
            },
            {
                "locationName": "EAST-LOCATION-A",
                "zoneID": 1,
                "locationID": 2,
                "alive": "true"
            },
            {
                "locationName": "WEST-LOCATION-A",
                "zoneID": 2,
                "locationID": 4,
                "alive": "true"
            },
            {
                "locationName": "WEST-LOCATION-B",
                "zoneID": 2,
                "locationID": 5,
                "alive": "true"
            }
        ]
        #print(content[0])
        Stubs.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'FindAllLocation',
                bca.wrap_filter(content[0], 'FindAllLocation', None),
                checkpoint_id1, connectivity, self.case_id, direction=Direction.Value("FIRST")
            ),

        )

    # Main method
    def execute(self):
        try:
            self.test_get()

        except Exception as e:
            logging.error('Error execution', exc_info=True)
        # close_fe(self.case_id, self.session_id)
