from django.urls import path
from . import views
from django.views.generic import TemplateView
from .api import BookApi

urlpatterns = [
    path('', TemplateView.as_view(template_name="library/home.html")),

    path("student_registration/", views.student_registration, name="student_registration"),
    path("student_login/", views.student_login, name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),

    path("student/", views.student_main, name="student"),
    path("admin_main/", views.admin_main, name="admin_main"),
    path("logout/", views.Logout, name="logout"),

    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),

    path("view_students/", views.view_students, name="view_students"),
    path('books/', BookApi.as_view()),
    path("view_books/", views.view_books, name="view_books"),
    path("add_book/", views.add_book, name="add_book"),
    path("view_issued_books/", views.view_issued_books, name="view_issued_books"),
    path("issue_book/", views.issue_book, name="issue_book"),

    path('update_return_date/<int:data_id>/<str:new_date>/', views.update_return_date, name='update_return_date'),
    path('update_status/<int:book_id>/<str:new_status>/', views.update_status, name='update_status'),

    path("delete_issued_book/<int:myid>/", views.delete_issued_book, name="delete_issued_book"),
    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
]