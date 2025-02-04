from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('inspection/<int:step>/', views.inspection_step, name='inspection_step'),
    path('inspection_complete/', views.inspection_complete, name='inspection_complete'),
    path('inspection_form/', views.inspection_form_view, name='inspection_form'),
    path('autosave_inspection/', views.autosave_inspection, name='autosave_inspection'),
]