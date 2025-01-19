from django.urls import path
from . import views


urlpatterns = [
    path('cours/', views.CoursList.as_view(), name='Cours_list'),
    path('cours/<slug:slug>/', views.CoursView.as_view(), name='detail_cours'),
    path('Cours/create/', views.CoursCreateView.as_view(), name='cours_create'),
    path('convert/<slug:slug>/', views.convert_text_to_speech, name='convert_text_to_speech'),
    path('Cours/<slug:slug>/update/', views.CoursUpdateView.as_view(), name='cours_update'),
    path('Cours/<slug:slug>/delete/', views.CoursDeleteView.as_view(), name='cours_delete'),
    path('Exercice/', views.ExerciceList.as_view(), name='Exercice_list'),
    path('Exercice/create/', views.ExerciceCreateView.as_view(), name='exercice_create'),
    path('exercice/<slug:slug>/', views.ExerciceDetailView.as_view(), name='exercice_detail'),
    path('Exercice/<slug:slug>/update/', views.ExerciceUpdateView.as_view(), name='exercice_update'),
    path('Exercice/<slug:slug>/delete/', views.ExerciceDeleteView.as_view(), name='exercice_delete'),
    path('Solution/', views.SolutionList.as_view(), name='Solution_list'),
    path('Solution/create/', views.SolutionCreateView.as_view(), name='solution_create'),
    path('Solution/<slug:slug>/', views.SolutionView.as_view(), name='detail_solution'),
    path('Solution/<slug:slug>/update/', views.SolutionUpdateView.as_view(), name='solution_update'),
    path('Solution/<slug:slug>/delete/', views.SolutionDeleteView.as_view(), name='solution_delete'),
    path('status/create/<slug:slug>/', views.StatusCreateView.as_view(), name='status_create'),
    path('status/update/<slug:slug>/', views.StatusUpdateView.as_view(), name='status_update'),
    path('Status/<slug:exercice_slug>/',views.StatusView.as_view(), name='detail_status'),
    path('status/delete/<slug:slug>/', views.StatusDeleteView.as_view(), name='status_delete'),
]
