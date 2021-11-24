from core.models import User
from django.shortcuts import redirect
import sweetify
from django.conf import settings
from django.core.mail import send_mail
from random import choice


def restore_password(request):
    errors = None
    username = request.POST.get('username', '')
    get_user = User.objects.filter(username=username)
    if get_user:
        for user in get_user:
            email = user.email
            name = user.first_name + ' ' + user.last_name
            user_name = user.username
            company = user.company_id.name + ' ' + user.company_id.society

            # Generando Contraseña
            password = ''
            get_user_id = User.objects.get(username=username)
            values = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-_*."
            large = 7
            password = password.join([choice(values) for i in range(large)])
            get_user_id.set_password(password)
            get_user_id.save()

        #  Datos y envío del Correo
        subject = \
            'LogosERP: Cambio de contraseña para su cuenta %s en %s' \
            % (user_name, company)
        message = \
            '''
            Saludos %s.
            Conforme a su solicitud, su contraseña nueva será:

            %s

            Una vez ingrese al sistema podrá cambiarla en su perfil de usuario.
            Un abrazo.
            ''' % (name, password)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)

        msg = 'Hola %s, se ha enviado un correo a %s con su nueva contraseña' \
              % (name, email)
        sweetify.error(request, msg, button='Chevere!', timer=15000)
        return True
    else:
        msg = 'No existe este usuario, por favor revise e intente nuevamente'
        sweetify.error(request, msg)
        return False
