from django.shortcuts import render, redirect
from .forms import UsuarioForm
from .models import Usuario
from .models import Voto, Categoria, Opcion, Edicion
from .forms import VotoForm
from django.db.models import Count
from django.http import JsonResponse
from .forms import CategoriaForm
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404
from .forms import CategoriaForm, EdicionForm, OpcionForm

def inicio(request):

            if 'usuario_id' not in request.session:
                return redirect('login')

            usuario = Usuario.objects.get(
                id=request.session['usuario_id']
            )

            return render(
                request,
                'inicio.html',
                {
                    'usuario': usuario
                }
            )

def index(request):
            return render(request, 'index.html')

def registro(request):

    if request.method == 'POST':

        formulario = UsuarioForm(request.POST)

        if formulario.is_valid():

            correo = formulario.cleaned_data['correo']

            if Usuario.objects.filter(correo=correo).exists():

                return render(
                    request,
                    'registro.html',
                    {
                        'formulario': formulario,
                        'mensaje': 'El correo ya se encuentra registrado'
                    }
                )

            formulario.save()

            return redirect('login')

    else:

        formulario = UsuarioForm()

    return render(
        request,
        'registro.html',
        {
            'formulario': formulario
        }
    )


def login(request):

    mensaje = ""

    if request.method == 'POST':

        correo = request.POST['correo']
        password = request.POST['password']

        # 1. Intentar autenticar al administrador de Django
        User = get_user_model()

        administrador = User.objects.filter(
            email__iexact=correo
        ).first()

        username = administrador.username if administrador else correo

        usuario_admin = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario_admin and (
            usuario_admin.is_superuser or usuario_admin.is_staff
        ):

            request.session.pop('usuario_id', None)

            auth_login(request, usuario_admin)

            return redirect('panel_administrativo')

        # 2. Si no es administrador, buscar usuario normal
        try:

            usuario = Usuario.objects.get(
                correo=correo,
                password=password
            )

            auth_logout(request)

            request.session['usuario_id'] = usuario.id

            return redirect('inicio')

        except Usuario.DoesNotExist:

            mensaje = "Usuario o contraseña incorrectos"

    return render(
        request,
        'login.html',
        {
            'mensaje': mensaje
        }
    )

def panel_administrativo(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    return render(
        request,
        'panel_administrativo.html'
    )


def votar(request, categoria_id):

            mensaje = ""

            categoria = Categoria.objects.get(
                id=categoria_id
                
            )

            if not categoria.edicion.activa:

                return render(
                    request,
                    'votacion.html',
                    {
                        'categoria': categoria,
                        'opciones': [],
                        'mensaje': 'Esta edición no está habilitada para votaciones.'
                    }
                )

            if not categoria.habilitada:

                return render(
                    request,
                    'votacion.html',
                    {
                        'categoria': categoria,
                        'opciones': [],
                        'mensaje': 'La categoría seleccionada no está habilitada para votación.'
                    }
                )

            opciones = Opcion.objects.filter(
                categoria=categoria
            )

            if request.method == 'POST':

                usuario = Usuario.objects.get(
            id=request.session['usuario_id']
                )

                opcion_id = request.POST['opcion']

                opcion = Opcion.objects.get(
                    id=opcion_id

                )

                if opcion.categoria != categoria:

                    return render(
                request,
                'votacion.html',
                {
                    'categoria': categoria,
                    'opciones': opciones,
                    'mensaje': 'La opción seleccionada no pertenece a esta categoría.'
                }
                )

                edicion = categoria.edicion

                existe_voto = Voto.objects.filter(
                    usuario=usuario,
                    categoria=categoria,
                    edicion=edicion
                ).exists()

                if existe_voto:

                    mensaje = "Ya votaste en esta categoría"

                else:

                    Voto.objects.create(
                        usuario=usuario,
                        categoria=categoria,
                        edicion=edicion,
                        opcion=opcion
                    )

                    mensaje = "Voto registrado correctamente"

            return render(
                request,
                'votacion.html',
                {
                    'categoria': categoria,
                    'opciones': opciones,
                    'mensaje': mensaje
                }
            )

def categorias_votacion(request):

            if 'usuario_id' not in request.session:
                return redirect('login')

            categorias = Categoria.objects.all()

            return render(
                request,
                'categorias_votacion.html',
                {
                    'categorias': categorias
                }
            )

def mis_votos(request):

            if 'usuario_id' not in request.session:
                return redirect('login')

            usuario = Usuario.objects.get(
            id=request.session['usuario_id']
            )

            votos = Voto.objects.filter(
                usuario=usuario
            )

            return render(
                request,
                'mis_votos.html',
                {
                    'votos': votos
                }
            )

def resultados(request):

            if 'usuario_id' not in request.session:
                    return redirect('login')
            

            categorias = Categoria.objects.all()

            resultados = []

            for categoria in categorias:

                opciones = (
                    Opcion.objects
                    .filter(categoria=categoria)
                    .annotate(total_votos=Count('voto'))
                    .order_by('-total_votos')
                )

                resultados.append({
                    'categoria': categoria,
                    'opciones': opciones
                })

            return render(
                request,
                'resultados.html',
                {
                    'resultados': resultados
                }
            )

def logout(request):

            request.session.flush()

            return redirect('login')

def api_categorias(request):

            categorias = Categoria.objects.all()

            datos = []

            for categoria in categorias:

                opciones = Opcion.objects.filter(
                    categoria=categoria
                )

                datos.append({
                    'categoria': categoria.nombre,
                    'opciones': [
                        opcion.nombre
                        for opcion in opciones
                    ]
                })

            return JsonResponse(
                datos,
                safe=False
)


def crear_categoria(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    if request.method == 'POST':

        formulario = CategoriaForm(request.POST)

        if formulario.is_valid():

            formulario.save()

            return redirect('administrar_categorias')

    else:

        formulario = CategoriaForm()

    return render(
        request,
        'crear_categoria.html',
        {
            'formulario': formulario
        }
    )

def administrar_categorias(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    categorias = Categoria.objects.select_related(
        'edicion'
    ).all().order_by('id')

    return render(
        request,
        'administrar_categorias.html',
        {
            'categorias': categorias
        }
    )


def editar_categoria(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':

        formulario = CategoriaForm(
            request.POST,
            instance=categoria
        )

        if formulario.is_valid():

            formulario.save()

            return redirect('administrar_categorias')

    else:

        formulario = CategoriaForm(instance=categoria)

    return render(
        request,
        'editar_categoria.html',
        {
            'formulario': formulario,
            'categoria': categoria
        }
    )



def eliminar_categoria(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    categoria = get_object_or_404(Categoria, id=id)

    tiene_votos = Voto.objects.filter(
        categoria=categoria
    ).exists()

    if request.method == 'POST':

        if tiene_votos:

            return render(
                request,
                'confirmar_eliminar_categoria.html',
                {
                    'categoria': categoria,
                    'tiene_votos': True
                }
            )

        categoria.delete()

        return redirect('administrar_categorias')

    return render(
        request,
        'confirmar_eliminar_categoria.html',
        {
            'categoria': categoria,
            'tiene_votos': tiene_votos
        }
    )

def cambiar_estado_categoria(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    if request.method == 'POST':

        categoria = get_object_or_404(Categoria, id=id)

        categoria.habilitada = not categoria.habilitada
        categoria.save()

    return redirect('administrar_categorias')


def administrar_ediciones(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    ediciones = Edicion.objects.all().order_by('-id')

    return render(
        request,
        'administrar_ediciones.html',
        {
            'ediciones': ediciones
        }
    )



def crear_edicion(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    if request.method == 'POST':

        formulario = EdicionForm(request.POST)

        if formulario.is_valid():

            formulario.save()

            return redirect('administrar_ediciones')

    else:

        formulario = EdicionForm()

    return render(
        request,
        'crear_edicion.html',
        {
            'formulario': formulario
        }
    )



def editar_edicion(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    edicion = get_object_or_404(Edicion, id=id)

    if request.method == 'POST':

        formulario = EdicionForm(
            request.POST,
            instance=edicion
        )

        if formulario.is_valid():

            formulario.save()

            return redirect('administrar_ediciones')

    else:

        formulario = EdicionForm(instance=edicion)

    return render(
        request,
        'editar_edicion.html',
        {
            'formulario': formulario,
            'edicion': edicion
        }
    )

def cambiar_estado_edicion(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    if request.method == 'POST':
        edicion = get_object_or_404(Edicion, id=id)

        edicion.activa = not edicion.activa
        edicion.save()

    return redirect('administrar_ediciones')

def administrar_opciones(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    opciones = Opcion.objects.select_related('categoria').all().order_by('id')

    return render(request, 'administrar_opciones.html', {
        'opciones': opciones
    })


def crear_opcion(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    if request.method == 'POST':
        formulario = OpcionForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect('administrar_opciones')

    else:
        formulario = OpcionForm()

    return render(request, 'crear_opcion.html', {
        'formulario': formulario
    })


def editar_opcion(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    opcion = get_object_or_404(Opcion, id=id)

    if request.method == 'POST':
        formulario = OpcionForm(request.POST, instance=opcion)

        if formulario.is_valid():
            formulario.save()
            return redirect('administrar_opciones')

    else:
        formulario = OpcionForm(instance=opcion)

    return render(request, 'editar_opcion.html', {
        'formulario': formulario,
        'opcion': opcion
    })


def eliminar_opcion(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    opcion = get_object_or_404(Opcion, id=id)

    tiene_votos = Voto.objects.filter(opcion=opcion).exists()

    if request.method == 'POST':

        if tiene_votos:
            return render(request, 'confirmar_eliminar_opcion.html', {
                'opcion': opcion,
                'tiene_votos': True
            })

        opcion.delete()
        return redirect('administrar_opciones')

    return render(request, 'confirmar_eliminar_opcion.html', {
        'opcion': opcion,
        'tiene_votos': tiene_votos
    })


def resultados_administrativos(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('inicio')

    ediciones = Edicion.objects.all().order_by('-id')

    edicion_id = request.GET.get('edicion')

    resultados = []
    total_votos = 0

    if edicion_id:

        categorias = Categoria.objects.filter(
            edicion_id=edicion_id
        )

        for categoria in categorias:

            opciones = (
                Opcion.objects
                .filter(categoria=categoria)
                .annotate(total_votos=Count('voto'))
                .order_by('-total_votos')
            )

            votos_categoria = Voto.objects.filter(
                categoria=categoria
            ).count()

            total_votos += votos_categoria

            resultados.append({
                'categoria': categoria,
                'opciones': opciones,
                'total_votos': votos_categoria
            })

    return render(
        request,
        'resultados_administrativos.html',
        {
            'ediciones': ediciones,
            'resultados': resultados,
            'total_votos': total_votos,
            'edicion_id': edicion_id
        }
    )
