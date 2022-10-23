from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView, name='home'),

    path('students/', views.StudentsPageView, name='students'),
    path('add_students/', views.AddStudentsView, name='add_students'),
    path('update_students/<int:pk>', views.UpdateStudentsView.as_view(), name='update_students'),
    path('delete_students/<int:pk>', views.DeleteStudentsView.as_view(), name='delete_students'),
    path('complate_students/', views.ComplateStudentsView, name='complate_students'),

    # Groups section
    path('groups/', views.GroupsPageView, name='groups'),
    path('groups_add/', views.GroupsAddPageView, name='groups_add'),
    path('groups_completed', views.GroupsCompletedView, name='groups_completed'),
    path('groups_update/<int:pk>', views.GroupsUpdateView.as_view(), name='groups_update'),
    path('groups_delete/<int:pk>', views.GroupsDeleteView.as_view(), name='groups_delete'),
    path('groups_completed/', views.GroupsCompletedView, name='groups_completed'),
    path('groups_students/<int:pk>', views.GroupsStudentsView, name='groups_students'),
    
]