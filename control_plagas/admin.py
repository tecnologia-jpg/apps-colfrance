from django.contrib import admin
from .models import RegistroPlagas, TicketPlaga, ChatTicket


@admin.register(RegistroPlagas)
class RegistroPlagasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cedula",
        "area",
        "tipo_plaga",
        "plaga",
        "prioridad",
        "fecha_hora",
    )

    list_filter = ("fecha_hora", "area", "tipo_plaga", "plaga", "prioridad")

    search_fields = ("cedula", "plaga", "descripcion")

    date_hierarchy = "fecha_hora"

    # --- LA SOLUCIÓN ESTÁ AQUÍ ---
    # Le indicamos a Django que este campo es de solo lectura en el formulario
    readonly_fields = ("fecha_hora",)

    fieldsets = (
        (
            "Información del Reportante",
            {
                # Ahora Django dejará mostrar 'fecha_hora' porque sabe que es solo lectura
                "fields": ("cedula", "fecha_hora")
            },
        ),
        (
            "Detalles del Hallazgo",
            {"fields": ("area", "tipo_plaga", "plaga", "prioridad", "descripcion")},
        ),
        ("Material Adjunto", {"fields": ("evidencia",)}),
    )


@admin.register(TicketPlaga)
class TicketPlagaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "registro",
        "usuario_asignado",
        "estado",
        "hora_inicio",
        "hora_final",
    )
    list_filter = ("estado", "usuario_asignado")

    search_fields = ("registro__cedula", "descripcion_solucion")

    list_editable = ("estado",)


@admin.register(ChatTicket)
class ChatTicketAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "fecha", "mensaje")
    list_filter = ("fecha",)
    search_fields = ("mensaje", "ticket__id")
