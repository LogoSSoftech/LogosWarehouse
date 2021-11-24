from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import sweetify
from datetime import datetime
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic import DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from apps.warehouse import validations
from apps.warehouse import functions
from apps.warehouse import reports
from apps.warehouse.admin import StockMoveModel
from apps.warehouse.models import Product
from apps.warehouse.models import StockLocation
from apps.warehouse.models import ProductUnit
from apps.warehouse.models import ProductPackage
from apps.warehouse.models import MeasurementUnit
from apps.warehouse.models import StockMove
from apps.warehouse.models import StockControl
from apps.warehouse.forms import ProductForm
from apps.warehouse.forms import StockLocationForm
from apps.warehouse.forms import ProductUnitForm
from apps.warehouse.forms import ProductPackageForm
from apps.warehouse.forms import MeasurementUnitForm
from apps.warehouse.forms import MovePackageForm
from apps.warehouse.forms import MoveUnitForm
from apps.warehouse.forms import ReportForm

def test(request):
    return redirect('/')


# ---------------------------------REPORTS----------------------------#
class ViewReport(LoginRequiredMixin, TemplateView):

    template_name = 'reports/views/ViewReport.html'
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_moves_year_month(self):
        moves_qty = []
        try:
            year = datetime.now().year
            for month in range(1, 13):
                moves = StockMove.objects.filter(
                    date__year=year, date__month=month)
                moves_qty.append(len(moves))
        except:
            pass
        return moves_qty

    def get_context_data(self, **kwargs):
        total_year_moves = 0
        for item in self.get_moves_year_month():
            total_year_moves += item
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['by_move'] = 'Reporte de Movimientos'
        context['by_product'] = 'Reporte Movimientos por Producto'
        context['by_location'] = 'Reporte Movimientos por Ubicación'
        context['by_user'] = 'Reporte Movimientos por Usuario'
        context['year'] = datetime.now().year
        context['moves_year_month'] = self.get_moves_year_month()
        context['total_year_moves'] = total_year_moves

        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                data = reports.report_move(request)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

# -------------------------------PRODUCTS MODEL-----------------------#

# ------------------------VIEWS------------------------------#


class ListProduct(LoginRequiredMixin, ListView):

    model = Product
    create_form = ProductForm
    template_name = 'products/views/ListProduct.html'
    success_url = reverse_lazy('ListProduct')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nuevo Producto'
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateProduct'),
                      'text': 'Crear Nuevo Producto'},
        }
        context['create_forms'] = create_forms
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailProduct(LoginRequiredMixin, DetailView):
    model = ProductUnit
    template_name = 'products/views/DetailProduct.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        unit_ids = ProductUnit.objects.filter(product_id=product_id)
        package_ids = ProductPackage.objects.filter(product_id=product_id)
        heading = 'Detalle %s %s' % (product_id.code, product_id.name)
        context['heading'] = heading
        context['unit_lines'] = 'Unidades Asociadas'
        context['pckg_lines'] = 'Paquetes Asociados'
        if unit_ids:
            context['unit_ids'] = unit_ids
        if package_ids:
            context['package_ids'] = package_ids
        return context
# ------------------------FUNCTIONS------------------------------#


class CreateProduct(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/functions/CreateProduct.html'
    success_url = reverse_lazy('ListProduct')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditProduct(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/functions/CreateProduct.html'
    success_url = reverse_lazy('ListProduct')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DeleteProduct(LoginRequiredMixin, DeleteView):
    model = Product
    form_class = ProductForm
    template_name = 'products/functions/DeleteProduct.html'
    success_url = reverse_lazy('ListProduct')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# --------------------PRODUCT UNIT MODEL----------------------------#

# ------------------------VIEWS------------------------------#


class ListProductUnit(LoginRequiredMixin, ListView):

    model = ProductUnit
    template_name = 'product_units/views/ListProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateProductUnit'),
                      'text': 'Crear Nueva Unidad'},
        }
        create_pckg = {
            'pckg': {'button_pckg': '',
                     'text': 'Crear Paquetes'},
        }
        context['create_forms'] = create_forms
        context['create_pckg'] = create_pckg
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'datatable':
                data = []
                for unit_id in ProductUnit.objects.all():
                    data.append(unit_id.toJSON())
            if action == 'validate':
                unit_ids = request.POST.getlist('unit_ids[]')
                print(unit_ids)
                try:
                    ProductPackage.objects.create(
                        product_id_id=1,
                        location_id_id=1,
                        unit_ids=unit_ids
                    )#.get_created_id()
                    # print(package_id)
                except Exception as e:
                    print(str(e))
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class DetailProductUnit(LoginRequiredMixin, DetailView):
    model = ProductUnit
    template_name = 'product_units/views/DetailProductUnit.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unit_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        move_ids = StockMove.objects.filter(unit_id=unit_id)
        heading = 'Detalle %s %s' % (unit_id.code, unit_id.name)
        context['heading'] = heading
        context['move_heading'] = 'Movimientos'
        context['item_type'] = 'Unit'
        if move_ids:
            context['move_ids'] = move_ids
        if unit_id.package_id:
            move_pckg_ids = StockMove.objects.filter(
                package_id=unit_id.package_id.id)
            if move_pckg_ids:
                context['move_pckg_ids'] = move_pckg_ids
                context['pckg_moves'] = 'Movimientos del Paquete'
        return context


# ------------------------FUNCTIONS------------------------------#

class CreateProductUnit(LoginRequiredMixin, CreateView):
    model = ProductUnit
    addform = ProductForm
    form_class = ProductUnitForm
    template_name = 'product_units/functions/CreateProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                unit_id = form.save(commit=False)
                if unit_id.product_id.product_type == 'article':
                    unit_id.fixed_ammount = True
                unit_id.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditProductUnit(LoginRequiredMixin, UpdateView):
    model = ProductUnit
    form_class = ProductUnitForm
    template_name = 'product_units/functions/CreateProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DeleteProductUnit(LoginRequiredMixin, DeleteView):
    model = ProductUnit
    form_class = ProductUnitForm
    template_name = 'product_units/functions/DeleteProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# --------------------STOCK LOCATION MODEL--------------------------#

# ------------------------VIEWS------------------------------#


class ListStockLocation(LoginRequiredMixin, ListView):

    model = StockLocation
    template_name = 'stock_location/views/ListStockLocation.html'
    create_form = StockLocationForm
    success_url = reverse_lazy('ListStockLocation')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nueva Ubicación'
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateStockLocation'),
                      'text': 'Crear Nueva Ubicación'},
        }
        context['create_forms'] = create_forms
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailStockLocation(LoginRequiredMixin, DetailView):
    model = StockLocation
    template_name = 'stock_location/views/DetailStockLocation.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        stkctrl_ids = StockControl.objects.filter(location_id=location_id)
        pckg_ids = ProductPackage.objects.filter(location_id=location_id)
        move_ids = StockMove.objects.filter(location_dest_id=location_id)
        heading = 'Detalle %s %s' % (location_id.name, location_id.code)
        context['heading'] = heading
        context['controls_lines'] = 'Stock en esta ubicación'
        context['pckg_lines'] = 'Paquetes en esta ubicación'
        context['move_heading'] = 'Movimientos'
        if stkctrl_ids:
            context['stkctrl_ids'] = stkctrl_ids
        if pckg_ids:
            context['pckg_ids'] = pckg_ids
        if move_ids:
            context['move_ids'] = move_ids
        return context
# ------------------------FUNCTIONS------------------------------#


class CreateStockLocation(LoginRequiredMixin, CreateView):
    model = StockLocation
    form_class = StockLocationForm
    template_name = 'stock_location/functions/CreateStockLocation.html'
    success_url = reverse_lazy('ListStockLocation')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditStockLocation(LoginRequiredMixin, UpdateView):

    model = StockLocation
    form_class = StockLocationForm
    template_name = 'stock_location/functions/CreateStockLocation.html'
    success_url = reverse_lazy('ListStockLocation')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DeleteStockLocation(LoginRequiredMixin, DeleteView):
    model = StockLocation
    form_class = StockLocationForm
    template_name = 'stock_location/functions/DeleteStockLocation.html'
    success_url = reverse_lazy('ListStockLocation')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# -----------------------PRODUCT PACKAGE MODEL-----------------------#

# ------------------------VIEWS------------------------------#
class ListProductPackage(LoginRequiredMixin, ListView):

    model = ProductPackage
    template_name = 'products_package/views/ListProductPackage.html'
    create_form = ProductPackageForm
    success_url = reverse_lazy('ListProductPackage')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nuevo Paquete'
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateProductPackage'),
                      'text': 'Crear Nuevo Paquete'},
        }
        context['create_forms'] = create_forms
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailProductPackage(LoginRequiredMixin, DetailView):
    model = ProductPackage
    template_name = 'products_package/views/DetailProductPackage.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        move_ids = StockMove.objects.filter(package_id=package_id.id)
        unit_ids = ProductUnit.objects.filter(package_id=package_id.id)

        heading = 'Detalle %s %s' % \
            (package_id.code, package_id.product_id.name)
        context['heading'] = heading
        context['move_heading'] = 'Movimientos'
        context['lines_heading'] = 'Unidades del Paquete'
        context['item_type'] = 'Package'
        if move_ids:
            context['move_ids'] = move_ids
            context['unit_ids'] = unit_ids
        return context


# ------------------------FUNCTIONS------------------------------#

class CreateProductPackage(LoginRequiredMixin, CreateView):
    model = ProductPackage
    form_class = ProductPackageForm
    template_name = 'products_package/functions/CreateProductPackage.html'
    success_url = reverse_lazy('ListProductPackage')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditProductPackage(LoginRequiredMixin, UpdateView):
    model = ProductPackage
    form_class = ProductPackageForm
    template_name = 'products_package/functions/CreateProductPackage.html'
    success_url = reverse_lazy('ListProductPackage')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DeleteProductPackage(LoginRequiredMixin, DeleteView):
    model = ProductPackage
    form_class = ProductPackageForm
    template_name = 'products_package/functions/DeleteProductPackage.html'
    success_url = reverse_lazy('ListProductPackage')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def create_unit_package(request, pk):
    '''
    Crea las unidades de productos del paquete

    '''
    pckg = ProductPackage.objects.get(id=pk)
    if functions.create_unit_package(request, pckg):
        if functions.create_pckg_stock_control(request, pckg):
            return redirect('ListProductPackage')
    else:
        sweetify.error(request, 'Error en la creación del Control de Stock')
    return redirect('ListProductPackage')


# ------------------MEASUREMENTS UNITS-----------------------------#

# ------------------------VIEWS------------------------------#
class ListMeasurementUnit(LoginRequiredMixin, ListView):

    model = MeasurementUnit
    template_name = 'measurement_units/views/ListMeasurementUnit.html'
    create_form = MeasurementUnitForm
    success_url = reverse_lazy('ListMeasurementUnit')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateMeasurementUnit'),
                      'text': 'Crear nueva Medida'},
        }
        context['create_forms'] = create_forms
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailMeasurementUnit(DetailView):
    model = MeasurementUnit
    template_name = 'measurement_units/views/DetailMeasurementUnit.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        measure_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        product_ids = Product.objects.filter(measure_id=measure_id)
        heading = 'Detalle %s' % measure_id.name
        context['heading'] = heading
        context['product_lines'] = 'Productos Asociados'
        if product_ids:
            context['product_ids'] = product_ids
        return context

        return context

# ----------------------------FUNCTIONS------------------------------#


class CreateMeasurementUnit(LoginRequiredMixin, CreateView):
    model = MeasurementUnit
    form_class = MeasurementUnitForm
    template_name = 'measurement_units/functions/CreateMeasurementUnit.html'
    success_url = reverse_lazy('ListMeasurementUnit')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditMeasurementUnit(LoginRequiredMixin, UpdateView):
    model = MeasurementUnit
    form_class = MeasurementUnitForm
    template_name = 'measurement_units/functions/CreateMeasurementUnit.html'
    success_url = reverse_lazy('ListMeasurementUnit')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DeleteMeasurementUnit(LoginRequiredMixin, DeleteView):
    model = MeasurementUnit
    form_class = MeasurementUnitForm
    template_name = 'measurement_units/functions/DeleteMeasurementUnit.html'
    success_url = reverse_lazy('ListMeasurementUnit')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# ----------------------STOCK MOVE MODEL----------------------------#
# --------------------------VIEWS-----------------------------------#


class ListStockMove(LoginRequiredMixin, ListView):
    model = StockMove
    template_name = 'stock_move/views/ListStockMove.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        create_forms = {
            'form1': {'button_create': reverse_lazy('MoveUnit'),
                      'text': 'Mover Unidad'},
            'form2': {'button_create': reverse_lazy('MovePackage'),
                      'text': 'Mover Paquete'},
        }
        context['create_forms'] = create_forms
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = StockMove.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DetailStockMove(LoginRequiredMixin, DetailView):
    model = StockMove
    template_name = 'stock_move/views/DetailStockMove.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # locale.setlocale(locale.LC_ALL, 'es-ES')
        context = super().get_context_data(**kwargs)
        move_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        heading = 'Detalle %s %s -> %s' \
            % (move_id.code, move_id.location_id,
               move_id.location_dest_id)
        context['heading'] = heading
        return context


# ----------------------------------------FUNCTIONS----------------------------------------#


class MoveUnit(LoginRequiredMixin, CreateView):
    model = StockMove
    form_class = MoveUnitForm
    template_name = 'stock_move/functions/MoveUnit.html'
    success_url = reverse_lazy('ListStockMove')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
    	#Si el movimiento es valido moved = True
        moved = True
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.form_class(request.POST)
                if form.is_valid():
                    move = form.save(commit=False)
                    # Si las funciones devuelven una lista de errores
                    # Devuelve el error y no se crea el movimiento
                    if moved:
                        errors = validations.validate_moves(request, move)
                        if errors:
                            data['error'] = errors
                            moved = False
                    if moved:
                        errors = validations.validate_stock_control(
                            request, move)
                        if errors:
                            data['error'] = errors
                            moved = False
                    if moved:
                        functions.create_stock_move(request, move)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class MovePackage(LoginRequiredMixin, CreateView):
    model = StockMove
    form_class = MovePackageForm
    template_name = 'stock_move/functions/MovePackage.html'
    success_url = reverse_lazy('ListStockMove')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        moved = True
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.form_class(request.POST)
                if form.is_valid():
                    move = form.save(commit=False)
                    # Si las funciones devuelven una lista de errores
                    # Devuelve el error y no se crea el movimiento
                    if moved:
                        errors = validations.validate_moves(request, move)
                        if errors:
                            data['error'] = errors
                            moved = False
                    if moved:
                        errors = validations.validate_stock_control(
                            request, move)
                        if errors:
                            data['error'] = errors
                            moved = False
                    if moved:
                        functions.create_stock_move(request, move)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


# ---------------------------STOCK CONTROL-------------------------#
# -----------------------------VIEWS--------------------------------#


class ListStockControl(LoginRequiredMixin, ListView):
    model = StockControl
    template_name = 'stock_control/views/ListStockControl.html'
