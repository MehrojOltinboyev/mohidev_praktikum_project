from django.urls import path
from .views import (news_list,news_detail,homePageView,ContactPageView,turtyuzturtPageView,aboutPageView,HomePageView,LocalNewsPage,ForeignNewsView,SportNewsView,TechnologyNewsView)

urlpatterns = [
    path("",HomePageView.as_view(),name="home_page"),
    path('news/', news_list, name="all_news_list"),
    path('news/<slug:news>/',news_detail, name='news_detail_page'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('turtyuzturt-page/',turtyuzturtPageView,name='turtyuzturt_page'),
    path('about-page/',aboutPageView,name='about-page'),
    path("local/",LocalNewsPage.as_view(),name="local_news_page"),
    path("forein/",ForeignNewsView.as_view(),name="foreign_news_page"),
    path("technology/",TechnologyNewsView.as_view(),name="technology_news_page"),
    path("sport/",SportNewsView.as_view(),name="sport_news_page"),
]