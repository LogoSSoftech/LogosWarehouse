from django import forms
# from bootstrap_modal_forms.forms import BSModalForm
from apps.warehouse.models import Product
from apps.warehouse.models import StockLocation
from apps.warehouse.models import ProductUnit
from apps.warehouse.models import ProductPackage
from apps.warehouse.models import MeasurementUnit
from apps.warehouse.models import StockMove


class ReportForm(forms.Form):

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }))


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product

        fields = [
            'name',
            'active',
            'measure_id',
            'description',
            'product_image',
            'product_type',
            'article_qty',
            ]

    def clean(self):
        cleaned = super().clean()
        if cleaned['product_type'] == 'service' and cleaned['measure_id']:
            raise forms.ValidationError(
                'Los servicios no pueden tener Unidades de Medida')
        return cleaned

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductUnitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ProductUnit

        fields = [
            'name',
            'product_id',
            'fixed_ammount',
            'description',
            ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': "Nombre de la Unidad"}),
            'product_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'fixed_ammount': forms.CheckboxInput(),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Añadir una Descripción'}),
        }


class StockLocationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = StockLocation

        fields = [
            'name',
            'location_type',
            'active',
            'description',
            ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Ubicación'}),
            'location_type': forms.Select(
                attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Añadir Descripción'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned['location_type'] == 'Null':
            raise forms.ValidationError(
                'La ubicacion no puede ser Null')
        return cleaned

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductPackageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['unit_qty'].widget.attrs['autofocus'] = True

    class Meta:
        model = ProductPackage

        fields = [
            'product_id',
            'unit_qty',
            'fixed_ammount',
            'description',
            ]
        widgets = {
            'product_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'unit_qty': forms.NumberInput(
                attrs={'class': 'form-control'}),
            'fixed_ammount': forms.CheckboxInput(),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Añadir Descripción'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned['product_id'].article_qty \
                and cleaned['unit_qty'] != cleaned['product_id'].article_qty:
            raise forms.ValidationError(
                'La cantidad por unidad de este paquete debe ser igual '
                'a la cantidad por artículo del producto debido a que el '
                'producto es de tipo Articulo. En este caso, '
                'la cantidad debe ser %s' % cleaned['product_id'].article_qty)
        return cleaned

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class MeasurementUnitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = MeasurementUnit

        fields = [
            'name',
            'abbreviation',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Nombre unidad de Medida'}),
            'abbreviation': forms.TextInput(
                attrs={'placeholder': 'Kg., Lt, m2...'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Añadir Descripción'}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class MovePackageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['note'].widget.attrs['autofocus'] = True

    class Meta:
        model = StockMove

        fields = [
            'note',
            'pieces',
            'package_id',
            'location_id',
            'location_dest_id',
            'description',
            ]
        widgets = {
            'note': forms.TextInput(),
            'pieces': forms.NumberInput(),
            'package_id': forms.Select(),
            'location_id': forms.Select(),
            'location_dest_id': forms.Select(),
            'description': forms.Textarea(
                attrs={'placeholder': 'Agregue una Descripción'}),
        }


class MoveUnitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['note'].widget.attrs['autofocus'] = True

    unit_id = forms.ModelChoiceField(
        ProductUnit.objects.exclude(
            quantity__lte=0.000001,
            first_move=True))

    class Meta:
        model = StockMove

        fields = [
            'note',
            'quantity',
            'unit_id',
            'location_id',
            'location_dest_id',
            'description',
        ]
        widgets = {
            'note': forms.TextInput(),
            'quantity': forms.NumberInput(),
            'unit_id': forms.Select(),
            'location_id': forms.Select(),
            'location_dest_id': forms.Select(),
            'description': forms.Textarea(
                attrs={'placeholder': 'Agregue una Descripción'}),
        }
