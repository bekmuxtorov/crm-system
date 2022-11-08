from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),

    path('students/', views.StudentsPageView, name='students'),
    path('add_students/', views.AddStudentsView, name='add_students'),
    path('update_students/<int:pk>', views.UpdateStudentsView.as_view(), name='update_students'),
    path('delete_students/<int:pk>', views.DeleteStudentsView.as_view(), name='delete_students'),
    path('complate_students/', views.ComplateStudentsView, name='complate_students'),
    path('students/<int:pk>', views.SingleStudentsView, name='student'),


    # Groups section
    path('groups/', views.GroupsPageView, name='groups'),
    path('groups_add/', views.GroupsAddPageView, name='groups_add'),
    path('groups_completed', views.GroupsCompletedView, name='groups_completed'),
    path('groups_update/<int:pk>', views.GroupsUpdateView.as_view(), name='groups_update'),
    path('groups_delete/<int:pk>', views.GroupsDeleteView.as_view(), name='groups_delete'),
    path('groups_completed/', views.GroupsCompletedView, name='groups_completed'),
    path('groups_students/<int:pk>', views.GroupsStudentsView, name='groups_students'),

    # Teacher section
    path('teachers/', views.TeacherListView, name='teachers'),
    path('teachers_delete/<int:pk>', views.TeacherDeleteView.as_view(), name='teachers_delete'),
    path('teachers_update/<int:pk>', views.TeacherUpdateView.as_view(), name='teachers_update'),

    # Payments
    path('payments', views.PaymentsPageView, name='payments'),
    path('payments_groups/<int:pk>', views.PaymentsGroups, name='payments_groups'),
    path('payments_others', views.OthersPaymentsView, name='payments_others'),
    path('add_payments/', views.AddPaymentsView, name='add_payments'),

    # Single person
    path('accounts/single_person', views.AccountsSingleView, name='single_person'),
        
]