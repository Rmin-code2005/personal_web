from django.urls import path
from .views import (
    ProfileView, EducationListView, SkillListView,
    ProjectListView, ContactCreateView, CategoryListView,
)

urlpatterns = [
    path('profile/', ProfileView.as_view()),
    path('projects/', ProjectListView.as_view()),
    path('skills/', SkillListView.as_view()),
    path('education/', EducationListView.as_view()),
    path('contact/', ContactCreateView.as_view()),
    path('categories/', CategoryListView.as_view()),
]