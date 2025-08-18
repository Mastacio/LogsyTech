from django.urls import path
from . import views

app_name = 'cotizaciones'

urlpatterns = [
    # URLs principales
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # URLs para Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<uuid:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<uuid:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # URLs para Servicios
    path('servicios/', views.ServicioListView.as_view(), name='servicio_list'),
    path('servicios/nuevo/', views.ServicioCreateView.as_view(), name='servicio_create'),
    path('servicios/<uuid:pk>/editar/', views.ServicioUpdateView.as_view(), name='servicio_update'),
    path('servicios/<uuid:pk>/eliminar/', views.ServicioDeleteView.as_view(), name='servicio_delete'),
    
    # URLs para Cotizaciones
    path('cotizaciones/', views.CotizacionListView.as_view(), name='cotizacion_list'),
    path('cotizaciones/nueva/', views.CotizacionCreateView.as_view(), name='cotizacion_create'),
    path('cotizaciones/nueva-completa/', views.cotizacion_completa_create, name='cotizacion_completa_create'),
    path('cotizaciones/<uuid:pk>/', views.CotizacionDetailView.as_view(), name='cotizacion_detail'),
    path('cotizaciones/<uuid:pk>/editar/', views.CotizacionUpdateView.as_view(), name='cotizacion_update'),
    path('cotizaciones/<uuid:pk>/detalles/', views.cotizacion_detalles_edit, name='cotizacion_detalles_edit'),
    path('cotizaciones/<uuid:pk>/eliminar/', views.CotizacionDeleteView.as_view(), name='cotizacion_delete'),
    path('cotizaciones/<uuid:pk>/pdf/', views.generar_pdf_cotizacion, name='cotizacion_pdf'),
    path('cotizaciones/<uuid:pk>/pdf-sin-info/', views.generar_pdf_cotizacion_sin_info, name='cotizacion_pdf_sin_info'),
    path('api/servicio-tarifa/', views.obtener_tarifa_servicio, name='obtener_tarifa_servicio'),
]

