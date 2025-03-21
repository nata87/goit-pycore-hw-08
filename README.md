# Домашнє завдання: Серіалізація та копіювання об'єктів в Python

## Функціонал

- Збереження **стану адресної книги** у файл перед виходом з програми.
- Відновлення даних **під час запуску** програми.
- Використання `pickle` для серіалізації та десеріалізації даних.

---

### Серіалізація та десеріалізація з `pickle`

```python
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Якщо файл не знайдено, створюється нова адресна книга
```

### Інтеграція збереження у програму

```python
def main():
    book = load_data()

    # Основний цикл роботи з адресною книгою

    save_data(book)  # Збереження перед виходом
```

---

### Основний цикл роботи

1. При **запуску програми** дані завантажуються з файлу `addressbook.pkl`.
2. Ви можете **додавати, видаляти, редагувати контакти** в адресній книзі.
3. При **виході з програми** всі зміни зберігаються у файл `addressbook.pkl`.
