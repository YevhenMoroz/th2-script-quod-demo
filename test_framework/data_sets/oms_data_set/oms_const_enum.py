from enum import Enum


class OmsFixInstruments(Enum):
    instrument_1 = dict(  # without commission/fee
        Symbol='FR0010436584',  # assigned counterpart_reb_1
        SecurityID='FR0010436584',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS',
        SecurityDesc='VETOQUINOL'
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


class OmsJavaApiInstruments(Enum):
    instrument_1 = dict(
        InstrSymbol="FR0010436584_EUR",
        SecurityID="FR0010436584",
        SecurityIDSource="ISI",
        InstrType="Equity",
        SecurityExchange="XPAR"
    )
    instrument_3 = dict(
        InstrSymbol='ISI3',
        SecurityID='ISI3',
        SecurityIDSource='ISI',
        InstrType='Equity',
        SecurityExchange='XEUR'
    )

    instrument_2 = dict(
        InstrSymbol='ISI3',
        SecurityID='ISI3',
        SecurityIDSource='ISI',
        InstrType="Equity",
        SecurityExchange="XEUR"
    )


class OmsInstrumentId(Enum):
    instrument_1 = "5XRAA7DXZg14IOkuNrAfsg"
    instrument_2 = "EuUVvUnWPiYSvXGV6IBedQ"
    instrument_3 = "JAFGYQq-9qTrmmY9kyM2TQ"


class OmsListingId(Enum):
    listing_1 = "1200"
    listing_2 = '9500000049'
    listing_3 = "704"


class OmsVenues(Enum):
    venue_1 = "PARIS"
    venue_2 = "EUREX"
    venue_3 = "JSE"


class OmsLookupForVenues(Enum):
    """USED FOR CREATING ORDER VIA FE"""
    lookup_1 = 'VETO'
    lookup_2 = 'DNX'
    lookup_for_listing_eurex_web_admin = 'EUR[EUREX]'


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
    client_pt_9 = "MOClient_9"
    client_pt_10 = "MOClient10"  # CS Manual Fully auto
    """Care"""
    client_co_1 = "CLIENT_FIX_CARE"  # also used for Basket
    client_co_2 = "CLIENT_FIX_CARE_WB"
    """Commissions"""
    client_com_1 = "CLIENT_COMM_1"
    client_com_2 = "CLIENT_COMM_2"
    client_fees_1 = "CLIENT_FEES_1"
    """Counterparts"""
    client_counterpart_1 = "CLIENT_COUNTERPART"
    client_counterpart_2 = "CLIENT_COUNTERPART2"
    client_counterpart_3 = "CLIENT_COUNTERPART_3"


class OmsVenueClientNames(Enum):
    """Base"""
    client_1_venue_1 = "XPAR_CLIENT1"
    client_2_venue_1 = "XPAR_CLIENT2"
    client_1_venue_2 = "XEUR_CLIENT1"
    """PostTrade"""
    client_pt_1_venue_1 = "MOClient_PARIS"
    client_pt_1_venue_2 = "MOClient_EUREX"
    client_pt_2_venue_1 = "MOClient2_PARIS"
    client_pt_2_venue_2 = "MOClient2_EUREX"
    client_pt_3_venue_1 = "MOClient3_PARIS"
    client_pt_3_venue_2 = "MOClient3_EUREX"
    client_pt_4_venue_1 = "MOClient4_PARIS"
    client_pt_4_venue_2 = "MOClient4_EUREX"
    client_pt_5_venue_1 = "MOClient5_PARIS"
    client_pt_6_venue_1 = "MOClient6_PARIS"
    client_pt_7_venue_1 = "MOClient7_PARIS"
    client_pt_9_venue_1 = "MOClient9_PARIS"
    client_pt_10_venue_1 = "MOClient10_PARIS"
    client_pos_3_venue_1 = "SBK_PARIS"
    client_pos_1_venue_1 = "36ONE_PARIS"
    """Care"""
    client_co_1_venue_1 = "CLIENT_FIX_CARE_PARIS"
    client_co_2_venue_1 = "CLIENT_FIX_CARE_WB_PARIS"
    """Commissions"""
    client_com_1_venue_1 = "CLIENT_COMM_1_PARIS"
    client_com_1_venue_2 = "CLIENT_COMM_1_EUREX"
    """Counterparts"""
    client_counterpart_1_venue_1 = "CLIENT_COUNTERPART_PARIS"
    client_counterpart_1_venue_2 = "CLIENT_COUNTERPART_EUREX"
    client_counterpart_2_venue_1 = "CLIENT_COUNTERPART2_PARIS"
    client_counterpart_3_venue_1 = "CLIENT_COUNTERPART_3_PARIS"


class OmsAccounts(Enum):
    """Base"""
    client_1_acc_1 = "NEWACCOUNT"
    """PositionMgt"""
    client_pos_3_acc_1 = "Facilitation"
    client_pos_3_acc_2 = "Prime_Optimise"
    client_pos_3_acc_3 = "PROP"
    client_pos_3_acc_4 = "PROP_TEST"
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
    client_pt_9_acc_1 = "MOClient9_SA1"
    client_pt_10_acc_1 = "MOClient10_SA1"
    """Care"""
    client_co_1_acc_1 = "CLIENT_FIX_CARE_SA1"
    """Dummy"""
    client_co_1_dummy_acc = "CLIENT_FIX_CARE_DUMMY_SA1"
    """Commissions"""
    client_com_1_acc_1 = "CLIENT_COMM_1_SA1"
    client_com_1_acc_2 = "CLIENT_COMM_1_SA2"
    client_com_1_acc_3 = "CLIENT_COMM_1_SA3"
    client_com_1_acc_4 = "CLIENT_COMM_1_EXEMPTED"  # This acc is exempted from client commissions
    client_com_2_acc_1 = "CLIENT_COMM_2_SA1"
    client_com_2_acc_2 = "CLIENT_COMM_2_SA2"
    client_com_2_acc_3 = "CLIENT_COMM_2_SA3"
    client_fees_1_acc_1 = "CLIENT_FEES_1_SA_1"
    """Counterparts"""
    client_counterpart_1_acc_1 = "CLIENT_COUNTERPART_SA1"
    client_counterpart_1_acc_2 = "CLIENT_COUNTERPART_SA2"
    client_counterpart_1_acc_3 = "CLIENT_COUNTERPART_SA3"
    client_counterpart_2_acc_1 = "CLIENT_COUNTERPART2_SA1"
    client_counterpart_3_acc_1 = "CLIENT_COUNTERPART_3_SA1"


class AlgoParametersExternal(Enum):
    parameter_name = "ParameterName"
    parameter_value = "ParameterValue"


class OmsWashbookAccounts(Enum):
    washbook_account_1 = "DMA Washbook"
    washbook_account_2 = "CareWB"
    washbook_account_3 = "DefaultWashBook"
    washbook_account_4 = "AlgoWashBook"


class OmsRecipients(Enum):
    recipient_desk_1 = ""
    recipient_desk_2 = ""
    recipient_desk_3 = ""

    recipient_user_1 = "JavaApiUser"
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
    abs_amt_3 = 9
    commission_with_minimal_value = 600018
    client_commission_percentage = 15
    abs_amt_gbp = 12
    perc_rounding_to_whole_number = 800020
    abs_amt_gbp_small = 800021

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
    on_calculated = "CAL"


class OMSFeeOrderScope(Enum):
    done_for_day = "DFD"
    order_acknowledgement = "ACK"


class OMSFee(Enum):
    fee1 = 1
    fee2 = 2
    fee3 = 3
    fee_vat = 11


class OMSCommission(Enum):
    commission1 = 1
    commission2 = 2
    commission3 = 3


class OMSClientListID(Enum):
    cl_list_comm_1 = 400006
    cl_list_peq_4925 = 400010


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


class OMSGiveUpBrokers(Enum):
    give_up_broker_1 = 'GiveUpBrokerForVS'


class OMSClientDesks(Enum):
    client_desk_1 = 'Fully Manual'


class OMSBookingTicketFeeType(Enum):
    fee_type_in_booking_ticket_1 = "Regulatory"


class OMSNetGrossInd(Enum):
    net_ind = 'Net'
    gross_ind = 'Gross'


class OMSStatus(Enum):
    status_1 = 'Accepted'


class OMSMatchStatus(Enum):
    match_status_1 = 'Unmatched'


class OMSExecutionPolicy(Enum):
    dma = 'DMA'
    care = 'Care'
    synthetic = 'Synth'


class OMSTimeInForce(Enum):
    time_in_force_1 = "Day"
    time_in_force_2 = "GoodTillDate"


class OMSOrdType(Enum):
    limit = 'Limit'


class OMSCapacity(Enum):
    agency = 'Agency'


class OMSBagStrategy(Enum):
    internal_twap = "Quod Financial Internal TWAP"


class OMSBagScenario(Enum):
    twap_strategy = "TWAP strategy"


class OMSVenueID(Enum):
    paris = "PARIS"
    eurex = "EUREX"
    chix = "CHIX"
    jse = "JSE"


class OMSCounterpartID(Enum):
    contra_firm = "200003"
    contra_firm2 = "1000009"


class OMSInstrType(Enum):
    equity = "EQU"


class OMSContraFirm(Enum):
    contra_firm_1 = "ContraFirm"
    contra_firm_2 = "ContraFirm2"


class OMSReferencePrice(Enum):
    ref_pr_1 = 'DayLow'
    ref_pr_2 = 'DayHigh'
    ref_pr_3 = 'LastTradedPrice'
    ref_pr_4 = 'Open'
    ref_pr_5 = 'Close'
    ref_pr_6 = 'LTP'
    ref_pr_7 = 'CLO'
    ref_pr_8 = 'OPN'
    ref_pr_9 = 'DHI'
    ref_pr_10 = 'DLO'


class OMSWashBookRule(Enum):
    RuleForTest = 200004
    name_washbook_rule = 'washbook1'


class VenueAccountIDSource(Enum):
    oth = 'OTH'


class OMSVenueAccountNamesOfSecurityAccounts(Enum):
    venue_account_name_of_security_acc_1_chix = "MOClient_SA1_CHIX"
    venue_account_name_of_security_acc_1_eurex = "MOClient_SA1_EUREX"
    venue_account_name_of_security_acc_1_jse = "MOClient_SA1_JSE"
    venue_account_name_of_security_acc_1_paris = "MOClient_SA1_PARIS"


class OMSVenueSecAccountNames(Enum):
    venue_sec_act_name_pt_1_acc_1_rec_1 = [False, False, False, VenueAccountIDSource.oth.value,
                                           OMSVenueAccountNamesOfSecurityAccounts.venue_account_name_of_security_acc_1_chix.value,
                                           OmsVenueClientAccounts.client_pt_1_acc_1_venue_client_account.value,
                                           OMSVenueID.chix.value
                                           ]
    venue_sec_act_name_pt_1_acc_1_rec_2 = [False, False, False, VenueAccountIDSource.oth.value,
                                           OMSVenueAccountNamesOfSecurityAccounts.venue_account_name_of_security_acc_1_eurex.value,
                                           OmsVenueClientAccounts.client_pt_1_acc_1_venue_client_account.value,
                                           OMSVenueID.eurex.value
                                           ]
    venue_sec_act_name_pt_1_acc_1_rec_3 = [False, False, False, VenueAccountIDSource.oth.value,
                                           OMSVenueAccountNamesOfSecurityAccounts.venue_account_name_of_security_acc_1_jse.value,
                                           OmsVenueClientAccounts.client_pt_1_acc_1_venue_client_account.value,
                                           OMSVenueID.jse.value
                                           ]
    venue_sec_act_name_pt_1_acc_1_rec_4 = [False, False, False, VenueAccountIDSource.oth.value,
                                           OMSVenueAccountNamesOfSecurityAccounts.venue_account_name_of_security_acc_1_paris.value,
                                           OmsVenueClientAccounts.client_pt_1_acc_1_venue_client_account.value,
                                           OMSVenueID.paris.value
                                           ]


class OMSCommonVenueSecAccountNamesOfAcc(Enum):
    client_pt_1_acc_1 = (OMSVenueSecAccountNames.venue_sec_act_name_pt_1_acc_1_rec_1.value,
                         OMSVenueSecAccountNames.venue_sec_act_name_pt_1_acc_1_rec_2.value,
                         OMSVenueSecAccountNames.venue_sec_act_name_pt_1_acc_1_rec_3.value,
                         OMSVenueSecAccountNames.venue_sec_act_name_pt_1_acc_1_rec_4.value
                         )


class OMSClearingAccountTypes(Enum):
    institutional = 'INS'


class OMSVenueListForCommissionAndFees(Enum):
    venue_list_1 = 1


class OMSISINSecurityAltIDs(Enum):
    isin_security_alt_id_isi_3 = 'IS0000000001'


class OMSSecurityIDSourceForListings(Enum):
    security_id_source = "ISI"


class OMS_SymbolForListingsFromWebAdmin(Enum):
    symbol_1 = "EUR"


class OMSTickSizeProfile(Enum):
    tick_size_profile_1 = 3


class OMSCounterPartyIDs_FIX(Enum):
    counterpart_id_gtwquod4 = {'PartyRole': "36", 'PartyRoleQualifier': '1011', 'PartyID': "gtwquod4",
                               'PartyIDSource': "D"}
    counterpart_id_market_maker_th2_route = {'PartyRole': "66", 'PartyID': "MarketMaker - TH2Route",
                                             'PartyIDSource': "C"}
    counterpart_id_investment_firm_cl_counterpart_sa1 = {'PartyRole': "5",
                                                         'PartyID': 'InvestorID - ClCounterpart_SA1',
                                                         'PartyIDSource': "C"}
    counterpart_id_custodian_user_2 = {'PartyRole': '28', 'PartyID': 'CustodianUser2', 'PartyRoleQualifier': '24',
                                       'PartyIDSource': 'C'}
    counterpart_id_custodian_user = {'PartyRole': '28', 'PartyID': 'CustodianUser', 'PartyRoleQualifier': '24',
                                     'PartyIDSource': 'C'}
    counter_part_id_contra_firm = {'PartyRole': "17", 'PartyID': 'ContraFirm', 'PartyIDSource': "C"}
    counter_part_id_contra_firm_2 = {'PartyRole': "17", 'PartyID': 'ContraFirm2', 'PartyIDSource': "C"}
    counter_part_id_executing_firm = {'PartyRole': "1", 'PartyID': "ExecutingFirm", 'PartyIDSource': "C"}
    counterpart_id_investment_firm_cl_counterpart = {'PartyRole': "67", 'PartyID': "InvestmentFirm - ClCounterpart",
                                                     'PartyIDSource': "C"}
    counterpart_id_investment_firm_cl_counterpart_sa3 = {'PartyRole': "67",
                                                         'PartyID': "InvestmentFirm - ClCounterpart_SA3",
                                                         'PartyIDSource': "C"}
    counterpart_id_regulatory_body_venue_paris = {'PartyRole': "34",
                                                  'PartyID': "RegulatoryBody - Venue(Paris)",
                                                  'PartyIDSource': "C"}
    counterpart_id_settlement_location = {'PartyRole': '10',
                                          'PartyID': "CREST",
                                          'PartyIDSource': "D"}
    counterpart_id_euro_clear = {'PartyRole': '10',
                                          'PartyID': "EURO_CLEAR",
                                          'PartyIDSource': "D"}
    counterpart_java_api_user = {'PartyRole': '36',
                                          'PartyID': "JavaApiUser",
                                          'PartyIDSource': "D"}


class OMSCounterPartyIDs_JavaAPI(Enum):
    counterpart_executing_firm = {'PartyRole': 'EXF', 'CounterpartID': '200002'}
    counterpart_contra_firm = {'PartyRole': 'CNF', 'CounterpartID': '200003'}
    counterpart_contra_firm_2 = {'PartyRole': 'CNF', 'CounterpartID': '1000009'}
