from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signup/buyer', views.signup_buyer, name='signup-buyer'),
    path('signup/offerer', views.signup_offerer, name='signup-offerer'),
    path('search', views.search, name='search'),
    path('offerers/<int:pk>/', views.offerer_detail, name='offerer-detail'),
    path('tickets/<int:pk>/', views.delete_ticket, name='ticket-detail'),
    path('tickets/<int:pk>/delete', views.delete_ticket, name='ticket-delete'),
    path('tickets/<int:pk>/edit', views.edit_ticket, name='ticket-edit'),
    path('tickets/<int:pk>/exchange', views.edit_ticket, name='ticket-exchange'),
    path('approve-offerer/<int:pk>/', views.approve_offerer, name='approve-offerer'),
    path('new-ticket/', views.new_ticket, name='new-ticket'),
]