# Base_Datos/templatetags/form_tags.py
from django import template
from django.utils.html import format_html
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    """
    Añade o mergea la clase CSS al widget del campo.
    Uso: {{ form.field|add_class:"form-control" }}
    Maneja BoundField y strings de fallback.
    """
    try:
        if isinstance(field, BoundField):
            existing = field.field.widget.attrs.copy()
            # merge classes
            prev = existing.get("class", "")
            classes = (prev + " " + css).strip()
            existing["class"] = classes
            return field.as_widget(attrs=existing)
        # si llaman al filtro sobre una cadena u otro, simplemente devuelvo campo normal
        return field.as_widget(attrs={"class": css})
    except Exception:
        return field
