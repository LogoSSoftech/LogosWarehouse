from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Crum(models.Model):
    user_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='+',
        null=True, blank=True,
        verbose_name='Ultimo usuario en modificar')
    user_updater = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='+',
        null=True, blank=True,
        verbose_name='Ultimo usuario en modificar')
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,
        verbose_name='Fecha Creacion')
    date_updated = models.DateTimeField(
        auto_now=True, null=True, blank=True,
        verbose_name='Fecha Modificación')
    company_id = models.ForeignKey(
        settings.COMPANY_MODEL,
        on_delete=models.CASCADE, default=1,
        verbose_name='Compañía')

    class Meta:
        abstract = True


class User(AbstractUser, Crum):
    user_image = models.ImageField(
        upload_to='users', blank=True,
        null=True, verbose_name="Imagen de Perfil",
        default='default/default_avatar.png')


class CoreCompanies(models.Model):

    # RIF_TYPE
    j = 'J'
    v = 'V'
    e = 'E'

    RIF_TYPE = [
        (j, 'J'),
        (v, 'v'),
        (e, 'E'),

    ]

    # SOCIETY
    ca = 'C.A'
    sa = 'S.A'

    SOCIEDAD = [
        (ca, 'C.A'),
        (sa, 'S.A'),

    ]

    society = models.CharField(
        max_length=3,
        choices=SOCIEDAD,
        default=ca,
    )
    rif_type = models.CharField(
        max_length=1,
        choices=RIF_TYPE,
        default=j,
    )
    name = models.CharField(
        max_length=25,
        verbose_name='Razón Social')
    rif = models.CharField(
        max_length=12,
        verbose_name='RIF')
    company_image = models.ImageField(
        upload_to='company',
        verbose_name="Logotipo")
    email = models.EmailField(
        verbose_name="Email")
    web_site = models.URLField(
        verbose_name="Web Site",
        null=True, blank=True)
    phone1 = models.CharField(
        verbose_name="Telefono",
        max_length=15)
    phone2 = models.CharField(
        verbose_name="Telefono Adicional",
        null=True, blank=True,
        max_length=15)
    description = models.CharField(
        verbose_name="Descripción",
        null=True, blank=True,
        max_length=999)
    address = models.CharField(
        verbose_name="Direccion",
        null=True, blank=True,
        max_length=999)
    date = models.DateTimeField(
        default=datetime.now)

    class Meta:
        verbose_name = 'Compañia'
        db_table = 'core_companies'
        ordering = ['name']

    @receiver(post_save, sender='core.CoreCompanies')
    def set_rif(sender, instance, **kwargs):
        if kwargs.get('created'):
            rif = sender.objects.filter(id=instance.id).update(
                rif=instance.rif_type + '-' + str(instance.rif))

    def __str__(self):
        return str(self.name)

    def toJSON(self):
        item = model_to_dict(self)  # Se pueden excluir parámetros
        return item