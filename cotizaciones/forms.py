from django import forms
from django.forms import inlineformset_factory
from .models import Cliente, Servicio, Cotizacion, DetalleCotizacion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button, HTML
from crispy_forms.bootstrap import TabHolder, Tab
from decimal import Decimal
import datetime

class ClienteForm(forms.ModelForm):
    """Formulario para crear y editar clientes"""
    
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'empresa', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6'),
                Column('empresa', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'direccion',
            Submit('submit', 'Guardar Cliente', css_class='btn btn-primary')
        )

class ServicioForm(forms.ModelForm):
    """Formulario para crear y editar servicios"""
    
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'tipo_servicio', 'tarifa_hora']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tipo_servicio': forms.Select(attrs={'class': 'form-control'}),
            'tarifa_hora': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-6'),
                Column('tipo_servicio', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'descripcion',
            Row(
                Column('tarifa_hora', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar Servicio', css_class='btn btn-primary')
        )

class CotizacionForm(forms.ModelForm):
    """Formulario para crear y editar cotizaciones"""
    
    class Meta:
        model = Cotizacion
        fields = [
            'cliente', 'fecha_vencimiento', 'modalidad_pago', 'estado',
            'descuento_porcentaje', 'iva_porcentaje', 'notas', 'terminos_condiciones'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'modalidad_pago': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'descuento_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'iva_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'terminos_condiciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        
        # Establecer fecha de vencimiento por defecto (30 días desde hoy)
        if not self.instance.pk:
            self.fields['fecha_vencimiento'].initial = datetime.date.today() + datetime.timedelta(days=30)
        
        self.helper.layout = Layout(
            TabHolder(
                Tab('Información General',
                    Row(
                        Column('cliente', css_class='form-group col-md-6'),
                        Column('fecha_vencimiento', css_class='form-group col-md-6'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('modalidad_pago', css_class='form-group col-md-6'),
                        Column('estado', css_class='form-group col-md-6'),
                        css_class='form-row'
                    ),
                ),
                Tab('Configuración Fiscal',
                    Row(
                        Column('descuento_porcentaje', css_class='form-group col-md-6'),
                        Column('iva_porcentaje', css_class='form-group col-md-6'),
                        css_class='form-row'
                    ),
                ),
                Tab('Notas y Términos',
                    'notas',
                    'terminos_condiciones',
                )
            ),
            Submit('submit', 'Guardar Cotización', css_class='btn btn-primary')
        )

class DetalleCotizacionForm(forms.ModelForm):
    """Formulario para crear y editar detalles de cotización"""
    
    class Meta:
        model = DetalleCotizacion
        fields = ['servicio', 'descripcion', 'horas_estimadas', 'tarifa_hora']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'horas_estimadas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0.5'}),
            'tarifa_hora': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar las opciones del campo servicio para incluir tarifas
        if 'servicio' in self.fields:
            servicios = Servicio.objects.filter(activo=True).order_by('nombre')
            choices = [('', 'Seleccionar servicio...')]
            for servicio in servicios:
                choices.append((servicio.id, f'{servicio.nombre} - ${servicio.tarifa_hora}/hora'))
            self.fields['servicio'].choices = choices
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Row(
                Column('servicio', css_class='form-group col-md-6'),
                Column('horas_estimadas', css_class='form-group col-md-3'),
                Column('tarifa_hora', css_class='form-group col-md-3'),
                css_class='form-row'
            ),
            'descripcion',
            Submit('submit', 'Guardar Detalle', css_class='btn btn-primary')
        )

    def clean(self):
        cleaned_data = super().clean()
        horas_estimadas = cleaned_data.get('horas_estimadas')
        tarifa_hora = cleaned_data.get('tarifa_hora')
        
        # Solo validar si hay datos
        if horas_estimadas and horas_estimadas <= 0:
            raise forms.ValidationError("Las horas estimadas deben ser mayores a 0.")
        
        if tarifa_hora and tarifa_hora <= 0:
            raise forms.ValidationError("La tarifa por hora debe ser mayor a 0.")
        
        return cleaned_data

# Formset para manejar múltiples detalles de cotización
DetalleCotizacionFormSet = inlineformset_factory(
    Cotizacion,
    DetalleCotizacion,
    form=DetalleCotizacionForm,
    extra=1,
    can_delete=True,
    fields=['servicio', 'descripcion', 'horas_estimadas', 'tarifa_hora']
)

class CotizacionCompletaForm(forms.ModelForm):
    """Formulario completo para cotización con detalles"""
    
    class Meta:
        model = Cotizacion
        fields = [
            'cliente', 'fecha_vencimiento', 'modalidad_pago', 'estado',
            'descuento_porcentaje', 'iva_porcentaje', 'notas', 'terminos_condiciones'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'modalidad_pago': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'descuento_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'iva_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'terminos_condiciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        
        # Establecer fecha de vencimiento por defecto
        if not self.instance.pk:
            self.fields['fecha_vencimiento'].initial = datetime.date.today() + datetime.timedelta(days=30)
        
        self.helper.layout = Layout(
            HTML('<h3>Información de la Cotización</h3>'),
            Row(
                Column('cliente', css_class='form-group col-md-6'),
                Column('fecha_vencimiento', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('modalidad_pago', css_class='form-group col-md-6'),
                Column('estado', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('descuento_porcentaje', css_class='form-group col-md-6'),
                Column('iva_porcentaje', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'notas',
            'terminos_condiciones',
            HTML('<h3>Detalles de Servicios</h3>'),
            HTML('<div id="detalles-container"></div>'),
            Submit('submit', 'Guardar Cotización Completa', css_class='btn btn-primary')
        )

