from django.urls import path

from hello import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fancy-hello', views.fancy_index, name='fancy_index'),
    path('<str:name>', views.hello_name, name='hello_name'),
]

