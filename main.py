import PyPDF2
import numpy as np
import os


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


def parse_sapsan_ticket(ticket_data: list) -> tuple:
    if ticket_data[4].find("БИЗНЕС") != -1 or ticket_data[4].find("ПЕРВЫЙ") != -1:
        passport_number, date_of_birth = ticket_data[20].split(sep="ПАСПОРТРФ")[1].split(sep=" ")[:-1]
        second_name = ticket_data[22]
        try:
            surname, name = ticket_data[21].split(sep=" ")
        except ValueError:
            surname = name = ticket_data[21]
        male = ticket_data[20][-1]
    else:
        passport_number, date_of_birth = ticket_data[20].split(sep="ПАСПОРТРФ")[1].split(sep=" ")[:-1]
        second_name = ticket_data[22]
        surname = name = ticket_data[21]
        male = ticket_data[20][-1]
    return surname, name, second_name, passport_number, date_of_birth, male


def parse_megapolis_ticket(ticket_data: list) -> tuple:
    surname = name = ticket_data[20]
    second_name = ticket_data[21]
    passport_number, date_of_birth = ticket_data[19].split(sep="ПАСПОРТРФ")[1].split(sep=" ")[:-1]
    male = ticket_data[19][-1]
    return surname, name, second_name, passport_number, date_of_birth, male


def parse_grand_ticket(ticket_data: list) -> tuple:
    surname, name, second_name = ticket_data[6].replace(".", "").split(sep=" ")
    passport_number, date_of_birth = ticket_data[7].split(sep=" / ")[:2]
    male = ticket_data[7][-1]
    return surname, name, second_name, passport_number, date_of_birth, male


def parse_red_arrow_ticket(ticket_data: list) -> tuple:
    try:
       surname, name = ticket_data[20].split(sep=" ")
    except ValueError:
        surname = name = ticket_data[20]
    second_name = ticket_data[21]
    passport_number, date_of_birth = ticket_data[19].split(sep="ПАСПОРТРФ")[1].split(sep=" ")[:-1]
    male = ticket_data[19][-1]
    return surname, name, second_name, passport_number, date_of_birth, male


def parse_night_express_ticket(ticket_data: list) -> tuple:
    try:
       surname, name = ticket_data[20].split(sep=" ")
    except ValueError:
        surname = name = ticket_data[20]
    second_name = ticket_data[21]
    passport_number, date_of_birth = ticket_data[19].split(sep="ПАСПОРТРФ")[1].split(sep=" ")[:-1]
    male = ticket_data[19][-1]
    return surname, name, second_name, passport_number, date_of_birth, male


def get_ticket_info(file_name):
    file = open(file_name, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(file)
    page_obj = pdf_reader.getPage(0)
    ticket_data = page_obj.extractText().split(sep='\n')
    file.close()
    train = ticket_data[3].split(sep=' ')[0]
    if train == 'Купе' or train == "СВ":
        ticket_info = parse_red_arrow_ticket(ticket_data=ticket_data)
    elif train == "САПСАН":
        ticket_info = parse_sapsan_ticket(ticket_data=ticket_data)
    elif train == "МЕГАПОЛИС":
        ticket_info = parse_megapolis_ticket(ticket_data=ticket_data)
    elif train == "receipt":
        ticket_info = parse_grand_ticket(ticket_data=ticket_data)
    elif train == "Ночнойэкспресс":
        ticket_info = parse_night_express_ticket(ticket_data=ticket_data)

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

        (surname_from_ticket, name_from_ticket, second_name_from_ticket,
         passport_from_ticket, date_of_birth_from_ticket, male) = ticket

        for passenger in passports_base:
            surname_from_base = passenger[0].upper()
            name_from_base = passenger[1].upper()
            second_name_from_base = passenger[2].upper()
            passport_from_base = passenger[3]
            date_of_birth_from_base = passenger[4]

            if surname_from_ticket.find(surname_from_base) != -1:
                print(f'{surname_from_base} match')

                if surname_from_ticket.find(surname_from_base) == -1:
                    print(f'Ошибка в фамилии {surname_from_base}')
                if (name_from_base != name_from_ticket and
                        (len(name_from_ticket) == 1 and name_from_base[0] != name_from_ticket[0])
                ):
                    print(f'Ошибка в имени {surname_from_base}')
                if (second_name_from_ticket.find(second_name_from_base) == -1 and
                        (len(second_name_from_ticket) == 1 and second_name_from_base[0] != second_name_from_ticket[0])
                ):
                    print(f'Ошибка в отчестве {surname_from_base}')
                if (passport_from_base != passport_from_ticket and
                        passport_from_base[-4:] != passport_from_ticket[-4:]
                ):
                    print(f'Ошибка в паспорте {surname_from_base}')
                if not date_of_birth_from_base == date_of_birth_from_ticket:
                    print(f'Ошибка в дате рождения {surname_from_base}')

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


check_tickets("Дядя Ваня", "Спб")

