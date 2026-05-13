from django.contrib import admin
from .models import RegistroPlagas

# Register your models here.
@admin.register(RegistroPlagas)
class RegistroPlagasAdmin(admin.ModelAdmin):
    list_display= ("importancia","tipo_plaga","descripcion","area","fecha_hora","estado")
    search_fields= ("importancia",)
    list_filter= ("importancia",)
    
    