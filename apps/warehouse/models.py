from datetime import datetime
from django.db import models
from crum import get_current_user
from core.models import Crum
from django.db.models.signals import post_save
from django.db.models.constraints import UniqueConstraint
from django.dispatch import receiver
from django.forms import model_to_dict
from apps.warehouse import settings


class MeasurementUnit(Crum):

    __AUTOCODE__ = 'MSRE'

    code = models.CharField(
        verbose_name="Código",
        max_length=100, unique=True)
    name = models.CharField(
        max_length=30,
        verbose_name="Nombre", unique=True)
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Descripción")
    abbreviation = models.CharField(
        verbose_name="Abbreviación",
        max_length=5, unique=True)

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'
        db_table = 'measurement_unit'
        ordering = ['code']
        UniqueConstraint(
            fields=['code', 'abbreviation'], name='unique_measure')

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creator = user
            else:
                self.user_updater = user
        super(MeasurementUnit, self).save()

    @receiver(post_save, sender='warehouse.MeasurementUnit')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item


class Product(Crum):

    __AUTOCODE__ = 'PRD'

    article = 'article'
    consumable = 'consumable'
    service = 'service'

    TYPE_CHOICES = [
        (article, 'Articulo'),
        (consumable, 'Consumible'),
        (service, 'Servicio'),
    ]

    product_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=article,
        verbose_name="Tipo de Producto"
    )

    article_qty = models.PositiveIntegerField(
        verbose_name="Cantidad por Artículo",
        blank=True, null=True)
    code = models.CharField(
        verbose_name="Código",
        max_length=100,
        unique=True)
    name = models.CharField(
        max_length=30, verbose_name="Nombre",
        unique=True)
    active = models.BooleanField(
        default=True, verbose_name="Activo")
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Descripción")
    measure_id = models.ForeignKey(
        MeasurementUnit,
        verbose_name="Unidad de Medida",
        on_delete=models.CASCADE, blank=True,
        null=True)
    product_image = models.ImageField(
        upload_to='product', blank=True,
        null=True, verbose_name="Imagen de Producto",
        default='default/default_product.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'product'
        ordering = ['code']

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creator = user
            else:
                self.user_updater = user
        super(Product, self).save()

    @receiver(post_save, sender='warehouse.Product')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))

    def __str__(self):
        return str(self.code + ' ' + self.name)

    def toJSON(self):
        item = model_to_dict(self)
        return item


class StockLocation(Crum):

    __AUTOCODE__ = 'STCKLO'

    ingress = 'Ingress'
    egress = 'Egress'
    internal = 'Internal'
    null = 'Null'

    TYPE_CHOICES = [
        (null, 'Null'),
        (ingress, 'Ingress'),
        (egress, 'Egress'),
        (internal, 'Internal'),
    ]
    location_type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=null,
    )
    code = models.CharField(
        verbose_name="Código",
        max_length=100, unique=True)
    name = models.CharField(
        max_length=30, unique=True,
        verbose_name="Nombre")
    active = models.BooleanField(
        default=True, verbose_name="Activo")
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Descripción")
    date_created = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Creación")
    date_modify = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        db_table = 'stock_location'
        ordering = ['name']

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creator = user
            else:
                self.user_updater = user
        super(StockLocation, self).save()

    @receiver(post_save, sender='warehouse.StockLocation')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))

    def __str__(self):
        return str(self.name)

    def toJSON(self):
        item = model_to_dict(self)
        return item


class ProductPackage(Crum):

    __AUTOCODE__ = 'PCKG'

    code = models.CharField(
        verbose_name="Código",
        max_length=100)
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Descripción")
    pieces = models.PositiveIntegerField(
        verbose_name="Piezas", default=0.0)
    unit_ids = models.ManyToOneRel(
        settings.PRODUCT_UNIT_MODEL,
        on_delete=models.PROTECT,
        field_name='unit_ids',
        to='package_id',
        )
    units_created = models.BooleanField(
        default=False)
    unit_qty = models.FloatField(
        verbose_name="Cantidad por Unidad",
        default=0.0)
    product_id = models.ForeignKey(
        Product, verbose_name="Producto",
        on_delete=models.CASCADE)
    location_id = models.ForeignKey(
        StockLocation,
        verbose_name="Ubicación", null=True, blank=True,
        on_delete=models.CASCADE)
    fixed_ammount = models.BooleanField(
        verbose_name="Fijar Cantidad",
        default=False)
    first_move = models.BooleanField(
        verbose_name="Primer Movimiento",
        default=False)

    class Meta:
        verbose_name = 'Paquete de Productos'
        verbose_name_plural = 'Paquetes de Productos'
        db_table = 'product_package'
        ordering = ['code']

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creator = user
            else:
                self.user_updater = user
        super(ProductPackage, self).save()

    @receiver(post_save, sender='warehouse.ProductPackage')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))

    @receiver(post_save, sender='warehouse.ProductPackage')
    def get_created_id(sender, instance, **kwargs):
        instance = instance.id
        return instance

    def __str__(self):
        if self.location_id:
            name_location = str(self.location_id.name)
        else:
            name_location = ''
        return str(self.code + ' ' + name_location)

    def toJSON(self):
        item = model_to_dict(self)
        return item


class ProductUnit(Crum):

    __AUTOCODE__ = 'PRDUNT'

    code = models.CharField(
        verbose_name="Código", max_length=100,
        unique=True)
    name = models.CharField(
        max_length=100, verbose_name="Nombre")
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Descripción")
    quantity = models.FloatField(
        verbose_name="Cantidad",
        default=0.0)
    pieces = models.PositiveIntegerField(
        verbose_name="Piezas", default=0.0)
    product_id = models.ForeignKey(
        Product, verbose_name="Producto",
        on_delete=models.CASCADE)
    measure = models.CharField(
        verbose_name="Medida", max_length=30,
        blank=True, null=True)
    package_id = models.ForeignKey(
        ProductPackage,
        null=True, blank=True, verbose_name="Paquete",
        on_delete=models.CASCADE)
    location_id = models.ForeignKey(
        StockLocation,
        verbose_name="Ubicación", null=True,
        blank=True, on_delete=models.CASCADE)
    stock_ctrl = models.BooleanField(
        default=False)
    fixed_ammount = models.BooleanField(
        verbose_name="Fijar Cantidad", default=False)
    first_move = models.BooleanField(
        verbose_name="Primer Movimiento", default=False)

    class Meta:
        verbose_name = 'Unidad de Producto'
        verbose_name_plural = 'Unidades de Producto'
        db_table = 'product_unit'
        ordering = ['code']

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creator = user
            else:
                self.user_updater = user
        super(ProductUnit, self).save()

    @receiver(post_save, sender='warehouse.ProductUnit')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            autocode = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id),
                )

    def __str__(self):
        return str(
            self.name
            + ' ' + self.code + ' ' + str(self.quantity) + ' '
            + (self.product_id.measure_id.abbreviation if
                self.product_id.measure_id else ' '))

    def toJSON(self):
        item = model_to_dict(self)
        return item


class StockMove(Crum):

    __AUTOCODE__ = 'MOVE'

    code = models.CharField(
        verbose_name="Código", max_length=100,
        unique=True)
    note = models.TextField(
        verbose_name="Notas")
    description = models.TextField(
        verbose_name="Descripción")
    pieces = models.IntegerField(
        verbose_name="Piezas",
        default=0)
    quantity = models.FloatField(
        verbose_name="Cantidad",
        default=0.0)
    prev_qty = models.FloatField(
        verbose_name="Cantidad previa de la Unidad",
        default=0.0)
    balance = models.FloatField(
        verbose_name="Saldo total de la Unidad",
        default=0.0)
    prev_qty_origin = models.FloatField(
        null=True, blank=True,
        verbose_name="Cantidad previa en el origen",
        default=0.0)
    balance_origin = models.FloatField(
        null=True, blank=True,
        verbose_name="Saldo nuevo en el origen",
        default=0.0)
    prev_qty_dest = models.FloatField(
        null=True, blank=True,
        verbose_name="Cantidad previa en el Destino",
        default=0.0)
    balance_dest = models.FloatField(
        null=True, blank=True,
        verbose_name="Saldo nuevo en el Destino",
        default=0.0)
    unit_id = models.ForeignKey(
        ProductUnit, null=True, blank=True,
        verbose_name="Unidad de Producto",
        on_delete=models.CASCADE)
    package_id = models.ForeignKey(
        ProductPackage, null=True, blank=True,
        verbose_name="Paquetes", on_delete=models.CASCADE)
    location_id = models.ForeignKey(
        StockLocation, on_delete=models.CASCADE,
        verbose_name="Origen")
    location_dest_id = models.ForeignKey(
        StockLocation, on_delete=models.CASCADE,
        related_name='+', verbose_name="Destino")
    date = models.DateTimeField(
        verbose_name="Fecha", default=datetime.now)
    move_type = models.CharField(
        verbose_name="Tipo de Movimiento", max_length=100)

    class Meta:
        verbose_name = 'Movimiento de Stock'
        verbose_name_plural = 'Movimientos de Stock'
        db_table = 'stock_move'
        ordering = ['code']

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creator = user
            else:
                self.user_updater = user
        super(StockMove, self).save()

    @receiver(post_save, sender='warehouse.StockMove')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))

    def __str__(self):
        return self.code

    def toJSON(self):
        item = model_to_dict(self)
        return item


class StockControl(Crum):

    __AUTOCODE__ = 'STKCTRL'

    code = models.CharField(
        verbose_name="Codigo", max_length=100,
        unique=True)
    pieces = models.IntegerField(
        verbose_name="Piezas", default=0.0)
    quantity = models.FloatField(
        verbose_name="Cantidad",
        default=0.0)
    unit_id = models.ForeignKey(
        ProductUnit, null=True, blank=True,
        verbose_name="Unidad de Producto",
        on_delete=models.CASCADE, default=0.0)
    unit_id = models.ForeignKey(
        ProductUnit, null=True, blank=True,
        verbose_name="Unidad de Producto",
        on_delete=models.CASCADE)
    location_id = models.ForeignKey(
        StockLocation, on_delete=models.CASCADE)
    date = models.DateField(
        verbose_name="Fecha", auto_now_add=True)

    class Meta:
        verbose_name = 'Control de Stock'
        verbose_name_plural = 'Controles de Stock'
        db_table = 'stock_control'
        ordering = ['code']

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creator = user
            else:
                self.user_updater = user
        super(StockControl, self).save()

    @receiver(post_save, sender='warehouse.StockControl')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))

    def __str__(self):
        return self.code

    def toJSON(self):
        item = model_to_dict(self)
        return item
