from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_o_colaborador_required(view_func):
    """
    Decorador que permite el acceso si el usuario es un Administrador (Auth nativo)
    O si es un Colaborador (Sesión manual).
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # 1. Verificamos si es administrador
        es_admin = request.user.is_authenticated

        # 2. Verificamos si es colaborador
        # (Asegúrate de usar la llave correcta, aquí uso "colaborador" que fue el diccionario que creamos antes)
        es_colaborador = "colaborador" in request.session

        # Si cumple ALGUNA de las dos condiciones, lo dejamos pasar
        if es_admin or es_colaborador:
            return view_func(request, *args, **kwargs)

        # Si no cumple NINGUNA, lo bloqueamos
        else:
            messages.warning(
                request, "Debes iniciar sesión para acceder al formulario."
            )
            # Por defecto, lo mandamos al login de colaboradores (o al que prefieras)
            return redirect("control_plagas:login_colab")

    return _wrapped_view
