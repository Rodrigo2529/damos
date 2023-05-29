from django import views
from django.urls import path
from .views import (
    InicioView,
    DetalleEquipoView,
    CrearControlView,
    RegistroUsuarioView,
    IniciarSesionView,
    CerrarSesionView,
    CrearEmpresaView,
    ConfigurarPerfilView,
    CrearControlView, 
    EnviarCorreoView,
    RestablecerContraseñaView,
)

app_name = 'preventivos'

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),
    path('equipo/<int:equipo_id>/', DetalleEquipoView.as_view(), name='detalle_equipo'),
    path('equipo/<int:equipo_id>/crear-control/', CrearControlView.as_view(), name='crear_control'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('iniciar-sesion/', IniciarSesionView.as_view(), name='iniciar_sesion'),
    path('cerrar-sesion/', CerrarSesionView.as_view(), name='cerrar_sesion'),
    path('crear-empresa/', CrearEmpresaView.as_view(), name='crear_empresa'),
    path('configurar-perfil/', ConfigurarPerfilView.as_view(), name='configurar_perfil'),
    path('enviar-correo/', EnviarCorreoView.as_view(), name='enviar_correo'),
    path('restablecer-contraseña/<str:uidb64>/<str:token>/', RestablecerContraseñaView.as_view(), name='restablecer_contraseña'),

]