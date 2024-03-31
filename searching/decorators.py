from functools import wraps

from user.utils import validateStaffUser, validateSuperUser


def roleValidation(validation_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(instance, request, *args, **kwargs):
            token = request.META['HTTP_AUTHORIZATION']

            if validation_type == 'staff':
                validationResponse = validateStaffUser(token)
            elif validation_type == 'admin':
                validationResponse = validateSuperUser(token)
            else:
                raise ValueError("Invalid validation type specified")

            if validationResponse:
                return validationResponse

            return view_func(instance, request, *args, **kwargs)

        return _wrapped_view

    return decorator
