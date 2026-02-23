from rest_framework.response import Response


def api_response(success, message, data=None, status_code=200):
    """
    Respuesta estándar para toda la API
    """
    return Response(
        {
            "success": success,
            "message": message,
            "data": data
        },
        status=status_code
    )
