import logging

from th2_grpc_act_gui_quod import cp_operations_pb2

from custom.verifier import Verifier, VerificationMethod
from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca

from win_gui_modules.utils import (set_session_id, get_base_request, call , get_opened_fe)
from win_gui_modules.wrappers import set_base
from win_gui_modules.client_pricing_wrappers import BaseTileDetails


class TestCase:
    def __init__(self, report_id):
        # Logger setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Services setup
        self.common_act = Stubs.win_act

        self.ar_service = Stubs.win_act_aggregated_rates_service
        self.cp_service = Stubs.win_act_cp_service
        self.ob_act = Stubs.win_act_order_book

        # Case parameters setup
        self.case_id = bca.create_event('QAP-1557', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        self.base_details = BaseTileDetails(base=self.base_request)

        self.venue = 'HSB'
        self.user = 'QA4'   #Stubs.custom_config['qf_trading_fe_user_303']
        self.quote_id = None

        # Case rules
        self.rule_manager = RuleManager()
        self.RFQ = None
        self.TRFQ = None

    # FE open method
    def prepare_frontend(self):
        work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
        password = Stubs.custom_config['qf_trading_fe_password_303']
        # get_opened_fe_303(self.case_id, self.session_id)
        get_opened_fe(self.case_id, self.session_id )


    def colour(self):
        det = cp_operations_pb2.ClientPriceGridDetails(base=self.base_request,
                                                       clientTier='Bronze',
                                                       instrSymbol='EUR/USD',
                                                       clientPriceColumns=[],
                                                       extractBands=True,
                                                       bandsColumns=['Key', 'Spot'])

        string = call(Stubs.win_act_cp_service.processClientPriceGrid, det)

        res = ''
        for x in range(len(string['bandsTable'])):
            if string['bandsTable'][x] == '#':
                for y in range(0, 7):
                    res += string['bandsTable'][x + y]
                res += ','
        list = res.split(',')
        print(list)

        verifier = Verifier(self.case_id)
        verifier.set_event_name("Check colors")
        for x in range(0,len(list)-1,2):
            name = 'color Id: ' + str(x/2)
            verifier.compare_values(name, list[x], list[x+1], VerificationMethod.NOT_EQUALS)
        verifier.verify()

    # def client_grid(self):
    #     client_grid_params = ExtractClientGridValues(self.base_request)
    #     client_grid_params.set_client_tier('Generic')
    #     client_grid_params.set_instr_symbol('EUR/USD')
    #     client_grid_params.set_extract_bands()
    #     client_grid_params.set_bands_columns('key')
    #
    #     res = call(Stubs.win_act_cp_service.processClientPriceGrid, client_grid_params.build())
    #
    #     for x in res:
    #         print(x, ' - - - ', res[x])

    def execute(self):
        try:
            self.prepare_frontend()
            self.colour()
            # self.client_grid()
        except Exception as e:
            logging.error('Error execution', exc_info=True)
        # close_fe(self.case_id, self.session_id)
