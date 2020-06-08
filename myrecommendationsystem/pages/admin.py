from django.contrib import admin
from .models import Contactus,Places,Myrating

# Register your models here.
admin.site.register((Contactus)),
admin.site.register((Places)),
admin.site.register((Myrating))
