from django.urls import path
from myapp import views

app_name = " "

urlpatterns = [
    # http://127.0.0.1:8000/myapp/hello/
    path('', views.index),
    path('<int:my_id>/', views.indexItem, name='detail'),
    # http://127.0.0.1:8000/myapp/contacts/
]