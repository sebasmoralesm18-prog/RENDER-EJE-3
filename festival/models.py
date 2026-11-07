from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Edicion(models.Model):
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    edicion = models.ForeignKey(
        Edicion,
        on_delete=models.CASCADE
    )
    habilitada = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Opcion(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre


class Voto(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )

    edicion = models.ForeignKey(
        Edicion,
        on_delete=models.CASCADE
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    opcion = models.ForeignKey(
        Opcion,
        on_delete=models.CASCADE
    )

    fecha_voto = models.DateTimeField(
        auto_now_add=True
    )

#restriccion de voto doble.

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'usuario',
                    'edicion',
                    'categoria'
                ],
                name='voto_unico_por_categoria'
            )
        ]

    def __str__(self):
        return f"{self.usuario} - {self.categoria}"