class Book:
    def __init__(self,title, author):
        self.title = title
        self.author = author

    def get_data(self):
        return f'{self},{self.title,self.author}'

book = Book("Python Basics", "John Doe")
print(book.title)
print(book.author)
