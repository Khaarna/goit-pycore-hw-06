from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing contact name. Required field."""
    
    def __init__(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    """Class for storing phone number with validation (10 digits)."""
    
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)
    
    @staticmethod
    def validate(value):
        """Validate that phone number contains exactly 10 digits."""
        return value.isdigit() and len(value) == 10


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """Add a phone number to the record."""
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        """Remove a phone number from the record."""
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone {phone} not found")
    
    def edit_phone(self, old_phone, new_phone):
        """Edit an existing phone number."""
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            # Validate by creating Phone object (raises ValueError if invalid)
            new_phone_obj = Phone(new_phone)
            phone_to_edit.value = new_phone_obj.value
        else:
            raise ValueError(f"Phone {old_phone} not found")
    
    def find_phone(self, phone):
        """Find and return a phone number object."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Class for storing and managing contact records."""
    
    def add_record(self, record):
        """Add a record to the address book."""
        self.data[record.name.value] = record
    
    def find(self, name):
        """Find a record by name."""
        return self.data.get(name)
    
    def delete(self, name):
        """Delete a record by name."""
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found")


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
