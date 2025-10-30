from django.urls import path
from .views import main_view
from django.urls import path
from .views import main_view, logout_view  # ← aquí debe estar logout_view

urlpatterns = [
    path('', main_view, name='main'),
    #path('logout/', logout_view, name='logout'),
    path('logout/', logout_view, name='logout'),

]