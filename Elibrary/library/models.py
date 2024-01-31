from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta


class Book(models.Model):
    AVAILABLE = 'available'
    CHECKED_OUT = 'checked out'
    DAMAGED = 'damaged'
    LOST = 'lost'

    STATUS_CHOICES = (
        (AVAILABLE, 'Available'),
        (CHECKED_OUT, 'Checked Out'),
        (DAMAGED, 'Damaged'),
        (LOST, 'Lost'),
    )

    isbn = models.CharField(max_length=10, blank=True)
    title = models.CharField(max_length=225)
    author = models.CharField(max_length=225, blank=True)
    category = models.CharField(max_length=50, blank=True)
    status = models.CharField(default=AVAILABLE, max_length=100, choices=STATUS_CHOICES)

    def __str__(self):
        return "{}".format(self.title)

class Person(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, blank=True)

    def __str__(self):
        return "{}".format(self.user.username)


def expiry():
    return datetime.today() + timedelta(days=10)

class IssuedBook(models.Model):

    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='issued_books', default=None)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issued_books', default=None)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
    return_date = models.DateField(blank=True, null=True, default=None)
