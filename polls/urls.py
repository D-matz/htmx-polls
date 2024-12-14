from django.urls import path, include

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path('load_more_questions/<int:pagenum>/', views.load_more_questions, name='load_more_questions'),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/see_results/", views.see_results, name="see_results"),
    path('search/', views.search_polls, name='search_polls'),
]
