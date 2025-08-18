from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from io import BytesIO
import os
from datetime import datetime, timedelta
import json

from .models import Cliente, Servicio, Cotizacion, DetalleCotizacion
from .forms import (
    ClienteForm, ServicioForm, CotizacionForm, DetalleCotizacionForm,
    DetalleCotizacionFormSet, CotizacionCompletaForm
)
from .config import EMPRESA_CONFIG

# Vistas para Clientes
class ClienteListView(ListView):
    model = Cliente
    template_name = 'cotizaciones/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        queryset = Cliente.objects.filter(activo=True)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(empresa__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cotizaciones/cliente_form.html'
    success_url = reverse_lazy('cotizaciones:cliente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente creado exitosamente.')
        return super().form_valid(form)

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cotizaciones/cliente_form.html'
    success_url = reverse_lazy('cotizaciones:cliente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente actualizado exitosamente.')
        return super().form_valid(form)

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'cotizaciones/cliente_confirm_delete.html'
    success_url = reverse_lazy('cotizaciones:cliente_list')

    def delete(self, request, *args, **kwargs):
        cliente = self.get_object()
        cliente.activo = False
        cliente.save()
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect(self.success_url)

# Vistas para Servicios
class ServicioListView(ListView):
    model = Servicio
    template_name = 'cotizaciones/servicio_list.html'
    context_object_name = 'servicios'
    paginate_by = 10

    def get_queryset(self):
        queryset = Servicio.objects.filter(activo=True)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(tipo_servicio__icontains=search)
            )
        return queryset

class ServicioCreateView(CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'cotizaciones/servicio_form.html'
    success_url = reverse_lazy('cotizaciones:servicio_list')

    def form_valid(self, form):
        messages.success(self.request, 'Servicio creado exitosamente.')
        return super().form_valid(form)

class ServicioUpdateView(UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'cotizaciones/servicio_form.html'
    success_url = reverse_lazy('cotizaciones:servicio_list')

    def form_valid(self, form):
        messages.success(self.request, 'Servicio actualizado exitosamente.')
        return super().form_valid(form)

class ServicioDeleteView(DeleteView):
    model = Servicio
    template_name = 'cotizaciones/servicio_confirm_delete.html'
    success_url = reverse_lazy('cotizaciones:servicio_list')

    def delete(self, request, *args, **kwargs):
        servicio = self.get_object()
        servicio.activo = False
        servicio.save()
        messages.success(request, 'Servicio eliminado exitosamente.')
        return redirect(self.success_url)

# Vistas para Cotizaciones
class CotizacionListView(ListView):
    model = Cotizacion
    template_name = 'cotizaciones/cotizacion_list.html'
    context_object_name = 'cotizaciones'
    paginate_by = 10

    def get_queryset(self):
        queryset = Cotizacion.objects.all().select_related('cliente')
        search = self.request.GET.get('search')
        estado = self.request.GET.get('estado')
        
        if search:
            queryset = queryset.filter(
                Q(numero_cotizacion__icontains=search) |
                Q(cliente__nombre__icontains=search) |
                Q(cliente__empresa__icontains=search)
            )
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = Cotizacion.ESTADO_CHOICES
        return context

class CotizacionCreateView(CreateView):
    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizaciones/cotizacion_form.html'
    success_url = reverse_lazy('cotizaciones:cotizacion_list')

    def form_valid(self, form):
        cotizacion = form.save()
        messages.success(self.request, f'Cotización {cotizacion.numero_cotizacion} creada exitosamente.')
        return redirect(reverse('cotizaciones:cotizacion_detail', kwargs={'pk': cotizacion.pk}))

class CotizacionUpdateView(UpdateView):
    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizaciones/cotizacion_form.html'

    def get_success_url(self):
        return reverse('cotizaciones:cotizacion_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Cotización actualizada exitosamente.')
        return super().form_valid(form)

class CotizacionDetailView(DetailView):
    model = Cotizacion
    template_name = 'cotizaciones/cotizacion_detail.html'
    context_object_name = 'cotizacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detallecotizacion_set.all()
        return context

class CotizacionDeleteView(DeleteView):
    model = Cotizacion
    template_name = 'cotizaciones/cotizacion_confirm_delete.html'
    success_url = reverse_lazy('cotizaciones:cotizacion_list')

    def delete(self, request, *args, **kwargs):
        cotizacion = self.get_object()
        numero = cotizacion.numero_cotizacion
        cotizacion.delete()
        messages.success(request, f'Cotización {numero} eliminada exitosamente.')
        return redirect(self.success_url)

# Vista para crear cotización completa con detalles
def cotizacion_completa_create(request):
    if request.method == 'POST':
        form = CotizacionCompletaForm(request.POST)
        if form.is_valid():
            cotizacion = form.save()
            messages.success(request, f'Cotización {cotizacion.numero_cotizacion} creada exitosamente.')
            return redirect(reverse('cotizaciones:cotizacion_detail', kwargs={'pk': cotizacion.pk}))
    else:
        form = CotizacionCompletaForm()
    
    return render(request, 'cotizaciones/cotizacion_completa_form.html', {
        'form': form,
        'title': 'Nueva Cotización'
    })

# Vista para editar detalles de cotización
def cotizacion_detalles_edit(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    
    if request.method == 'POST':
        formset = DetalleCotizacionFormSet(request.POST, instance=cotizacion)
        if formset.is_valid():
            # Usar el método save() estándar del formset
            formset.save()
            
            # Recalcular totales
            cotizacion.calcular_totales()
            
            messages.success(request, 'Detalles de cotización actualizados exitosamente.')
            return redirect(reverse('cotizaciones:cotizacion_detail', kwargs={'pk': cotizacion.pk}))
        else:
            # Si hay errores, mostrar mensaje
            messages.error(request, 'Por favor corrija los errores en el formulario.')
            print("Errores del formset:", formset.errors)  # Debug
            print("Non form errors:", formset.non_form_errors())  # Debug
            print("POST data:", request.POST)  # Debug para ver qué datos se están enviando
    else:
        formset = DetalleCotizacionFormSet(instance=cotizacion)
    
    # Obtener todos los servicios activos para el formulario
    servicios = Servicio.objects.filter(activo=True).order_by('nombre')
    
    return render(request, 'cotizaciones/cotizacion_detalles_form.html', {
        'formset': formset,
        'cotizacion': cotizacion,
        'servicios': servicios,
        'title': f'Editar Detalles - {cotizacion.numero_cotizacion}'
    })

# Vista para generar PDF
def generar_pdf_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    detalles = cotizacion.detallecotizacion_set.all()
    
    # Renderizar el template HTML
    html_string = render_to_string('cotizaciones/template_pdf_cotizacion.html', {
        'cotizacion': cotizacion,
        'detalles': detalles,
        'empresa': EMPRESA_CONFIG,
    })
    
    # Configurar fuentes
    font_config = FontConfiguration()
    
    # Crear el PDF usando WeasyPrint
    html = HTML(string=html_string)
    css = CSS(string='', font_config=font_config)
    
    # Generar el PDF
    pdf = html.write_pdf(stylesheets=[css], font_config=font_config)
    
    # Crear la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cotizacion_{cotizacion.numero_cotizacion}.pdf"'
    response.write(pdf)
    
    return response

# Vista para generar PDF sin información de la empresa
def generar_pdf_cotizacion_sin_info(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    detalles = cotizacion.detallecotizacion_set.all()
    
    # Renderizar el template HTML
    html_string = render_to_string('cotizaciones/template_pdf_cotizacion_withoutinfo.html', {
        'cotizacion': cotizacion,
        'detalles': detalles,
        #'empresa': EMPRESA_CONFIG,
    })
    
    # Configurar fuentes
    font_config = FontConfiguration()
    
    # Crear el PDF usando WeasyPrint
    html = HTML(string=html_string)
    css = CSS(string='', font_config=font_config)
    
    # Generar el PDF
    pdf = html.write_pdf(stylesheets=[css], font_config=font_config)
    
    # Crear la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cotizacion_{cotizacion.numero_cotizacion}.pdf"'
    response.write(pdf)
    
    return response



# Vista para el dashboard
def dashboard(request):
    # Estadísticas básicas
    total_cotizaciones = Cotizacion.objects.count()
    cotizaciones_pendientes = Cotizacion.objects.filter(estado='enviada').count()
    cotizaciones_aprobadas = Cotizacion.objects.filter(estado='aprobada').count()
    total_clientes = Cliente.objects.filter(activo=True).count()
    
    # Cotizaciones recientes
    cotizaciones_recientes = Cotizacion.objects.select_related('cliente').order_by('-fecha_creacion')[:5]
    
    # Cotizaciones por estado
    cotizaciones_por_estado = {}
    for estado, nombre in Cotizacion.ESTADO_CHOICES:
        cotizaciones_por_estado[nombre] = Cotizacion.objects.filter(estado=estado).count()
    
    context = {
        'total_cotizaciones': total_cotizaciones,
        'cotizaciones_pendientes': cotizaciones_pendientes,
        'cotizaciones_aprobadas': cotizaciones_aprobadas,
        'total_clientes': total_clientes,
        'cotizaciones_recientes': cotizaciones_recientes,
        'cotizaciones_por_estado': cotizaciones_por_estado,
    }
    
    return render(request, 'cotizaciones/dashboard.html', context)

# Vista principal
def home(request):
    return redirect('cotizaciones:dashboard')

# Vista AJAX para obtener tarifa de servicio
def obtener_tarifa_servicio(request):
    if request.method == 'GET':
        servicio_id = request.GET.get('servicio_id')
        try:
            servicio = Servicio.objects.get(id=servicio_id, activo=True)
            return JsonResponse({
                'success': True,
                'tarifa': float(servicio.tarifa_hora),
                'nombre': servicio.nombre
            })
        except Servicio.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Servicio no encontrado'
            })
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
