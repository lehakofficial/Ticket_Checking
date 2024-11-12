import PyPDF2
import numpy as np
import os

from pyasn1.codec.ber.decoder import decode


def rename(old_name):
    file = open('tickets to rename/' + old_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(file)
    pageObj = pdfReader.getPage(0)
    data0 = pageObj.extractText().split(sep='\n')
    if data0[3] == 'САПСАН Сидячий' and data0[4] == '("ЭКОНОМ")Для пассажиров с':
        data = pageObj.extractText().split(sep='\n')[23]
    elif data0[3] == 'САПСАН Сидячий':
        data = pageObj.extractText().split(sep='\n')[22]
    else:
        data = pageObj.extractText().split(sep='\n')[21]
    new_name = 'renamed tickets/' + data + '.pdf'
    file.close()
    os.rename('tickets to rename/' + old_name, new_name)


def renamer():
    name_lst = os.listdir('tickets to rename/')
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
    """
    Для поезда 233 в 01:05 тоже работает
    """

    passport_birth = data[20].replace('СВИДЕТЕЛЬСТВО О РОЖДЕНИИ', 'ПАСПОРТ').split(sep='ПАСПОРТ ')[1][3:].split(sep=' ')
    passport = passport_birth[0]
    date_of_birth = passport_birth[1]
    male = passport_birth[3]
    full_name = data[21].split(sep=' ')
    if len(full_name) > 3:
        surname = full_name[0]
        name = full_name[1]
        second_name = full_name[-1]
    else:
        surname = full_name[0]
        name = full_name[-1]
        length = int(len(data[22])/2)
        second_name = data[22][:-int(len(data[22])/2)]

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


def parse_sapsan_econom_ticket(ticket_data: list) -> tuple:
    # if data[3] == 'САПСАН Сидячий' and data[4] == '("ЭКОНОМ")Для пассажиров с':
    #     passport_birth = data[22].split(sep='ПАСПОРТ ')[1][4:].split(sep=' ')
    #     passport = passport_birth[0]
    #     date_of_birth = passport_birth[1]
    #     male = passport_birth[3]
    #     full_name = data[23].split(sep=' ')
    #     surname = full_name[0]
    #     name = full_name[1][0]
    #     second_name = full_name[2][0]
    # elif data[3] == 'САПСАН Сидячий':
    date_of_birth = ticket_data[21].replace('СВИДЕТЕЛЬСТВО О РОЖДЕНИИ', 'ПАСПОРТ').split(sep='ПАСПОРТ ')[1][3:].split(sep=' ')
    passport_number = date_of_birth[0]
    date_of_birth = date_of_birth[1]
    male = date_of_birth[3]
    full_name = ticket_data[22].split(sep=' ')
    if len(full_name) > 3:
        surname = full_name[0]
        name = full_name[1]
        second_name = full_name[-1]
    else:
        surname = full_name[0]
        name = full_name[-1]
        second_name = ticket_data[23][:-int(len(ticket_data[23])/2)]
    return surname, name, second_name, passport_number, date_of_birth, male


def parse_sapsan_business_ticket(ticket_data: list) -> tuple:
    passport_number, date_of_birth = ticket_data[20].split(sep="ПАСПОРТРФ")[1].split(sep=" ")[:-1]
    second_name = ticket_data[22]
    surname, name = ticket_data[21].split(sep=" ")
    male = ticket_data[20][-1]
    return surname, name, second_name, passport_number, date_of_birth, male


def grand_by_rgd(data):
    passport = data[7].replace('СВИДЕТЕЛЬСТВО О РОЖДЕНИИ', 'ПАСПОРТ')
    date_of_birth = data[8][:10]
    male = data[8][-1]
    full_name = data[6].split(sep=' ')
    surname = full_name[0]
    name = full_name[1][0]
    second_name = full_name[2][0]

    return surname, name, second_name, passport, date_of_birth, male


def get_ticket_info_old(file_name):
    file = open(file_name, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(file)
    page_obj = pdf_reader.getPage(0)
    data = page_obj.extractText().split(sep='\n')
    file.close()
    train = data[3].split(sep=' ')[0]
    if train == 'САПСАН':
        ticket_info = parse_sapsan_econom_ticket(ticket_data=data)
    elif train == 'МЕГАПОЛИС':
        ticket_info = megapolis(data=data)
    elif (train == 'Купе' or train[:2] == 'СВ') and data[9] == 'ГлавныйГлавный':
        ticket_info = red_arrow(data=data)
    elif (train == 'Купе' or train[:2] == 'СВ') and data[9] == 'ЛадожскийЛадожский':
        ticket_info = two_floor(data=data)
    elif train == 'Год':
        ticket_info = grand_by_rgd(data=data)
        # ticket_info = grand(data=data)
    elif train == 'ВАГОН' and data[11] == 'СВ':
        ticket_info = double_cv(data=data)
    elif train == 'ВАГОН' and data[11] == 'САПСАН':
        ticket_info = sapsan_non_econom(data=data)
    else:
        ticket_info = 'cringe'
        print(f'{file_name} кринж')

    return ticket_info


def get_ticket_info(file_name):
    file = open(file_name, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(file)
    page_obj = pdf_reader.getPage(0)
    ticket_data = page_obj.extractText().split(sep='\n')
    file.close()
    train = ticket_data[3].split(sep=' ')[0]
    if train == 'Купе':
        ticket_info = red_arrow(data=ticket_data)
    elif train == "САПСАН" and ticket_data[4].find("БИЗНЕС"):
        ticket_info = parse_sapsan_business_ticket(ticket_data=ticket_data)
    elif train == "САПСАН":
        ticket_info = parse_sapsan_econom_ticket(ticket_data=ticket_data)


    else:
        ticket_info = 'cringe'
        print(f'Не найден поезд для {file_name}')

    return ticket_info


def get_info_from_file(file_name: str) -> np.ndarray:
    data = np.loadtxt(f"{file_name}.csv", delimiter=';', dtype=str)
    # data = data_raw[::2]
    # data_name = data[:, ::2]
    names_column = data[:, :1]
    passports_column = data[:, 1:2]

    formatted_passports_column = np.array(['Паспорт'])
    for passport in passports_column:
        formatted_passport = passport[0].replace(" ", "").replace("№", "")
        formatted_passports_column = np.vstack((formatted_passports_column, np.array(formatted_passport)))

    formatted_names_column = np.array(['Фамилия', 'Имя', 'Отчество'])
    for name in names_column:
        formatted_name = (name[0] if name[0][-1] != " "  else name[0][:-1]).replace("  ", " ").split(sep=' ')
        formatted_names_column = np.vstack((formatted_names_column, np.array(formatted_name)))

    # data = np.hstack(((new_array_of_names[1:]), new_array_of_passports[1:], data[:, 1:2]))

    data_raw_birthday = data[:, 2:]
    data = np.hstack((formatted_names_column[1:], formatted_passports_column[1:], data_raw_birthday))
    return data


def get_tickets_files_names(path = "tickets/") -> list:
    return os.listdir(path)



def check_tickets(data_base_path: str, tickets_path: str):
    tickets_files_names = get_tickets_files_names(path=tickets_path)
    passports_base = get_info_from_file(file_name=data_base_path)
    counter = 0
    for ticket_file in tickets_files_names:
        ticket = get_ticket_info(f"{tickets_path}/{ticket_file}")
        flag = False

        for j in passports_base:
            surname_from_base = j[0].upper()
            name_from_base = j[1].upper()
            second_name_from_base = j[2].upper()
            passport_from_base = j[3]
            date_of_birth_from_base = j[4]

            surname_from_ticket = ticket[0]
            name_from_ticket = ticket[1]
            second_name_from_ticket = ticket[2]
            passport_from_ticket = ticket[3]
            date_of_birth_from_ticket = ticket[4]
            male_from_ticket = ticket[5]

            if surname_from_base == surname_from_ticket:
                print(f'{j[0]} match')
                if j[0].upper() == ticket[0]:
                    pass
                else:
                    print(f'Ошибка в фамилии {j[0]}')
                if name_from_base == name_from_ticket:
                    pass
                else:
                    print(f'Ошибка в имени {j[0]}')
                if second_name_from_base == second_name_from_ticket:
                    pass
                else:
                    print(f'Ошибка в отчестве {j[0]}')
                if passport_from_base == passport_from_ticket:
                    pass
                else:
                    print(f'Ошибка в паспорте {j[0]}')
                if date_of_birth_from_base == date_of_birth_from_ticket:
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
            print(f'{ticket_file} не найден')
    print(f'Проверено {counter} людей')


check_tickets("Дядя Ваня", "Мск")

