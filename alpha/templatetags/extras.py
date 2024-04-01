import json

from django import template

from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse

register = template.Library()
from django.db import models


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            # if model
            if isinstance(obj, models.Model):
                return model_to_dict(obj)
            # if queryset
            if isinstance(obj, models.QuerySet):
                return [
                    model_to_dict(x) if isinstance(x, models.Model) else x for x in obj
                ]
            return super().default(obj)
        except TypeError:
            # print("JSON Conversion Error. Defaulting to string. Value:", obj)
            return str(obj)


@register.filter
def model_to_string(x):
    return json.dumps(x, cls=CustomJSONEncoder)
