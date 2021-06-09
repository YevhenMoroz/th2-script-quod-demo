class RoutesConstants:
    ROUTES_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Routes ']"
#   -----Main page-----
    NAME_FILTER = '//*[@class="ag-header-container"]//div[2]/div[2]//*[@class="ag-input-wrapper"]//input'
    DESCRIPTION_FILTER = '//*[@class="ag-header-container"]//div[2]/div[1]//*[@class="ag-input-wrapper"]//input'
    ES_INSTANCE_FILTER = '//*[@class="ag-header-container"]//div[2]/div[3]//*[@class="ag-input-wrapper"]//input'
    CLIENT_ID_FILTER = '//*[@class="ag-header-container"]//div[2]/div[4]//*[@class="ag-input-wrapper"]//input'
    DEFAULT_STRATEGY_TYPE_FILTER = '//*[@class="ag-header-container"]//div[2]/div[5]//*[@class="ag-input-wrapper"]//input'
    COUNTERPART_FILTER = '//*[@class="ag-header-container"]//div[2]/div[6]//*[@class="ag-input-wrapper"]//input'
    SUPPORT_CONTRA_FIRM_COMMISSION_FILTER = '//*[@class="ag-header-container"]//div[2]/div[7]//select'

    NAME_VALUE = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="routeName"]//*[@ref="eValue"]'
    DESCRIPTION_VALUE = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="routeDescription"]//*[@ref="eValue"]'
    ES_INSTANCE_VALUE = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="ESInstanceID"]//*[@ref="eValue"]'
    CLIENT_ID_VALUE = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="clientRouteID"]//*[@ref="eValue"]'
    DEFAULT_STRATEGY_TYPE_VALUE = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="defaultScenario.scenarioName"]//*[@ref="eValue"]'
    COUNTERPART_VALUE = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="counterpart.counterpartName"]//*[@ref="eValue"]'
    SUPPORT_CONTRA_FIRM_COMMISSION_VALUE = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="supportContraFirmCommission"]//input'

    NEW_BUTTON = '//button[text()="New"]'
    REFRESH_PAGE = '//*[@data-name="refresh"]'
    MORE_ACTIONS = '//*[@data-name="more-vertical"]'
    EDIT_AT_MORE_ACTIONS = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS = '//*[@data-name="copy"]'
    DELETE_AT_MORE_ACTIONS = '//*[@data-name="trash-2"]'

# ------Edit------
    #--Values tab--

    NAME_AT_VALUES_TAB = '//*[@formcontrolname="routeName"]'
    CLIENT_ID_AT_VALUES_TAB ='//*[text()="Client ID"]'
    ES_INSTANCE_AT_VALUES_TAB='//*[text()="ES Instance"]'
    DESCRIPTION_AT_VALUES_TAB ='//*[@id="routeDescription"]'
    COUNTERPART_AT_VALUES_TAB ='//*[@id="counterpart"]'

