import gspread


def ConnTable():
    gc = gspread.service_account(filename=r'file.json')

    sh = gc.open_by_key('1P-7eFZ3YXLnuWlEX2_pNLJ2mlKc8Tf7BIU7py4raCo4')

    return sh


def GetPhoneTable(phone):
    sh = ConnTable()
    data = sh.sheet1.get_all_records()
    for i in range(0,len(data)):
        if data[i]['Номер телефона'] == phone:
            return data[i]


