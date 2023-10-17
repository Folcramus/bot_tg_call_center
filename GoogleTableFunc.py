import gspread


def ConnTable():
    gc = gspread.service_account(filename=r'file.json')

    sh = gc.open_by_key('1qSJncekRpbXCmkLCuLnNZC6ugPVnnpNoYhtSlniZVoM')

    return sh


def GetPhoneTable(phone):
    sh = ConnTable()
    data = sh.sheet1.acell('B1').value
    print(data)
    for i in range(0,len(data)):
        if data[i]["Телефон"] == phone:
            return data[i]


GetPhoneTable(1)