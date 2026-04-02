from django.contrib import admin
from .models import APIRequest, APIResult

admin.site.register(APIRequest)
admin.site.register(APIResult)