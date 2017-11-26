# Створіть за допомогою класів та продемонструйте свою реалізацію шкільної
# бібліотеки(включіть фантазію).


class Book(object):
    """Implement Book object


    """
    counter = 0

    def __init__(self, grade, subject, title, **kwargs):
        """Constructor for Book object

        Keyword arguments:
        grade -->(int) number of recommend school grage (1, 2, 3 ...)
        subject -->(str) school subject of book (like 'history', 'physics')
        title -->(str) book's title
        **kwargs --> other info about book (like author, ISBN, keywords etc.)
        """

        self.grade = int(grade)
        # Convert 'subject' to upper for prevent double saving of same
        # subject and keep strings like "history of Ukraine" in correct
        # capitalizing
        self.subject = str(subject).upper()
        self.title = str(title)
        self.book_id = Book.counter
        Book.counter += 1
        self.args = kwargs

    def __str__(self):
        """Overload standart method for readable string representation"""
        s = "ID: {id}\nFor grade #{grade}\n\
Subject: {subject}\nTitle: {title}".format(id=self.book_id, grade=self.grade,
                                           subject=self.subject,
                                           title=self.title)
        if self.args:
            for k, v in self.args.items():
                s += "\n{key}: {value}".format(key=str(k).capitalize(),
                                               value=v)
        return s


class Library(object):
    """Implement Library object"""
    _books = []
    _grades = []
    _subjects = []

    def __init__(self, title):
        """Constructor for Library object

        Keyword arguments:
        title -->(str) name of created library
        """
        self.title = title

    @property
    def book_count(self):
        return len(self._books)

    @property
    def grades(self):
        return tuple(set(self._grades))

    @property
    def subjects(self):
        return tuple(set(self._subjects))

    def add_book(self, *books):
        """Add instance of Book to Library

        Print out result and return count of books in Library.
        """
        for book in books:
            if not self.get_book(book.book_id):
                self._books.append(book)
                self._grades.append(book.grade)
                self._subjects.append(book.subject)
                print("Book #{} added!".format(book.book_id))
            else:
                print("Book #{} is already in Library!".format(book.book_id))
        return len(self._books)

    def del_book(self, book_id):
        """Remove Book with selected book_id from Library

        Print out result and return count of books in Library.

        Keyword arguments:
        book_id -->(int) ID of book in Library
        """
        book = self.get_book(book_id)
        if book:
            self._books.remove(book)
            self._grades.remove(book.grade)
            self._subjects.remove(book.subject.upper())
            print("Book #{} removed!".format(book.book_id))
        else:
            print("Book #{} not found!".format(book.book_id))
        return len(self._books)

    def get_book(self, book_id):
        """Search book in Library by ID

        If found - return instance of a Book
        If not found - return None

        Keyword arguments:
        book_id -->(int) ID of book in Library
        """
        book = list(filter(lambda i: i.book_id == book_id, self._books))
        if len(book):
            return book[0]
        else:
            return None

    def book_info(self, book_id):
        """Display book's info

        If found - return (str)book
        If not found - return None

        Keyword arguments:
        book_id -->(int) ID of book in Library
        """
        book = self.get_book(book_id)
        if book:
            print("--------- Book info ---------")
            print(book)
            print("------------ END ------------")
            return str(book)
        else:
            print("Book #{} not found!".format(book_id))
            return None

    def get_books_grade(self, grade):
        """Display books for selected grade

        If found - return list with instances of Book
        If not found - return None

        Keyword arguments:
        grade -->(int) grade number
        """
        if grade in self._grades:
            return [self.get_book(i.book_id) for i in
                    list(filter(lambda x: x.grade == grade, self._books))]
        else:
            return None

    def get_books_subject(self, subject):
        """Display books for selected subject

        If found - return list with instances of Book
        If not found - return None

        Keyword arguments:
        subject -->(str) name of subject
        """
        subj = str(subject).upper()
        if subj in self._subjects:
            return [self.get_book(i.book_id) for i in
                    list(filter(lambda x:
                                x.subject.upper() == subj, self._books))]
        else:
            return None


# ----------------------- TEST ------------------
libr = Library("School #28")
a = Book(11, "Географія", "Географія")
b = Book(11, "Історія", "Всесвітня історія")
c = Book(11, "Історія", "Історія України")
d = Book(11, "Хімія", "Хімія", author="Лашевська")
e = Book(11, "Хімія", "Хімія", author="Величко")
libr.add_book(a, b, c, d, e)
libr.book_info(3)
libr.add_book(Book(2, "Математика", "Математика", author="Рівкінд"))
libr.add_book(Book(2, "Основи здоров'я", "Основи здоров'я"))
libr.add_book(Book(2, "Основи здоров'я", "Основи здоров'я. Зошит-практикум"))
print("Books for second grade: ", libr.get_books_grade(2))
print("Books on 'Історія': ", libr.get_books_subject("історія"))
print("Grades: ", libr.grades)
print("Subjects: ", libr.subjects)
print("Count of books: ", libr.book_count)
print("Book counter: ", Book.counter)
libr.del_book(2)
libr.add_book(Book(11, "Геометрія", "Геометрія", author="Бевз"))
print("Count of books: ", libr.book_count)
print("Book counter: ", Book.counter)
