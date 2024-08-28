import gspread


def ConnTable():
    gc = gspread.service_account(filename=r'file.json')

    sh = gc.open_by_key()

    return sh


def DataTable():
    sh = ConnTable()
    return sh.sheet1.get_all_records()


def GetPhoneTable(phone):
    data = DataTable()
    for i in range(0, len(data)):
        if data[i]['Номер телефона'] == phone:
            return data[i]
def OrderTable(phone):
    data = DataTable()
    res = {}
    index = 0
    for i in range(0, len(data)):
        if data[i]['Номер телефона'] == phone:
            res[index] =  [data[i]["ФИО"], data[i]['Номер телефона'], data[i]['Номер заказа'],data[i]['Дата'], data[i]['День недели'], data[i]['Магазин'] ,data[i]['Адрес'], data[i]['Примечание'], data[i]['Мастер'], data[i]['Номер мастера'], data[i]["Заказ"]]
            index+=1
    return res

print(OrderTable(79047868561))
