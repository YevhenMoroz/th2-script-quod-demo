
def check_order_status(ord_status):
    number = '0'
    if ord_status == 'Filled':
        number = '2'
    elif ord_status == 'Rejected':
        number = '8'
    else:
        number = '0'
    return number

def prepeare_tif(tif):
    new_tif = ''
    if tif == '4':
        new_tif = 'Fill or Kill'
    elif tif == '3':
        new_tif = 'Immediate or Cancel'
    elif tif == '0':
        new_tif = 'Day'
    elif tif == '1':
        new_tif = 'Good till Cancel'
    return new_tif

def parse_settl_type(settl_type):
    new_settl_type=''
    if settl_type=='MO1':
        new_settl_type='M1'
    return new_settl_type
