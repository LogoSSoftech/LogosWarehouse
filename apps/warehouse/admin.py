from django.contrib import admin
from apps.warehouse.models import StockMove
from apps.warehouse.models import StockControl
from apps.warehouse.models import Product
from apps.warehouse.models import StockLocation
from apps.warehouse.models import ProductUnit
from apps.warehouse.models import ProductPackage
from apps.warehouse.models import MeasurementUnit


class ProductModel(admin.ModelAdmin):

    list_display = ("code", "name", "active", "description", "id")
    search_fields = ("code", "name", "active")
    list_filter = ("code", "name", "active")


class ProductPackageModel(admin.ModelAdmin):

    list_display = ("code", "product_id", "pieces", "unit_qty", "location_id", "description", "id")
    search_fields = ("code", "product_id", "pieces", "unit_qty", "location_id")
    list_filter = ("code", "product_id", "pieces", "unit_qty", "location_id")


class ProductUnitModel(admin.ModelAdmin):

    list_display = ("code", "name", "description", "quantity", "product_id", "id")
    search_fields = ("code", "name", "pieces", "quantity", "product_id")
    list_filter = ("code", "name", "pieces", "quantity", "product_id")


class StockLocationModel(admin.ModelAdmin):
    list_display = ("code", "name", "location_type", "active", "description", "id")
    search_fields = ("code", "name", "location_type", "active")
    list_filter = ("code", "name", "location_type", "active")


class MeasurementUnitModel(admin.ModelAdmin):
    list_display = ("code", "name", "description", "id")
    search_fields = ("code", "name")
    list_filter = ("code", "name")


class StockMoveModel(admin.ModelAdmin):

    list_display = ("code", "note", "package_id", "unit_id",
                    "pieces", "quantity", "location_id", "location_dest_id", "description", "id")
    search_fields = ("code", "package_id", "unit_id", "location_id", "location_dest_id", "quantity", "pieces")
    list_filter = ("code", "package_id", "unit_id", "location_id", "location_dest_id", "quantity", "pieces")


class StockControlModel(admin.ModelAdmin):

    list_display = ("code", "unit_id", "pieces", "quantity", "location_id", "id")
    search_fields = ("code", "unit_id", "pieces", "quantity", "location_id")
    list_filter = ("code", "unit_id", "pieces", "quantity", "location_id")


admin.site.register(Product, ProductModel)
admin.site.register(ProductPackage, ProductPackageModel)
admin.site.register(ProductUnit, ProductUnitModel)
admin.site.register(StockLocation, StockLocationModel)
admin.site.register(MeasurementUnit, MeasurementUnitModel)
admin.site.register(StockMove, StockMoveModel)
admin.site.register(StockControl, StockControlModel)