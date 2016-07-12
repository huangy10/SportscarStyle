"""
 Created by Woody Huang, 2016.07.10
 This file offers useful base view classes which can be used in Django apps
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from .utils import post_data_loader, login_first


class OperationView(View):
    """
     This class supports
    """

    operations = []

    @method_decorator(post_data_loader())
    def post(self, request, data, *args, **kwargs):
        op_type = data.get("op_type")
        if op_type in self.operations:
            handler = getattr(self, op_type.lower(), self.undefined_op_type)
            return handler(request, data, *args, **kwargs)
        else:
            return self.undefined_op_type(request, data, op_type=op_type)

    def undefined_op_type(self, request, data, op_type=None, **kwargs):
        if op_type is None:
            return JsonResponse(dict(success=False, message="Operation Type Not Found"))
        else:
            return JsonResponse(dict(success=False, message="Undefined Operation Type: %s" % op_type))


class LoginFirstOperationView(OperationView):

    @method_decorator(login_first)
    def post(self, request, *args, **kwargs):
        return super(LoginFirstOperationView, self).post(request, *args, **kwargs)
