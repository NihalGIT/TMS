from django.contrib import admin
from django.urls import path
import tasks.views as views

urlpatterns = [
    path('', views.index,name="Login"),
    path('Home/', views.connection,name="Home"),
    path('Home/Form/', views.form,name="Form"),
    path('Home/Resultat/', views.resp ,name="Resultat"),
    path('admin/', admin.site.urls),
]
