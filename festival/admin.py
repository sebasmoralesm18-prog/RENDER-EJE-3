from django.contrib import admin
from .models import Usuario, Edicion, Categoria, Opcion, Voto

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Edicion)
admin.site.register(Categoria)
admin.site.register(Opcion)
admin.site.register(Voto)