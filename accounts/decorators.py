from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            if request.user.role not in roles:
                return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
            return func(request, *args, **kwargs)
        return wrapped
    return decorator
