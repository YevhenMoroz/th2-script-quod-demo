from custom.verifier import Verifier
from stubs import Stubs
from test_framework.win_gui_wrappers.base_window import BaseWindow
from test_framework.win_gui_wrappers.fe_trading_constant import PanicValues
from win_gui_modules.application_wrappers import ModifyPanicWindow, ExtractPanicValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call


class BasePanicWindow(BaseWindow):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.extraction_request = ExtractPanicValues()
        self.base_details = BaseTileDetails(base=self.base_request)
        self.modification_request = ModifyPanicWindow(details=self.base_details)
        self.common_act = Stubs.win_act
        self.extraction_call = self.common_act.extractPanicValues
        self.modification_call = self.common_act.modifyPanicWindow

    def set_default_params(self):
        self.modification_request = ModifyPanicWindow(details=self.base_details)
        self.extraction_request.set_details(self.base_details)
        self.extraction_request.set_extraction_id(self.extraction_id)
        self.verifier = Verifier(self.case_id)

    # region Extraction

    def extract_values_from_panic(self, *args: PanicValues):
        """
        Extract text of buttons in MM section in Panic window
        -----Example of usage-----
        response = self.panic_window.extract_values_from_panic(self.pricing)
        pricing_text = response[self.pricing.value]
        """
        self.set_default_params()
        if PanicValues.executable in args:
            self.extraction_request.extract_executable_button_text(PanicValues.executable.value)
        if PanicValues.pricing in args:
            self.extraction_request.extract_pricing_button_text(PanicValues.pricing.value)
        if PanicValues.hedge_orders in args:
            self.extraction_request.extract_hedge_orders_button_text(PanicValues.hedge_orders.value)
        response = call(self.extraction_call, self.extraction_request.build())
        self.clear_details([self.extraction_request])
        self.set_default_params()
        return response

    # endregion

    # region Modification
    def press_buttons(self, *args: PanicValues):
        """
        Press on buttons im MM section in Pricing window
        -----Example of usage-----
        pricing = PanicValues.pricing
        """
        if PanicValues.executable in args:
            self.modification_request.press_executable()
        if PanicValues.pricing in args:
            self.modification_request.press_pricing()
        if PanicValues.hedge_orders in args:
            self.modification_request.press_hedge_orders()
        call(self.modification_call, self.modification_request.build())
        self.clear_details([self.modification_request])
        self.set_default_params()

    def press_executable(self):
        self.set_default_params()
        self.modification_request.press_executable()
        call(self.modification_call, self.modification_request.build())
        self.clear_details([self.modification_request])

    def press_pricing(self):
        self.set_default_params()
        self.modification_request.press_pricing()
        call(self.modification_call, self.modification_request.build())
        self.clear_details([self.modification_request])

    def press_hedge_orders(self):
        self.set_default_params()
        self.modification_request.press_hedge_orders()
        call(self.modification_call, self.modification_request.build())
        self.clear_details([self.modification_request])
    # endregion
