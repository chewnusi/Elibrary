from rest_framework.generics import ListAPIView

from .serializers import BookSerializer, IssuedBookSerializer, PersonSerializer
from .models import Book, IssuedBook, Person

class BookApi(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class IssuedBookApi(ListAPIView):
    queryset = IssuedBook.objects.all()
    serializer_class = IssuedBookSerializer    

class PersonApi(ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer    