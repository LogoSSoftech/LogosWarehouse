from django.contrib import admin
from django.urls import path
from django.conf import settings
from apps.warehouse import views as warehouse_views
from apps.warehouse.models import Product
from apps.warehouse.models import StockLocation
from apps.warehouse.models import ProductUnit
from apps.warehouse.models import ProductPackage
from apps.warehouse.models import MeasurementUnit
from apps.warehouse.models import StockMove
from apps.warehouse.models import StockControl

urlpatterns = [

    #  -----------------------------REPORTS--------------------#

    path('ViewReport/', warehouse_views.ViewReport.as_view(
        extra_context={'heading': 'Reportes de Movimientos', 'title': 'Reportes'}), name='ViewReport'),

    #  -----------------------------PRODUCTS MODEL--------------------#
    path('ListProduct/', warehouse_views.ListProduct.as_view(
        extra_context={'heading': 'Productos', 'title': 'Productos'}, model=Product), name='ListProduct'),
    path('test/', warehouse_views.test, name='test'),
    path('DetailProduct/<int:pk>/', warehouse_views.DetailProduct.as_view(
        extra_context={'title': 'Detalle Producto'}, model=Product), name='DetailProduct'),
    path('CreateProduct/', warehouse_views.CreateProduct.as_view(
            extra_context={'heading': 'Creando Producto', 'title': 'Crear Producto'}, model=Product), name='CreateProduct'),
    path('EditProduct/<int:pk>/', warehouse_views.EditProduct.as_view(
        extra_context={'heading': 'Editando Producto', 'title': 'Editar Producto'}, model=Product), name='EditProduct'),
    path('DeleteProduct/<int:pk>/', warehouse_views.DeleteProduct.as_view(
        extra_context={'heading': 'Eliminar Producto', 'title': 'Eliminar Producto'}, model=Product), name='DeleteProduct'),

    #  ------------------------------------------PRODUCT UNIT MODEL--------------------------------------#
    path('ListProductUnit/', warehouse_views.ListProductUnit.as_view(
        extra_context={'heading': 'Unidades de Producto', 'title': 'Unidades de Producto'}, model=ProductUnit), name='ListProductUnit'),
    path('DetailProductUnit/<int:pk>/', warehouse_views.DetailProductUnit.as_view(
        extra_context={'title': 'Detalles'}, model=ProductUnit), name='DetailProductUnit'),
    path('CreateProductUnit/', warehouse_views.CreateProductUnit.as_view(
        extra_context={'heading': 'Creando Unidad', 'title': 'Crear Unidad'}, model=ProductUnit), name='CreateProductUnit'),
    path('EditProductUnit/<int:pk>/', warehouse_views.EditProductUnit.as_view(
        extra_context={'heading': 'Editando Unidad', 'title': 'Editar Unidad'}, model=ProductUnit), name='EditProductUnit'),
    path('DeleteProductUnit/<int:pk>/', warehouse_views.DeleteProductUnit.as_view(model=ProductUnit), name='DeleteProductUnit'),

    #  -----------------------------------------STOCK LOCATION MODEL--------------------------------#
    path('ListStockLocation/', warehouse_views.ListStockLocation.as_view(
        extra_context={'heading': 'Ubicaciones', 'title': 'Ubicaciones'}, model=StockLocation), name='ListStockLocation'),
    path('CreateStockLocation/', warehouse_views.CreateStockLocation.as_view(
        extra_context={'heading': 'Creado Ubicación', 'title': 'Crear Ubicación'}, model=StockLocation), name='CreateStockLocation'),
    path('EditStockLocation/<int:pk>/', warehouse_views.EditStockLocation.as_view(
        extra_context={'heading': 'Editando Ubicación', 'title': 'Editar Ubicación'}, model=StockLocation), name='EditStockLocation'),
    path('DeleteStockLocation/<int:pk>/', warehouse_views.DeleteStockLocation.as_view(
        model=StockLocation), name='DeleteStockLocation'),
    path('DetailStockLocation/<int:pk>/', warehouse_views.DetailStockLocation.as_view(
        extra_context={'title': 'Detalles'}, model=StockLocation), name='DetailStockLocation'),

    #  -------------------------------------PRODUCTS PACKAGE MODEL-----------------------------------------#
    path('ListProductPackage/', warehouse_views.ListProductPackage.as_view(
        extra_context={'heading': 'Paquetes', 'title': 'Paquetes de Productos'}, model=ProductPackage), name='ListProductPackage'),
    path('DetailProductPackage/<pk>/', warehouse_views.DetailProductPackage.as_view(
        extra_context={'heading': 'Detalle del Paquete', 'title': 'Detalle del Paquete'}, model=ProductPackage), name='DetailProductPackage'),
    path('CreateProductPackage/', warehouse_views.CreateProductPackage.as_view(
        extra_context={'heading': 'Creando Paquetes', 'title': 'Crear Paquete'}, model=ProductPackage), name='CreateProductPackage'),
    path('EditProductPackage/<int:pk>/', warehouse_views.EditProductPackage.as_view(
        extra_context={'heading': 'Editando Paquete', 'title': 'Editar Paquete'}, model=ProductPackage), name='EditProductPackage'),
    path('DeleteProductPackage/<int:pk>/', warehouse_views.DeleteProductPackage.as_view(
        model=ProductPackage), name='DeleteProductPackage'),
    path('create_unit_package/<int:pk>/', warehouse_views.create_unit_package, name='create_unit_package'),

    #  -------------------------------------MEASUREMENT UNITS MODEL-----------------------------------------#
    path('ListMeasurementUnit/', warehouse_views.ListMeasurementUnit.as_view(
        extra_context={'heading': 'Unidades de Medida', 'title': 'Unidades de Medida'}, model=MeasurementUnit), name='ListMeasurementUnit'),
    path('DetailMeasurementUnit/<pk>/', warehouse_views.DetailMeasurementUnit.as_view(
        extra_context={'heading': 'Detalle de la Unidad de Medida', 'title': 'Detalle de la Unidad de Medida'}, model=MeasurementUnit), name='DetailMeasurementUnit'),
    path('CreateMeasurementUnit/', warehouse_views.CreateMeasurementUnit.as_view(
        extra_context={'heading': 'Creando Unidad de Medida', 'title': 'Crear Unidad de Medida'}, model=MeasurementUnit), name='CreateMeasurementUnit'),
    path('EditMeasurementUnit/<int:pk>/', warehouse_views.EditMeasurementUnit.as_view(
        extra_context={'heading': 'Editando Unidad de Medida', 'title': 'Editar Unidad de Medida'}, model=MeasurementUnit), name='EditMeasurementUnit'),
    path('DeleteMeasurementUnit/<int:pk>/', warehouse_views.DeleteMeasurementUnit.as_view(model=MeasurementUnit), name='DeleteMeasurementUnit'),

    #  -------------------------------------STOCK MOVE MODEL-----------------------------------------#
    path('ListStockMove/', warehouse_views.ListStockMove.as_view(
        extra_context={'heading': 'Movimientos de Stock', 'title': 'Movimientos de Stock'}, model=StockMove), name='ListStockMove'),
    path('MoveUnit/', warehouse_views.MoveUnit.as_view(
        extra_context={'heading': 'Moviendo Unidad de Producto', 'title': 'Nuevo Movimiento'}, model=StockMove), name='MoveUnit'),
    path('MovePackage/', warehouse_views.MovePackage.as_view(
        extra_context={'heading': 'Moviendo Paquete', 'title': 'Nuevo Movimiento'}, model=StockMove), name='MovePackage'),
    path('DetailStockMove/<pk>', warehouse_views.DetailStockMove.as_view(
        extra_context={'title': 'Detalle Movimiento'}, model=StockMove), name='DetailStockMove'),

    #  -------------------------------------STOCK CONTROL MODEL-----------------------------------------#
    path('ListStockControl/', warehouse_views.ListStockControl.as_view(
        extra_context={'heading': 'Controles de Stock', 'title': 'Control de Stock'}, model=StockControl), name='ListStockControl'),
]
