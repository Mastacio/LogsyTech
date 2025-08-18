from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Cliente, Servicio, Cotizacion, DetalleCotizacion

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'empresa', 'telefono', 'fecha_creacion', 'activo']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'email', 'empresa']
    list_editable = ['activo']
    readonly_fields = ['id', 'fecha_creacion']
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'email', 'telefono')
        }),
        ('Información Empresarial', {
            'fields': ('empresa', 'direccion')
        }),
        ('Sistema', {
            'fields': ('id', 'fecha_creacion', 'activo'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_servicio', 'tarifa_hora', 'activo', 'fecha_creacion']
    list_filter = ['tipo_servicio', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['tarifa_hora', 'activo']
    readonly_fields = ['id', 'fecha_creacion']
    fieldsets = (
        ('Información del Servicio', {
            'fields': ('nombre', 'descripcion', 'tipo_servicio')
        }),
        ('Tarifas', {
            'fields': ('tarifa_hora',)
        }),
        ('Sistema', {
            'fields': ('id', 'fecha_creacion', 'activo'),
            'classes': ('collapse',)
        }),
    )

class DetalleCotizacionInline(admin.TabularInline):
    model = DetalleCotizacion
    extra = 1
    fields = ['servicio', 'descripcion', 'horas_estimadas', 'tarifa_hora', 'subtotal']
    readonly_fields = ['subtotal']

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = [
        'numero_cotizacion', 'cliente', 'estado', 'modalidad_pago', 
        'fecha_creacion', 'fecha_vencimiento', 'total_formatted'
    ]
    list_filter = ['estado', 'modalidad_pago', 'fecha_creacion', 'fecha_vencimiento']
    search_fields = ['numero_cotizacion', 'cliente__nombre', 'cliente__empresa']
    list_editable = ['estado']
    readonly_fields = [
        'id', 'numero_cotizacion', 'fecha_creacion', 'subtotal', 
        'descuento_monto', 'iva_monto', 'total'
    ]
    inlines = [DetalleCotizacionInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('cliente', 'fecha_vencimiento', 'modalidad_pago', 'estado')
        }),
        ('Cálculos', {
            'fields': ('descuento_porcentaje', 'iva_porcentaje'),
            'classes': ('collapse',)
        }),
        ('Totales (Calculados automáticamente)', {
            'fields': ('subtotal', 'descuento_monto', 'iva_monto', 'total'),
            'classes': ('collapse',)
        }),
        ('Información Adicional', {
            'fields': ('notas', 'terminos_condiciones'),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('id', 'numero_cotizacion', 'fecha_creacion'),
            'classes': ('collapse',)
        }),
    )

    def total_formatted(self, obj):
        return format_html('<strong>${:,.2f}</strong>', obj.total)
    total_formatted.short_description = 'Total'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Recalcular totales después de guardar
        obj.calcular_totales()

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)
        # Recalcular totales después de guardar los detalles
        if formset.model == DetalleCotizacion:
            form.instance.calcular_totales()

@admin.register(DetalleCotizacion)
class DetalleCotizacionAdmin(admin.ModelAdmin):
    list_display = ['cotizacion', 'servicio', 'horas_estimadas', 'tarifa_hora', 'subtotal_formatted']
    list_filter = ['servicio__tipo_servicio', 'cotizacion__estado']
    search_fields = ['cotizacion__numero_cotizacion', 'servicio__nombre']
    readonly_fields = ['id', 'subtotal']
    
    def subtotal_formatted(self, obj):
        return format_html('<strong>${:,.2f}</strong>', obj.subtotal)
    subtotal_formatted.short_description = 'Subtotal'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Recalcular totales de la cotización
        obj.cotizacion.calcular_totales()

# Configuración del sitio admin
admin.site.site_header = "Sistema de Cotizaciones"
admin.site.site_title = "Admin Cotizaciones"
admin.site.index_title = "Panel de Administración"
