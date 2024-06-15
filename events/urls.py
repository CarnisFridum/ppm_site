
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('list_event', views.list_event, name="list-event"),
    path('list_venue', views.list_venue, name="list-venue"),
    path('add_venue', views.add_venue, name="add-venue"),
    path('add_event', views.add_event, name="add-event"),
    path('update_venue/<venue_id>', views.update_venue, name="update-venue"),
    path('update_event/<event_id>', views.update_event, name="update-event"),
    path('delete_venue/<venue_id>', views.delete_venue, name="delete-venue"),
    path('delete_event/<event_id>', views.delete_event, name="delete-event"),
    path('attend_event/<event_id>', views.attend_event, name="attend-event"),
    path('disattend_event/<event_id>', views.disattend_event, name="disattend-event"),
    path('show_venue/<venue_id>', views.show_venue, name="show-venue"),
    path('show_venue/<venue_id>/<int:year>/<str:month>/', views.show_venue, name="show-venue"),
    path('show_event/<event_id>', views.show_event, name="show-event"),
    path('show_user/<user_id>', views.show_user, name="show-user"),
    path('search_result/<search_type>', views.search_result, name="search-result"),
]

