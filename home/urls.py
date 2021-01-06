"""Routes"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home as home_views

urlpatterns = [
    path('', home_views.home, name='home'),
    path('what-we-do', home_views.what_we_do, name='what_we_do'),
    path('research-and-reports', home_views.research_and_reports, name='research_and_reports'),
    path('stories', home_views.stories, name='stories'),
    path('take-action', home_views.take_action, name='take_action'),
    path('press-centre', home_views.press_centre, name='press_centre'),
    path('about-UNICEF', home_views.about_unicef, name='about_unicef'),
    path('where-we-work', home_views.where_we_work, name='where_we_work'),
    path('careers', home_views.careers, name='careers'),
    path('donate', home_views.donate, name='donate'),
    path('checkout', home_views.checkout, name='checkout'),
    path('send-email', home_views.send_email, name='send_email'),
    path('lang/<str:lang>', home_views.set_lang, name='set_lang'),
]