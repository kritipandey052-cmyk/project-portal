from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('materials/issue/', views.material_issue, name='material_issue'),
    path('materials/consume/', views.material_consume, name='material_consume'),
    path('dpr/', views.dpr, name='dpr'),
    path('expenses/', views.expenses, name='expenses'),
    path('reports/', views.reports, name='reports'),
    path('reports/export/excel/', views.export_excel, name='export_excel'),
    path('reports/export/pdf/', views.export_pdf, name='export_pdf'),
]
