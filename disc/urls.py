from django.urls import path
from . import views

app_name='disc'

urlpatterns=[
    path('',views.disc_index,name='disc_index'),
    path('disc_add/',views.disc_add,name='disc_add'),
    path('disc_delete/',views.disc_delete,name='disc_delete'),
    path('disc_update/',views.disc_update,name='disc_update'),
]