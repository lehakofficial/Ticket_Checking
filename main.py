import PyPDF2
import numpy as np
import os


def rename(old_name):
    file = open(old_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(file)
    pageObj = pdfReader.getPage(0)
    data0 = pageObj.extractText().split(sep='\n')
    if data0[3] == 'САПСАН Сидячий' and data0[4] == '("ЭКОНОМ")Для пассажиров с':
        data = pageObj.extractText().split(sep='\n')[23]
    elif data0[3] == 'САПСАН Сидячий':
        data = pageObj.extractText().split(sep='\n')[22]
    else:
        data = pageObj.extractText().split(sep='\n')[21]
    new_name = data + '.pdf'
    file.close()
    os.rename(old_name, new_name)


def renamer():
    name_lst = os.listdir()
    for i in name_lst:
        rename(i)


def sapsan_non_econom(data):
    passport = data[55].replace('СВИДЕТЕЛЬСТВО О РОЖДЕНИИ', 'ПАСПОРТ').split(sep=' ')[2]
    date_of_birth = data[56][:-1]
    male = data[58]
    surname = data[59]
    name = data[61][0]
    second_name = data[63][0]

    return surname, name, second_name, passport, date_of_birth, male


def double_cv(data):
    passport = data[53].replace('СВИДЕТЕЛЬСТВО О РОЖДЕНИИ', 'ПАСПОРТ').split(sep=' ')[2]
    date_of_birth = data[54][:-1]
    male = data[56]
    surname = data[57]
    name = data[59][0]
    second_name = data[61][0]

    return surname, name, second_name, passport, date_of_birth, male


def two_floor(data):
    passport_birth = data[19].replace('СВИДЕТЕЛЬСТВО О РОЖДЕНИИ', 'ПАСПОРТ').split(sep='ПАСПОРТ ')[1][4:].split(sep=' ')
    passport = passport_birth[0]
    date_of_birth = passport_birth[1]
    male = passport_birth[3]
    full_name = data[20].split(sep=' ')
    surname = full_name[0]
    name = full_name[1][0]
    second_name = full_name[2][0]

    return surname, name, second_name, passport, date_of_birth, male


def grand(data):
    passport = data[5].replace('СВИДЕТЕЛЬСТВО О РОЖДЕНИИ', 'ПАСПОРТ')
    date_of_birth = data[6][:10]
    male = data[6][-1]
    full_name = data[4][5:].split(sep=' ')
    surname = full_name[0]
    name = full_name[1][0]
    second_name = full_name[2][0]

    return surname, name, second_name, passport, date_of_birth, male


def red_arrow(data):
    # то же самое, что мегаполис
    passport_birth = data[20].replace('СВИДЕТЕЛЬСТВО О РОЖДЕНИИ', 'ПАСПОРТ').split(sep='ПАСПОРТ ')[1][4:].split(sep=' ')
    passport = passport_birth[0]
    date_of_birth = passport_birth[1]
    male = passport_birth[3]
    full_name = data[21].split(sep=' ')
    surname = full_name[0]
    name = full_name[1][0]
    second_name = full_name[2][0]

    return surname, name, second_name, passport, date_of_birth, male


def megapolis(data):

    # date_full = data[4][5:-3].split(sep=' ')
    # date_arrive = date_full[1]
    # time_arrive = date_full[0]
    # start = data[8][14:-16]
    # arrive = data[17][14:-29]
    passport_birth = data[20].replace('СВИДЕТЕЛЬСТВО О РОЖДЕНИИ', 'ПАСПОРТ').split(sep='ПАСПОРТ ')[1][4:].split(sep=' ')
    passport = passport_birth[0]
    date_of_birth = passport_birth[1]
    male = passport_birth[3]
    full_name = data[21].split(sep=' ')
    surname = full_name[0]
    name = full_name[1][0]
    second_name = full_name[2][0]

    return surname, name, second_name, passport, date_of_birth, male


def sapsan(data):
    # date_full = data[5][5:-3].split(sep=' ')
    # date_arrive = date_full[1]
    # time_arrive = date_full[0]
    # start = data[9].split(sep=' ')[2]
    # arrive = data[18][14:-29]
    if data[3] == 'САПСАН Сидячий' and data[4] == '("ЭКОНОМ")Для пассажиров с':
        passport_birth = data[22].split(sep='ПАСПОРТ ')[1][4:].split(sep=' ')
        passport = passport_birth[0]
        date_of_birth = passport_birth[1]
        male = passport_birth[3]
        full_name = data[23].split(sep=' ')
        surname = full_name[0]
        name = full_name[1][0]
        second_name = full_name[2][0]
    elif data[3] == 'САПСАН Сидячий':
        passport_birth = data[21].replace('СВИДЕТЕЛЬСТВО О РОЖДЕНИИ', 'ПАСПОРТ').split(sep='ПАСПОРТ ')[1][4:].split(sep=' ')
        passport = passport_birth[0]
        date_of_birth = passport_birth[1]
        male = passport_birth[3]
        full_name = data[22].split(sep=' ')
        surname = full_name[0]
        name = full_name[1][0]
        second_name = full_name[2][0]
    return surname, name, second_name, passport, date_of_birth, male


def get_ticket_info(file_name):
    file = open(file_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(file)

    pageObj = pdfReader.getPage(0)
    data = pageObj.extractText().split(sep='\n')
    file.close()
    train = data[3].split(sep=' ')[0]
    if train == 'САПСАН':
        ticket_info = sapsan(data=data)
    elif train == 'МЕГАПОЛИС':
        ticket_info = megapolis(data=data)
    elif (train == 'Купе' or train[:2] == 'СВ') and data[9] == 'ГлавныйГлавный':
        ticket_info = red_arrow(data=data)
    elif (train == 'Купе' or train[:2] == 'СВ') and data[9] == 'ЛадожскийЛадожский':
        ticket_info = two_floor(data=data)
    elif train == 'Год':
        ticket_info = grand(data=data)
    elif train == 'ВАГОН' and data[11] == 'СВ':
        ticket_info = double_cv(data=data)
    elif train == 'ВАГОН' and data[11] == 'САПСАН':
        ticket_info = sapsan_non_econom(data=data)
    else:
        ticket_info = 'cringe'
        print(f'{file_name} кринж')

    return ticket_info


def info_array(file_name):
    data = np.loadtxt(file_name + '.csv', delimiter=';', dtype=str)
    # data = data_raw[::2]
    # data_name = data[:, ::2]
    data_name = data[:, :1]
    data_passport = data[:, 1:2]

    new_array_of_passports = np.array(['Паспорт'])
    for i in data_passport:
        passport = i[0].replace(' ', '').replace('№', '')
        new_array_of_passports = np.vstack((new_array_of_passports, np.array(passport)))

    new_array_of_names = np.array(['Фамилия', 'Имя', 'Отчество'])
    for i in data_name:
        first = i[0].split(sep=' ')
        new_array_of_names = np.vstack((new_array_of_names, np.array(first)))

    # data = np.hstack(((new_array_of_names[1:]), new_array_of_passports[1:], data[:, 1:2]))

    data_raw_birthday = data[:, 2:]
    data = np.hstack((new_array_of_names[1:], new_array_of_passports[1:], data_raw_birthday))
    return data


def ticket_checker(data_base: str):
    name_list = os.listdir('tickets/')
    base = info_array(data_base)
    counter = 0
    for i in name_list:
        ticket = get_ticket_info('tickets/' + i)
        flag = False

        for j in base:
            a = j[0].upper()
            b = ticket[0]
            if j[0].upper() == ticket[0]:
                print(f'{j[0]} match')
                if j[0].upper() == ticket[0]:
                    pass
                else:
                    print(f'Ошибка в фамилии {j[0]}')
                if j[1][0] == ticket[1]:
                    pass
                else:
                    print(f'Ошибка в имени {j[0]}')
                if j[2][0] == ticket[2]:
                    pass
                else:
                    print(f'Ошибка в отчестве {j[0]}')
                if j[3][-4:] == ticket[3][-4:]:
                    pass
                else:
                    print(f'Ошибка в паспорте {j[0]}')
                a = j[4][:]
                b = ticket[4]
                if j[4][:] == ticket[4]:
                    pass
                else:
                    print(f'Ошибка в дате рождения {j[0]}')
                flag = True
                counter += 1
                break
            else:
                continue
        if flag:
            continue
        else:
            # continue
            print(f'{i} не найден')
    print(f'Проверено {counter} людей')


ticket_checker('Остров заблудших душ')
