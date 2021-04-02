from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('new/',views.getNewMsg,name='newMsg'),
    path('email/<int:pk>',views.MessagesDetailView.as_view(),name='email_detail'),
    path('spam/',views.get_spam,name='spam')
]