from functools import wraps
from rest_framework import status
from rest_framework.response import Response

def api_exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
    return wrapper