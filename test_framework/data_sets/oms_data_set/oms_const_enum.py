from enum import Enum


class OmsFixInstruments(Enum):
    instrument_1 = dict(  # without commission/fee
        Symbol='FR0010436584',  # assigned counterpart_reb_1
        SecurityID='FR0010436584',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS',
        SecurityDesc='DREAMNEX'
    )
    instrument_2 = dict(  # with commission/fee
        Symbol='ISI1',  # assigned counterpart_mma_2
        SecurityID='ISI1',
        SecurityIDSource='4',
        SecurityExchange='XEUR',
        SecurityType='CS'
    )
    instrument_3 = dict(
        Symbol='ISI3',  # with commission/fee
        SecurityID='ISI3',  # assigned counterpart_mma_2
        SecurityIDSource='4',
        SecurityExchange='XEUR',
        SecurityType='CS'
    )
    instrument_dummy = dict(
        Symbol='DUMMY',
        SecurityID='DUMMY',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )
    instrument_tag_5120 = dict(
        Symbol='test123',
        SecurityID='FR0010436584',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS',
    )


class OmsInstrumentId(Enum):
    instrument_1 = "5XRAA7DXZg14IOkuNrAfsg"


class OmsListingId(Enum):
    listing_1 = "1200"


class OmsVenues(Enum):
    venue_1 = "PARIS"
    venue_2 = "EUREX"
    venue_3 = "JSE"


class OmsLookupForVenues(Enum):
    """USED FOR CREATING ORDER VIA FE"""
    lookup_1 = 'VETO'


class OmsClients(Enum):
    """Base"""
    client_1 = "CLIENT1"
    client_2 = "CLIENT2"
    client_3 = "CLIENT3"
    client_4 = "CLIENT4"
    """PositionMgt"""
    client_pos_1 = "36ONE"  # Institutional
    client_pos_2 = "ABAXX"  # Institutional
    client_pos_3 = "SBK"  # Firm
    client_pos_4 = "TEST"  # BDA test
    """Dummy"""
    client_dummy = "DUMMY"
    """PostTrade"""
    client_pt_1 = "MOClient"  # Fully Manual
    client_pt_2 = "MOClient2"  # CS = Manual, Fully auto
    client_pt_3 = "MOClient3"  # CS = Manual, BI = Auto, Other Manual
    client_pt_4 = "MOClient4"  # CS = Manual, AP = Auto, Other Manual
    client_pt_5 = "MOClient5"  # CS = Manual, BA = Auto, Other Manual
    client_pt_6 = "MOClient6"  # CS = CTM, Other Manual
    client_pt_7 = "CLIENT_FIX_POSTTRADE"  # To automatically accept care orders sent via FIX
    client_pt_8 = "MOClient7"
    """Care"""
    client_co_1 = "CLIENT_FIX_CARE"  # also used for Basket
    client_co_2 = "CLIENT_FIX_CARE_WB"
    """Commissions"""
    client_com_1 = "CLIENT_COMM_1"
    client_com_2 = "CLIENT_COMM_2"


class OmsVenueClientNames(Enum):
    """Base"""
    client_1_venue_1 = "XPAR_CLIENT1"
    client_1_venue_2 = "XEUR_CLIENT1"
    """PostTrade"""
    client_pt_1_venue_1 = "MOClient_PARIS"
    client_pt_1_venue_2 = "MOClient_EUREX"
    client_pt_2_venue_1 = "MOClient2_PARIS"
    client_pt_3_venue_1 = "MOClient3_PARIS"
    client_pt_4_venue_1 = "MOClient4_PARIS"
    client_pt_5_venue_1 = "MOClient5_PARIS"
    client_pt_6_venue_1 = "MOClient6_PARIS"
    client_pt_7_venue_1 = "MOClient7_PARIS"
    client_pos_3_venue_1 = "SBK_PARIS"
    """Care"""
    client_co_1_venue_1 = "CLIENT_FIX_CARE_PARIS"
    client_co_2_venue_1 = "CLIENT_FIX_CARE_WB_PARIS"
    """Commissions"""
    client_com_1_venue_2 = "CLIENT_COMM_1_EUREX"


class OmsAccounts(Enum):
    """PositionMgt"""
    client_pos_3_acc_1 = "Facilitation"
    client_pos_3_acc_2 = "Prime_Optimise"
    client_pos_3_acc_3 = "PROP"
    """PostTrade"""
    client_pt_1_acc_1 = "MOClient_SA1"
    client_pt_1_acc_2 = "MOClient_SA2"
    client_pt_1_acc_3 = "MOClient_SA3"
    client_pt_1_acc_4 = "MOClient_SA4"
    client_pt_2_acc_1 = "MOClient2_SA1"
    client_pt_2_acc_2 = "MOClient2_SA2"
    client_pt_3_acc_1 = "MOClient3_SA1"
    client_pt_3_acc_2 = "MOClient3_SA2"
    client_pt_4_acc_1 = "MOClient4_SA1"
    client_pt_4_acc_2 = "MOClient4_SA2"
    client_pt_5_acc_1 = "MOClient5_SA1"
    client_pt_5_acc_2 = "MOClient5_SA2"
    client_pt_6_acc_1 = "MOClient6_SA1"
    client_pt_6_acc_2 = "MOClient6_SA2"
    client_pt_7_acc_1 = "MOClient7_SA1"
    """Care"""
    client_co_1_acc_1 = "CLIENT_FIX_CARE_SA1"
    """Commissions"""
    client_com_1_acc_1 = "CLIENT_COMM_1_SA1"
    client_com_1_acc_2 = "CLIENT_COMM_1_SA2"
    client_com_1_acc_3 = "CLIENT_COMM_1_SA3"
    client_com_1_acc_4 = "CLIENT_COMM_1_EXEMPTED"  # This acc is exempted from client commissions
    client_com_2_acc_1 = "CLIENT_COMM_2_SA1"
    client_com_2_acc_2 = "CLIENT_COMM_2_SA2"
    client_com_2_acc_3 = "CLIENT_COMM_2_SA3"


class OmsWashbookAccounts(Enum):
    washbook_account_1 = "DMA Washbook"
    washbook_account_2 = "CareWB"
    washbook_account_3 = "DefaultWashBook"


class OmsRecipients(Enum):
    recipient_desk_1 = ""
    recipient_desk_2 = ""
    recipient_desk_3 = ""

    recipient_user_1 = ""
    recipient_user_2 = ""
    recipient_user_3 = ""


class OmsCounterparts(Enum):
    counterpart_cus_1 = "Custodian - User"
    counterpart_cus_2 = "Custodian - User2"
    counterpart_mma_1 = "MarketMaker - TH2Route"
    counterpart_mma_2 = "MarketMaker - Venue(EUREX)"
    counterpart_reb_1 = "RegulatoryBody - Venue(Paris)"
    counterpart_exf_1 = "ExecutingFirm"
    counterpart_cnf_1 = "ContraFirm"
    counterpart_inf_1 = "InvestmentFirm - ClCounterpart"
    counterpart_inf_2 = "InvestmentFirm - ClCounterpart_SA1"
    counterpart_exc_1 = "Exchange - ClCountepart2"
    counterpart_inv_1 = "InvestorID - ClCounterpart2_SA1"
    counterpart_pos_1 = "PositionAccount - DMA Washbook"


class OmsMic(Enum):  # Market Identifier Code
    mic_1 = "XPAR"  # EURONEXT PARIS
    mic_2 = "XEUR"  # EUREX


class OmsCurrency(Enum):
    currency_1 = "EUR"
    currency_2 = "GBP"
    currency_3 = "GBp"
    currency_4 = "USD"
    currency_5 = "UAH"


class OmsRoutes(Enum):
    route_1 = "Route via FIXBUYTH2 - component"
    route_2 = "Chix direct access"


class OmsRouteID(Enum):
    route_1 = 24


class OmsVenueClientAccounts(Enum):
    client_pt_1_acc_1_venue_client_account = 'MOCLIENT_SA1'
    client_pt_1_acc_2_venue_client_account = 'MOCLIENT_SA2'
    client_pt_1_acc_3_venue_client_account = "11223344"


class OMSCommissionProfiles(Enum):
    abs_amt = 1
    per_u_qty = 2
    perc_qty = 3
    perc_amt = 4
    bas_amt = 5
    bas_qty = 6
    abs_amt_usd = 7
    abs_amt_2 = 8


class OMSFeeType(Enum):
    agent = "AGE"
    exch_fees = "EXC"
    levy = "LEV"
    consumption_tax = "CTX"
    conversion = "CON"
    extra = "EXT"
    local_comm = "LOC"
    markup = "MAR"
    other = "OTH"
    per_transac = "TRA"
    regulatory = "REG"
    route = "ROU"
    stamp = "STA"
    tax = "TAX"
    value_added_tax = "VAT"


class OMSExecScope(Enum):
    all_exec = "ALL"
    day_first_exec = "DAF"
    first_exec = "FST"


class OMSFeeOrderScope(Enum):
    done_for_day = "DFD"
    order_acknowledgement = "ACK"


class OMSFee(Enum):
    fee1 = 1
    fee2 = 2
    fee3 = 3


class OMSCommission(Enum):
    commission1 = 1
    commission2 = 2
    commission3 = 3


class OmsQtyTypes(Enum):
    qty_type_1 = "UnmatchedQty"
    qty_type_2 = "OrderQty"


class OMSPset(Enum):
    pset_1 = ('CREST', "CRSTGB22")
    pset_2 = ('EURO_CLEAR', "MGTCBEBE")


class OMSCommissionAndFeeBasis(Enum):
    comm_basis_1 = 'Absolute'
    comm_basis_2 = 'Percentage'


class OMSBasketTemplates(Enum):
    template1 = "Default Template"
    template2 = "Test Template"  # This is a test template with header and default value
    template3 = "Test Template 2"  # This is a test template without header and default value
    template4 = "TemplateWithCurrencyAndVenue"  # Template for testing set upped currency and venue
    template5 = "Test Template csv"  # This is a test template without header and custom delimiter
