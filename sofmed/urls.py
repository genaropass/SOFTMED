"""
URL configuration for sofmed project.
"""
from django.contrib import admin
from django.urls import path
from clinica import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('login-medico/', views.login_medico, name='login_medico'),
    path('logout-medico/', views.logout_medico, name='logout_medico'),
    path('registro-pacientes/', views.registro_pacientes, name='registro_pacientes'),
    path('agregar-paciente/', views.agregar_paciente, name='agregar_paciente'),
    path('paciente/<int:paciente_id>/', views.ver_paciente, name='ver_paciente'),
    path('paciente/<int:paciente_id>/agregar-historial/', views.agregar_historial, name='agregar_historial'),
    path('paciente/<int:paciente_id>/eliminar/', views.eliminar_paciente_view, name='eliminar_paciente'),
    path('listar-pacientes/', views.listar_pacientes, name='listar_pacientes'),
]

