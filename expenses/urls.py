from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
    path('summary/', views.monthly_summary, name='monthly_summary'),
    path('category-summary/', views.category_summary, name='category_summary'),
    path('charts/', views.charts_view, name='charts_view'),
    path('login/', auth_views.LoginView.as_view(template_name='expenses/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='expense_logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup_view, name='signup'),
    path('predict/', views.predict_expense, name='predict_expense'),
]