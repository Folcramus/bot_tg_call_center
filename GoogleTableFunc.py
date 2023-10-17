import gspread


def ConnTable():
    gc = gspread.service_account(filename=r'file.json')

    sh = gc.open_by_key('1bd1QoaY-O60n3AYY_MjTFQtIOTG5LBMp8o8IcU7e2ac')

    return sh


def GetPhoneTable(phone):
    sh = ConnTable()
    data = sh.sheet1.get_all_records()

    for i in range(0,len(data)):
        if data[i]["Телефон"] == phone:
            return data[i]


