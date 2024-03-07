import datetime
import re


class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not re.match(r'\d{10}$', self.value):
            raise ValueError("Invalid phone format. Phone number must contain 10 digits.")

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        try:
            datetime.datetime.strptime(self.value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY format.")

class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
                break
        if not found:
            raise ValueError("Phone not found")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = ', '.join([phone.value for phone in self.phones])
        birthday_str = f", Birthday: {self.birthday.value}" if self.birthday else ""
        return f"Name: {self.name.value}, Phones: {phones_str}{birthday_str}"

class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, name, phones=None, birthday=None):
        self.records[name] = Record(name, phones, birthday)
        print(f"Record for {name} added.")

    def find(self, name):
        return self.records.get(name, None)

    def delete(self, name):
        if name in self.records:
            del self.records[name]
            print(f"Record for {name} removed.")
        else:
            print("Record not found.")

    def get_upcoming_birthdays(self, days=7):
        today = datetime.date.today()
        upcoming_birthdays = []
        for record in self.records.values():
            if record.birthday:
                birthday_date = datetime.datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                next_birthday = birthday_date.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                if (next_birthday - today).days <= days:
                    upcoming_birthdays.append(record.name.value)
        return upcoming_birthdays


def parse_input(user_input):
    parts = user_input.strip().split(maxsplit=2)  
    cmd = parts[0].lower()  
    args = parts[1:] if len(parts) > 1 else []  
    return cmd, args

def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        return "Contact not found."

def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
        return contacts[name]
    else:
        return "Contact not found."

def show_all_contacts(contacts):
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])




def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid value provided."
        except IndexError:
            return "Please provide enough arguments."
    return wrapper

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise IndexError
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise IndexError
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError
    return contacts[name]

@input_error
def show_all_contacts(contacts):
    if not contacts:
        return "No contacts found."
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])


def parse_input(user_input):
    parts = user_input.strip().split(maxsplit=2)  
    cmd = parts[0].lower()  
    args = parts[1:] if len(parts) > 1 else []  
    return cmd, args


def parse_input(user_input):
    parts = user_input.strip().split(maxsplit=2)  
    cmd = parts[0].lower()  
    args = parts[1:] if len(parts) > 1 else []  
    return cmd, args

def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid value provided."
        except IndexError:
            return "Please provide enough arguments."
    return wrapper

@input_error
def remove_contact(args, address_book):
    if len(args) != 1:
        raise IndexError("Please provide only a name.")
    name = args[0]
    address_book.delete(name)

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            name, *phones = args
            address_book.add_record(name, phones)
        elif command == "change":
            name, phone = args
            record = address_book.find(name)
            if record:
                record.edit_phone(record.phones[0].value, phone)
                print(f"Phone number for {name} updated.")
            else:
                print("Record not found.")
        elif command == "phone":
            name = args[0]
            record = address_book.find(name)
            if record:
                print(record)
            else:
                print("Record not found.")
        elif command == "all":
            for name, record in address_book.records.items():
                print(record)
        elif command == "add-birthday":
            name, birthday = args
            record = address_book.find(name)
            if record:
                record.add_birthday(birthday)
                print(f"Birthday for {name} added.")
            else:
                print("Record not found.")
        elif command == "show-birthday":
            name = args[0]
            record = address_book.find(name)
            if record and record.birthday:
                print(f"Birthday for {name}: {record.birthday.value}")
            else:
                print("Birthday not found or record not found.")
        elif command == "birthdays":
            upcoming_birthdays = address_book.get_upcoming_birthdays()
            if upcoming_birthdays:
                print("Upcoming birthdays:")
                for name in upcoming_birthdays:
                    print(name)
            else:
                print("No upcoming birthdays.")
        elif command == "remove":
            remove_contact(args, address_book)
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()

