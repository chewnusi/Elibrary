from django import forms

class IssueBookForm(forms.Form):
    book_isbn = forms.CharField(label="Book ISBN", max_length=13)
    student_surname = forms.CharField(label="Student Surname", max_length=100)