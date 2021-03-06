from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'cardadmin', views.admin, name='cardadmin'),
    url(r'learn', views.learn, name='learn'),
    url(r'answer/(?P<card_id>.*)/(?P<result>.*)', views.answer, name='answer'),
    url(r'', views.index, name='index'),
]
