from django.conf.urls import url
from call_data import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^params/$', views.get_params, name='get_params'),
]
