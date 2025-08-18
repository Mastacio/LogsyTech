from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class Cliente(models.Model):
    """Modelo para almacenar información de clientes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200, verbose_name="Nombre completo")
    email = models.EmailField(verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    empresa = models.CharField(max_length=200, blank=True, verbose_name="Empresa")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True, verbose_name="Cliente activo")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - {self.empresa}" if self.empresa else self.nombre

class Servicio(models.Model):
    """Modelo para definir servicios y sus tarifas"""
    TIPO_SERVICIO_CHOICES = [
        ('desarrollo', 'Desarrollo de Software'),
        ('mantenimiento', 'Mantenimiento'),
        ('consultoria', 'Consultoría'),
        ('capacitacion', 'Capacitación'),
        ('otro', 'Otro'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200, verbose_name="Nombre del servicio")
    descripcion = models.TextField(verbose_name="Descripción")
    tipo_servicio = models.CharField(max_length=20, choices=TIPO_SERVICIO_CHOICES, default='desarrollo')
    tarifa_hora = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Tarifa por hora (USD)"
    )
    activo = models.BooleanField(default=True, verbose_name="Servicio activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['tipo_servicio', 'nombre']

    def __str__(self):
        return f"{self.nombre} - ${self.tarifa_hora}/hora"

class Cotizacion(models.Model):
    """Modelo principal para las cotizaciones"""
    MODALIDAD_PAGO_CHOICES = [
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
        ('unico', 'Pago único'),
    ]
    
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('enviada', 'Enviada'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_cotizacion = models.CharField(max_length=20, unique=True, verbose_name="Número de cotización")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento")
    modalidad_pago = models.CharField(max_length=10, choices=MODALIDAD_PAGO_CHOICES, default='unico')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    
    # Campos de cálculo
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Descuento (%)")
    descuento_monto = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Descuento (USD)")
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=16, verbose_name="IVA (%)")
    iva_monto = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="IVA (USD)")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Campos adicionales
    notas = models.TextField(blank=True, verbose_name="Notas adicionales")
    terminos_condiciones = models.TextField(blank=True, verbose_name="Términos y condiciones")
    
    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Cotización {self.numero_cotizacion} - {self.cliente.nombre}"

    def calcular_totales(self):
        """Calcula todos los totales de la cotización"""
        # Calcular subtotal
        self.subtotal = sum(detalle.subtotal for detalle in self.detallecotizacion_set.all())
        
        # Calcular descuento
        if self.descuento_porcentaje > 0:
            self.descuento_monto = (self.subtotal * self.descuento_porcentaje) / 100
        else:
            self.descuento_monto = 0
        
        # Calcular base imponible
        base_imponible = self.subtotal - self.descuento_monto
        
        # Calcular IVA
        self.iva_monto = (base_imponible * self.iva_porcentaje) / 100
        
        # Calcular total
        self.total = base_imponible + self.iva_monto
        
        self.save()

    def generar_numero_cotizacion(self):
        """Genera un número único de cotización"""
        if not self.numero_cotizacion:
            ultima_cotizacion = Cotizacion.objects.order_by('-fecha_creacion').first()
            if ultima_cotizacion and ultima_cotizacion.numero_cotizacion:
                try:
                    ultimo_numero = int(ultima_cotizacion.numero_cotizacion.split('-')[1])
                    nuevo_numero = ultimo_numero + 1
                except (IndexError, ValueError):
                    nuevo_numero = 1
            else:
                nuevo_numero = 1
            
            self.numero_cotizacion = f"COT-{nuevo_numero:04d}"
        
        return self.numero_cotizacion

    def save(self, *args, **kwargs):
        if not self.numero_cotizacion:
            self.numero_cotizacion = self.generar_numero_cotizacion()
        super().save(*args, **kwargs)

class DetalleCotizacion(models.Model):
    """Modelo para los detalles de cada cotización"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, verbose_name="Servicio")
    descripcion = models.TextField(verbose_name="Descripción del trabajo")
    horas_estimadas = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Horas estimadas"
    )
    tarifa_hora = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Tarifa por hora (USD)"
    )
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = "Detalle de cotización"
        verbose_name_plural = "Detalles de cotización"

    def __str__(self):
        return f"{self.servicio.nombre} - {self.horas_estimadas}h"

    def calcular_subtotal(self):
        """Calcula el subtotal del detalle"""
        self.subtotal = self.horas_estimadas * self.tarifa_hora
        return self.subtotal

    def save(self, *args, **kwargs):
        if not self.tarifa_hora:
            self.tarifa_hora = self.servicio.tarifa_hora
        self.subtotal = self.calcular_subtotal()
        super().save(*args, **kwargs)
        # Recalcular totales de la cotización
        self.cotizacion.calcular_totales()
