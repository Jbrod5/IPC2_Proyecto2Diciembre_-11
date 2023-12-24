from django.shortcuts import render

from django.http import HttpResponse,JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Cliente_Controller
from .models import Producto_Controller

from django.http import QueryDict

from modelos.Cliente import Cliente
from modelos.Producto import Producto

# Create your views here.

# CLIENTES ------------------------------------------------------------------------------------------------
@csrf_exempt
def obtener_clientes(request):

    controller = Cliente_Controller()

    clientes = controller.obtener_todos()
    response =  JsonResponse(clientes, safe = False)
    response["Access-Control-Allow-Origin"] = "*"
    return response

@csrf_exempt
def obtener_cliente(request, nit):
    controller = Cliente_Controller()
    cliente_json = controller.obtener_cliente(nit)
    return JsonResponse(cliente_json, safe = False)

# POST
@csrf_exempt
def ingresar_cliente(request):
    if request.method == 'POST':

        controller = Cliente_Controller()

        nit = request.POST['nit']
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']

        cliente = Cliente(nit, nombre, direccion)
        controller.ingresar_cliente_nuevo(cliente)
        return HttpResponse("Cliente ingresado correctamente!")

@csrf_exempt
def eliminar_cliente(request):
    if request.method == 'DELETE':
        controller = Cliente_Controller()

        data = QueryDict(request.body)
        nit = data.get('nit')
        controller.eliminar(nit)
        return HttpResponse("Cliente eliminado correctamente")

@csrf_exempt
def actualizar_cliente(request):
    if request.method == 'PATCH':
        controller = Cliente_Controller()

        data = QueryDict(request.body)
        nit = data.get('nit')
        nombre = data.get('nombre')
        direccion = data.get('direccion')

        cliente = Cliente(nit, nombre, direccion)
        controller.actualizar(cliente)
        return HttpResponse("Cliente actualizado correctamente")
        

# PRODUCTOS ----------------------------------------------------------------------------------------------

@csrf_exempt
def obtener_productos(request):
    controller = Producto_Controller()

    productos = controller.obtener_todos()
    return JsonResponse(productos, safe=False)

@csrf_exempt
def obtener_producto(request, codigo):
    controller = Producto_Controller()
    producto_json = controller.obtener_producto(codigo)
    return JsonResponse(producto_json, safe = False)

# POST
@csrf_exempt
def ingresar_producto(request):
    if request.method == 'POST':

        controller = Producto_Controller()

        codigo = request.POST['codigo']        
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        stock = request.POST['stock']

        producto = Producto(codigo, nombre, descripcion, precio, stock)
        controller.ingresar_producto_nuevo(producto)
        return HttpResponse("Producto ingresado correctamente!")
    
@csrf_exempt
def eliminar_producto(request):
    if request.method == 'DELETE':
        control = Producto_Controller()

        data = QueryDict(request.body)
        codigo_producto = data.get('codigo_producto')

        eliminado = control.eliminar_producto(codigo_producto)

        if eliminado:
            return HttpResponse("Producto eliminado correctamente!")
        else:
            return HttpResponse("Fallo al eliminar el producto")

@csrf_exempt
def actualizar_producto(request):
    if request.method == 'PATCH':
        control = Producto_Controller()

        data = QueryDict(request.body)
        codigo_producto = data.get('codigo_producto')
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        precio = data.get('precio')
        stock = data.get('stock')

        actualizar = control.actualizar_producto(codigo_producto, nombre, descripcion, precio, stock)

        if actualizar:
            return HttpResponse('Producto actualizado exitosamente!')
        else:
            return HttpResponse('No se pudo actualizar el producto')