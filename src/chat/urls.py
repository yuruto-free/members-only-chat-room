from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('create/room', views.CreateRoom.as_view(), name='create_room'),
    path('update/room/<int:pk>', views.UpdateRoom.as_view(), name='update_room'),
    path('delete/room/<int:pk>', views.DeleteRoom.as_view(), name='delete_room'),
    path('enter/room/<int:pk>', views.EnterRoom.as_view(), name='enter_room'),
]