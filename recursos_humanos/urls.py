from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('descargar_pdf/<str:d>', views.descargar_pdf, name='descargar_pdf'),

]