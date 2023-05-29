
import token
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Empresa, Equipo, Control
from .forms import EmpresaForm
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.models import User
from django.views.generic.edit import FormView







class InicioView(View):
    @method_decorator(login_required)
    def get(self, request):
        empresas = Empresa.objects.all()
        equipo_id = 1
        return render(request, 'preventivos/inicio.html', {'empresas': empresas, 'equipo_id': equipo_id})


class DetalleEquipoView(View):
    @method_decorator(login_required)
    def get(self, request, equipo_id):
        equipo = Equipo.objects.get(id=equipo_id)
        controles = Control.objects.filter(equipo=equipo)
        return render(request, 'preventivos/detalle_equipo.html', {'equipo': equipo, 'controles': controles})

class CrearControlView(View):
    @method_decorator(login_required)
    def get(self, request, equipo_id):
        equipo = Equipo.objects.get(id=equipo_id)
        return render(request, 'preventivos/crear_control.html', {'equipo_id': equipo_id})

    @method_decorator(login_required)
    def post(self, request, equipo_id):
        fecha = request.POST['fecha']
        realizado_por = request.user
        observaciones = request.POST['observaciones']
        equipo = Equipo.objects.get(id=equipo_id)

        control = Control.objects.create(equipo=equipo, fecha=fecha, realizado_por=realizado_por, observaciones=observaciones)
        control.save()

        return redirect('preventivos:detalle_equipo', equipo_id=equipo_id)

class RegistroUsuarioView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'preventivos/registro.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('preventivos:inicio')
        return render(request, 'preventivos/registro.html', {'form': form})

class IniciarSesionView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'preventivos/iniciar_sesion.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('preventivos:inicio')
        return render(request, 'preventivos/iniciar_sesion.html', {'form': form})

    
class CerrarSesionView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('preventivos:inicio')

    @method_decorator(login_required)
    def post(self, request):
        logout(request)
        return redirect('preventivos:inicio')

class CrearEmpresaView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = EmpresaForm()
        return render(request, 'preventivos/crear_empresa.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('preventivos:inicio')
        return render(request, 'preventivos/crear_empresa.html', {'form': form})


class ConfigurarPerfilView(View):
    def get(self, request):
        
        return render(request, 'preventivos/configurar_perfil.html')





class EnviarCorreoView(View):
    def get(self, request):
        

        email = request.GET.get('email', '')  # Obtener el correo electrónico del formulario

        if email:
            user = get_object_or_404(User, email=email)  # Buscar el usuario por su correo electrónico

            token = default_token_generator.make_token(user)

            subject = 'Restablecer contraseña'
            message = f'Aquí está el enlace para restablecer tu contraseña: {token}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return render(request, 'preventivos/confirmacion.html')

        

        return render(request, 'preventivos/confirmacion.html')   





class RestablecerContraseñaView(FormView):
    template_name = 'preventivos/restablecer_contraseña.html'
    success_url = reverse_lazy('preventivos:contraseña_restablecida')
    def get_form(self, form_class=None):
        # Implementa la lógica para crear una instancia del formulario de restablecimiento de contraseña
        # Puedes utilizar el formulario predeterminado de Django o personalizarlo según tus necesidades
        return super().get_form(form_class)

    def form_valid(self, form):
        # Implementa la lógica para procesar el formulario cuando sea válido
        # Aquí puedes realizar las operaciones para restablecer la contraseña del usuario
        return super().form_valid(form)

    def get_user(self, uidb64):
        # Lógica para obtener el usuario a partir del uidb64
        return get_object_or_404(User, pk=uidb64)

    def get_token(self, uidb64):
        # Lógica para obtener el token a partir del uidb64
        return get_object_or_404(token, user_id=uidb64)

    def token_valid(self, user, token):
        # Lógica para validar si el token es válido para el usuario
        return default_token_generator.check_token(user, token)
    def post(self, request, uidb64=None, token=None, **kwargs):
        # Lógica para procesar el restablecimiento de contraseña
        user = self.get_user(uidb64)
        reset_token = self.get_token(uidb64)

        if user is not None and reset_token is not None and self.token_valid(user, reset_token):
            # El token es válido, permite al usuario restablecer la contraseña
            # Implementa tu lógica aquí para actualizar la contraseña del usuario
            # Puedes utilizar el método set_password del modelo User

            # Redirige a la página de éxito
            return self.form_valid(request, self.get_form())

        # El token no es válido, muestra un mensaje de error o redirige a una página de error
        # Implementa tu lógica aquí según tus necesidades

        return self.form_invalid(self.get_form())
