from django import template
from django.template.defaultfilters import floatformat
from django.utils.safestring import mark_safe
import locale

from cotizaciones.config import EMPRESA_CONFIG

register = template.Library()

# Configurar locale para formateo de moneda
try:
    locale.setlocale(locale.LC_ALL, 'es_DO.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
        except locale.Error:
            # Fallback a configuración por defecto
            pass

# Obtener símbolo de moneda desde config
DEFAULT_CURRENCY_SYMBOL = EMPRESA_CONFIG.get('moneda_simbolo', 'RD$')

@register.filter
def currency(value, currency_symbol=None):
    """
    Formatea un número como moneda con símbolo configurable.
    Uso: {{ value|currency }} o {{ value|currency:"$" }}
    """
    if currency_symbol is None:
        currency_symbol = DEFAULT_CURRENCY_SYMBOL

    if value is None:
        return mark_safe(f'{currency_symbol}0.00')
    
    try:
        # Convertir a float si es string
        if isinstance(value, str):
            value = float(value.replace(',', ''))
        
        # Formatear con separadores de miles y decimales
        formatted = locale.format_string('%.2f', value, grouping=True)
        
        # Asegurar que use punto como separador decimal
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        return mark_safe(f'{currency_symbol}{formatted}')
    except (ValueError, TypeError):
        return mark_safe(f'{currency_symbol}0.00')

@register.filter
def currency_rd(value):
    """
    Formatea un número como moneda dominicana (RD$) configurable desde config.
    Uso: {{ value|currency_rd }}
    """
    return currency(value, EMPRESA_CONFIG.get('moneda_simbolo', 'RD$'))

@register.filter
def currency_usd(value):
    """
    Formatea un número como moneda estadounidense (USD$)
    Uso: {{ value|currency_usd }}
    """
    return currency(value, 'USD$')

@register.filter
def currency_eur(value):
    """
    Formatea un número como moneda europea (€)
    Uso: {{ value|currency_eur }}
    """
    if value is None:
        return mark_safe('€0.00')
    
    try:
        if isinstance(value, str):
            value = float(value.replace(',', ''))
        
        formatted = locale.format_string('%.2f', value, grouping=True)
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        return mark_safe(f'€{formatted}')
    except (ValueError, TypeError):
        return mark_safe('€0.00')

@register.filter
def percentage(value, decimal_places=1):
    """
    Formatea un número como porcentaje
    Uso: {{ value|percentage }} o {{ value|percentage:2 }}
    """
    if value is None:
        return mark_safe('0%')
    
    try:
        if isinstance(value, str):
            value = float(value.replace(',', ''))
        
        formatted = floatformat(value, decimal_places)
        return mark_safe(f'{formatted}%')
    except (ValueError, TypeError):
        return mark_safe('0%')

@register.filter
def number_format(value, decimal_places=2):
    """
    Formatea un número con separadores de miles
    Uso: {{ value|number_format }} o {{ value|number_format:0 }}
    """
    if value is None:
        return mark_safe('0')
    
    try:
        if isinstance(value, str):
            value = float(value.replace(',', ''))
        
        formatted = locale.format_string(f'%.{decimal_places}f', value, grouping=True)
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        return mark_safe(formatted)
    except (ValueError, TypeError):
        return mark_safe('0')

@register.filter
def currency_compact(value):
    """
    Formatea moneda en formato compacto (K, M, B)
    Uso: {{ value|currency_compact }}
    """
    symbol = EMPRESA_CONFIG.get('moneda_simbolo', 'RD$')
    if value is None:
        return mark_safe(f'{symbol}0')
    
    try:
        if isinstance(value, str):
            value = float(value.replace(',', ''))
        
        if value >= 1000000000:
            return mark_safe(f'{symbol}{value/1000000000:.1f}B')
        elif value >= 1000000:
            return mark_safe(f'{symbol}{value/1000000:.1f}M')
        elif value >= 1000:
            return mark_safe(f'{symbol}{value/1000:.1f}K')
        else:
            return currency_rd(value)
    except (ValueError, TypeError):
        return mark_safe(f'{symbol}0')

@register.filter
def currency_with_words(value):
    """
    Formatea moneda con palabras para números grandes
    Uso: {{ value|currency_with_words }}
    """
    symbol = EMPRESA_CONFIG.get('moneda_simbolo', 'RD$')
    if value is None:
        return mark_safe(f'{symbol}0.00')
    
    try:
        if isinstance(value, str):
            value = float(value.replace(',', ''))
        
        if value >= 1000000:
            millions = int(value // 1000000)
            remainder = value % 1000000
            if remainder > 0:
                return mark_safe(f'{symbol}{millions:,} millones {currency_rd(remainder)}')
            else:
                return mark_safe(f'{symbol}{millions:,} millones')
        elif value >= 1000:
            thousands = int(value // 1000)
            remainder = value % 1000
            if remainder > 0:
                return mark_safe(f'{symbol}{thousands:,} mil {currency_rd(remainder)}')
            else:
                return mark_safe(f'{symbol}{thousands:,} mil')
        else:
            return currency_rd(value)
    except (ValueError, TypeError):
        return mark_safe(f'{symbol}0.00')
