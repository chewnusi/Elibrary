from library.forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from .forms import IssueBookForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "student_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        student = Person.objects.create(user=user, phone=phone)
        user.save()
        student.save()
        alert = True
        return render(request, "student_registration.html", {'alert':alert})
    return render(request, "student_registration.html")

def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!")
            else:
                return redirect("/library/student")
        else:
            alert = True
            return render(request, "student_login.html", {'alert':alert})
    return render(request, "student_login.html")

def admin_login(request):
    alert=False
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/library/admin_main")
            else:
                return HttpResponse("You are not an admin!")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html", {'alert': alert})

def Logout(request):
    logout(request)
    return redirect ("/library/")

@login_required(login_url = '/student_login')
def student_main(request):
    return render(request, "student_main.html")

@login_required(login_url = '/admin_login')
def admin_main(request):
    return render(request, "admin_main.html")

@login_required(login_url = '/student_login')
def profile(request):
    return render(request, "profile.html")

@login_required(login_url = '/student_login')
def edit_profile(request):
    student = Person.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']

        student.user.email = email
        student.phone = phone
        student.user.save()
        student.save()
        alert = True
        return render(request, "edit_profile.html", {'alert':alert})
    return render(request, "edit_profile.html")

def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "change_password.html")

@login_required(login_url = '/student_login')
def student_issued_books(request):
    student = request.user.person  
    issued_books = IssuedBook.objects.filter(user=student)

    table_data = []
    for issued_book in issued_books:
        book_info = {
            'isbn': issued_book.book.isbn,
            'title': issued_book.book.title,
            'author': issued_book.book.author,
            'issued_date': issued_book.issued_date,
            'expiry_date': issued_book.expiry_date,
        }
        table_data.append(book_info)

    return render(request, 'student_issued_books.html', {'table_data': table_data})

@login_required(login_url = '/admin_login')
def view_students(request):
    students = Person.objects.all()
    return render(request, "view_students.html", {'students':students})

@login_required(login_url = '/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books':books})

@login_required(login_url = '/admin_login')
def view_issued_books(request):
    issued_books = IssuedBook.objects.all()
    context = {'issued_books': issued_books}
    return render(request, 'view_issued_books.html', context)

def update_status(request, book_id, new_status):
    book = get_object_or_404(Book, id=book_id)
    book.status = new_status
    book.save()
    return JsonResponse({'success': True})

def update_return_date(request, data_id, new_date):
    issuedbook = get_object_or_404(IssuedBook, id=data_id)
    issuedbook.return_date = new_date
    issuedbook.save()
    return JsonResponse({'success': True})

@login_required(login_url = '/admin_login')
def add_book(request):
    book_added = False
    if request.method == "POST":
        isbn = request.POST['isbn']
        title = request.POST['title']
        author = request.POST['author']
        category = request.POST['category']

        books = Book.objects.create(title=title, author=author, isbn=isbn, category=category)
        books.save()
        alert = True
        book_added = True
        return render(request, "add_book.html", {'alert':alert})
    return render(request, "add_book.html", {'book_added': book_added})

@login_required(login_url='/admin_login')
def issue_book(request):
    form = IssueBookForm()
    alert = False
    person_not_found = False
    book_not_found = False
    book_unavailable = False  
    book_borrowed = False

    if request.method == "POST":
        form = IssueBookForm(request.POST)
        if form.is_valid():
            book_isbn = form.cleaned_data['book_isbn']
            student_surname = form.cleaned_data['student_surname']

            try:
                book = Book.objects.get(isbn=book_isbn)

                if book.status == 'available':
                    student = Person.objects.get(user__last_name=student_surname)

                    obj = IssuedBook()
                    obj.book = book
                    obj.user = student
                    obj.save()

                    book.status = 'checked out'
                    book.save()

                    alert = True
                    book_borrowed = True
                else:
                    book_unavailable = True

            except Book.DoesNotExist:
                book_not_found = True
            except Person.DoesNotExist:
                person_not_found = True

    return render(request, "issue_book.html", {
        'form': form,
        'alert': alert,
        'person_not_found': person_not_found,
        'book_not_found': book_not_found,
        'book_unavailable': book_unavailable, 
        'book_borrowed': book_borrowed,
    })
def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/library/view_books")

def delete_issued_book(request, myid):
    data = IssuedBook.objects.filter(id=myid)
    data.delete()
    return redirect("/library/view_issued_books")

def delete_student(request, myid):
    students = Person.objects.filter(id=myid)
    students.delete()
    return redirect("/library/view_students")