from django.contrib import admin
from .models import Book, IssuedBook, Person

admin.site.register(Book)
admin.site.register(IssuedBook)
admin.site.register(Person)
