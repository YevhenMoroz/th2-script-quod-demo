import time
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.forex.fx_positions import FXPositions


class CreatePositions(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = SessionAliasFX().ss_rfq_connectivity
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.gateway_side_sell = DataSet.GatewaySide.Sell
        self.status = DataSet.Status.Fill
        self.positions = FXPositions(self.test_id, self.session_id)
        self.quote_request = FixMessageQuoteRequestFX()
        self.expected_position = int(expected_pos)

        self.clients = clients
        self.symbols = symbols
        self.currency = currency

        self.security_type = None
        self.settle_date = None
        self.settle_type = None

    @try_except(test_id=Path(__file__).name[:-3])
    def create_pos(self, account, base_currency, instrument):
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=account,
                                                           Currency=base_currency, Instrument=instrument,
                                                           OrderQty=100000)

        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        new_order_single = FixMessageNewOrderSinglePrevQuotedFX().set_default_prev_quoted(self.quote_request,
                                                                                          response[0])
        self.fix_manager_gtw.send_message_and_receive_response(new_order_single)
        execution_report = FixMessageExecutionReportPrevQuotedFX().set_params_from_new_order_single(new_order_single,
                                                                                                    self.gateway_side_sell,
                                                                                                    self.status)
        self.fix_verifier.check_fix_message(execution_report, direction=DirectionEnum.FromQuod)

        time.sleep(5)
        self.quote_request.change_parameter("QuoteReqID", bca.client_orderid(9))
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Side='2')
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        new_order_single = FixMessageNewOrderSinglePrevQuotedFX().set_default_prev_quoted(self.quote_request,
                                                                                          response[0])
        self.fix_manager_gtw.send_message_and_receive_response(new_order_single)
        execution_report = FixMessageExecutionReportPrevQuotedFX().set_params_from_new_order_single(new_order_single,
                                                                                                    self.gateway_side_sell,
                                                                                                    self.status)
        self.fix_verifier.check_fix_message(execution_report, direction=DirectionEnum.FromQuod)

    @try_except(test_id=Path(__file__).name[:-3])
    def equal_pos(self, account, base_currency, instrument, side, qty):
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=account,
                                                           Currency=base_currency, Instrument=instrument, Side=side,
                                                           OrderQty=qty)

        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        new_order_single = FixMessageNewOrderSinglePrevQuotedFX().set_default_prev_quoted(self.quote_request,
                                                                                          response[0])
        self.fix_manager_gtw.send_message_and_receive_response(new_order_single)
        execution_report = FixMessageExecutionReportPrevQuotedFX().set_params_from_new_order_single(new_order_single,
                                                                                                    self.gateway_side_sell,
                                                                                                    self.status)
        self.fix_verifier.check_fix_message(execution_report, direction=DirectionEnum.FromQuod)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # Region Precondition
        for client in self.clients:
            for symbol in self.symbols:
                base_currency = ''
                if self.currency == 1:
                    base_currency = symbol.split('/')[0]
                else:
                    base_currency = symbol.split('/')[1]
                instrument = {
                    "Symbol": symbol,
                    "SecurityType": self.security_type
                }
                self.create_pos(client, base_currency, instrument)
                position = self.positions.set_filter(['Account', client, 'Symbol', symbol]).extract_field(
                    'Position').replace(',', '')
                # print(position)
                position = int(position)
                if position != self.expected_position:
                    if position < self.expected_position:
                        side = '1'
                        difference = self.expected_position - position
                        difference = str(difference)
                        self.equal_pos(client, base_currency, instrument, side, difference)
                    elif position > self.expected_position:
                        side = '2'
                        difference = position - self.expected_position
                        self.equal_pos(client, base_currency, instrument, side, difference)
                print(
                    f'Position on account {client}_1 with symbol {symbol} now equals to {self.expected_position}, finished')


class CreatePositionsSpot(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_spot')
        self.settle_date = self.data_set.get_settle_date_by_name('spot')
        self.settle_type = self.data_set.get_settle_type_by_name('spot')


class CreatePositionsWK1(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_date = self.data_set.get_settle_date_by_name('wk1')
        self.settle_type = self.data_set.get_settle_type_by_name('wk1')


class CreatePositionsWK2(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_date = self.data_set.get_settle_date_by_name('wk2')
        self.settle_type = self.data_set.get_settle_type_by_name('wk2')


class CreatePositionsWK3(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_date = self.data_set.get_settle_date_by_name('wk3')
        self.settle_type = self.data_set.get_settle_type_by_name('wk3')


class CreatePositionsTOM(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_date = self.data_set.get_settle_date_by_name('tomorrow')
        self.settle_type = self.data_set.get_settle_type_by_name('tomorrow')


class CreatePositionsTOD(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_date = self.data_set.get_settle_date_by_name('today')
        self.settle_type = self.data_set.get_settle_type_by_name('today')


class CreatePositionsWK1NDF(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_ndf')
        self.settle_date = self.data_set.get_settle_date_by_name('wk1')
        self.settle_type = self.data_set.get_settle_type_by_name('wk1')


class CreatePositionsWK2NDF(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_ndf')
        self.settle_date = self.data_set.get_settle_date_by_name('wk2')
        self.settle_type = self.data_set.get_settle_type_by_name('wk2')


class CreatePositionsWK3NDF(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_ndf')
        self.settle_date = self.data_set.get_settle_date_by_name('wk3')
        self.settle_type = self.data_set.get_settle_type_by_name('wk3')


class CreatePositionsTOMNDF(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_ndf')
        self.settle_date = self.data_set.get_settle_date_by_name('tomorrow')
        self.settle_type = self.data_set.get_settle_type_by_name('tomorrow')


class CreatePositionsTODNDF(CreatePositions):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, clients: list = None,
                 symbols: list = None, currency: int = 1, expected_pos: int = 0):
        super().__init__(report_id, session_id, data_set, clients, symbols, currency, expected_pos)
        self.security_type = self.data_set.get_security_type_by_name('fx_ndf')
        self.settle_date = self.data_set.get_settle_date_by_name('today')
        self.settle_type = self.data_set.get_settle_type_by_name('today')
