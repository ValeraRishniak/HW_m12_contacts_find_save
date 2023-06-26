from collections import UserDict
from datetime import datetime
import pickle
import re


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value
    
    #перевірка на коректний номер телефону
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        new_value = (
            value.removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if len(new_value) <= 12 and new_value.isdigit():
            self.__value = new_value
        else:
            print("Please, check your phone number. It contain only digits.")


class Birthday(Field):
    def __init__(self, value):
        self.value = value
        self.__value = None

    def __repr__(self):
        return datetime.strftime(self.__value, '%d.%m.%Y')

    #перевірка на коректну дату дня народження
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        try:
            date_birthday = datetime.strptime(value, '%d.%m.%Y')
            self.__value = date_birthday
        except ValueError:
            print("Please, enter correct birthday in format DD.MM.YYYY")


class Record:
    def __init__(self, name : Name, phone: Phone = None, birthday = None):
        self.name = name
        self.phones = []
        if isinstance(phone, Phone):
            self.phones.append(phone)
        if birthday:
            self.birthday = Birthday(birthday)    

    #додавання контакту
    def add_phone_num(self, phone):
        self.phones.append(phone)

    #видалення контакту
    def delete_phone_num(self, phone):
        for seq_num, i in enumerate(self.phones):
            if i == phone:
                self.phones.pop(seq_num)

    #редагування контакту
    def change_phone_num(self, old_phone, new_phone):
        for seq_num, i in enumerate(self.phones):
            if i == old_phone:
                self.phones[seq_num] = new_phone

    #днів до дня народження
    def days_to_birthday(self):
        date_now = datetime.now()
        date_birthday = datetime(year=date_now.year, month=self.month, day=self.day)
        if date_birthday.date() == date_now.date():
            return f'{self.name} has Birthday TODAY!!!'
        elif date_birthday < date_now:
            days_to_birth_day = (datetime(year=date_now.year + 1, month=self.month, day=self.day) - date_now).days
            return f'{self.name} will have Birthday on {days_to_birth_day} days'
        else:
            days_to_birth_day = (date_birthday - date_now).days
            return f'{self.name} will have Birthday on {days_to_birth_day+1} days'


class AddressBook(UserDict):
    file_to_save = "Contacts.txt"

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, n=2): # параметр n - по замовчуванню 2
        index = 1
        print_block = '-' * 50 + '\n'  # блоки виводу, пагінація
        for record in self.data.values(): # ітеруємось по словнику АдресБук
            print_block += str(record) + '\n'
            if index < n: #якщо індекс меньше нашої n - то додаюмо запис в нашу строку print_block
                index += 1
            else:
                yield print_block # якщо ж індекс більше чим параметр n - то повертаємо всі записи що зібрали
                index = 1
                print_block = '-' * 50 + '\n'
        yield print_block # повертаємо що залишилось

    # вивід на екран контактів
    def show_all(*args):
        result = f'Contacts list:\n'
        print_list = AddressBook.iterator()  # викликаємо метод ітератор в нашіх книги контактів
        for item in print_list:
            result += f'{item}'
        return result

    # зберігання у файл
    def save_to_file(self):
        with open(self.file_to_save, "wb") as file:
            pickle.dump(self, file)
    
    # завантаження данних із файла
    def read_from_file(self):
        with open(self.file_to_save, "rb") as file:
            self.data = pickle.load(file)
        return self
    
    # завантаження данних із файла
    def search(self, user_input):
        all_match = []
        match = re.findall("\w+", user_input)
        match_birthday = re.findall("\d{2}.\d{2}.\d{4}", user_input)
        if match.isalpha():
            for i in self.data.values:
                if match in i.name.value:
                    all_match.append(i)
        
        elif match.isdigit():
            for i in self.data.values:
                for j in i.phone:
                    if match in j.value:
                        all_match.append(i)
        
        elif match_birthday:
            for i in self.data.values:
                for j in i.birthday:
                    if match_birthday in j.value:
                        all_match.append(i)

        else:
            print(f'Please, try again! Request can contain only letters, numbers or numbers and dots.')
        
        return all_match



