import pickle
from datetime import datetime, timedelta
from collections import UserDict
import re

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact does not exist.'
        except ValueError:
            return 'Give me valid data please.'
        except IndexError:
            return 'Not enough arguments provided.'
    return inner

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return f"Phone number {old_phone} changed to {new_phone}."
        return "Old phone number not found."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year <= next_week:
                    upcoming.append(f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}")
        return "\n".join(upcoming) if upcoming else "No upcoming birthdays."

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book.data, f)
    print("Дані збережено.")

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
        book = AddressBook()
        book.data = data
        print("Дані завантажено.")
        return book
    except FileNotFoundError:
        print("Файл не знайдено, створюємо нову адресну книгу.")
        return AddressBook()

def parse_input(user_input):
    parts = user_input.strip().split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1].split() if len(parts) > 1 else []
    return command, args

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return record.change_phone(old_phone, new_phone)

@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return ", ".join(phone.value for phone in record.phones) if record.phones else "No phone numbers found."

@input_error
def show_all(book):
    if not book.data:
        return "No contacts found."
    return "\n".join(f"{name}: {', '.join(phone.value for phone in record.phones)}" for name, record in book.data.items())

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "No birthday set."

@input_error
def birthdays(book):
    return book.get_upcoming_birthdays()

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()
