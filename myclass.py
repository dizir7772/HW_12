from collections import UserDict
import datetime
import re


class AddressBook(UserDict):
    def __getstate__(self):
        data = self.__dict__.copy()
        return data
    def __setstate__(self, data):
        self.__dict__ = data
    def add_record(self, record):
        self.data[record.name.value] = record
    def iterator(self, n=0):
        records = list(self.data.items())
        if len(records)<=n:
            result = '\n'.join([f'{record[0]}: {record[1]}' for record in records])
            return result
        else:
            while records:
                result = '\n'.join([f'{record[0]}: {record[1]}' for record in records[:n]])
                yield result
                records = records[n:]   
    
    def search(self, string):
        record_list = []
        for record in self.data.values():
            if re.search(string, record.name.value)!=None:
                record_list.append(str(record))
            phones = ' '.join(record.phone.value)
            if re.search(string, phones)!=None:
                record_list.append(str(record))
        return '\n'.join(record_list)


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_phone):
        sanitize_phone = re.sub(r'\D', '', new_phone.strip())
        phone_pattern = '\d{10}|\d{12}'
        if not re.search(phone_pattern, str(sanitize_phone)):
            raise ValueError(f'{new_phone} is invalid. Please enter a 10 or 12 digit phone number.')
        else:
            self.__phone = new_phone


class Birthday(Field):
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            #trying to get date object from string
            valid_birth_date = datetime.strptime(value, '%d.%m.%Y')
            self.__value = valid_birth_date
        except ValueError: 
            raise ValueError('Date is invalid!')        

    def days_to_birthday(self, birth_date):    
        current_date = datetime.now()
        birthday = birth_date.replace(year = current_date.year)
        if current_date>birthday:
            birthday = birthday.replace(year = current_date.year+1)
        delta = birthday-current_date
        return f'{delta} days left to birthday!'


class Record:
    def __init__(self, name, phone='', birthday=Birthday(None)):
        self.name = name
        self.phone = [phone]
        self.birthday = birthday

    def __str__(self):
        phone_list = ', '.join([phone.value for phone in self.phones])
        result = f'name:{self.name.value}\nphones:{phone_list}\nbirthday:{self.birthday.value}'
        return result

    def add_phone(self, phone):
        self.phones.append(phone)
        
    def remove_phone(self, phone):
        self.phones.remove(phone)

    def change_phone(self, phone_1, phone_2):
        self.remove_phone(phone_1)
        self.add_phone(phone_2)

if __name__ == '__main__':
    pass
