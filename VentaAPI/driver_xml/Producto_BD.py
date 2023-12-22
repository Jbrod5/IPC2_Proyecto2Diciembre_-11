import xml.etree.ElementTree as ET
from modelos.Producto import Producto
#from lista.Lista import Lista
import os.path as path


class Producto_BD:
    
    def __init__(self):
        self.ruta = "./PRODUCTO_BD.xml"
        if not path.exists(self.ruta):
            try:
                root = ET.Element("PRODUCTO_BD")
                tree = ET.ElementTree(root)
                tree.write(self.ruta)
                print(f"El archivo se ha creado correctamente.")
            except IOError:
                print(f"No se pudo crear el archivo.")
        else:
            print(f"El archivo {self.ruta} ya existe.")
       
    # Recibe de Parametro un Producto Nuevo para su verificación si no existe lo crea y retorna True, caso contrario retorna False 
    def verificarProductoNuevo(self, productoAIngresar: Producto):

        if path.exists(self.ruta):
                            
            producto_actual = self.obtenerProductoEspecifico(productoAIngresar.obtener_codigo())
            
            if producto_actual is not None:
                print("Ya hay un Producto Ingresado con ese codigo")
                return False
            else:
                self.ingresarProductoNuevo(productoAIngresar)
                return True
        else:
            self.ingresarProductoNuevo(productoAIngresar)
            return True
        
    # (DE USO EXCLUSIVO DE ESTA CLASE) Se invoca este metodo en caso el Producto no este Registrado en el XML
    def ingresarProductoNuevo(self, productoAIngresar: Producto):
                
        try:
            tree = ET.parse(self.ruta)
            root = tree.getroot()
        except FileNotFoundError:
            root = ET.Element("PRODUCTO_BD")
            tree = ET.ElementTree(root)
            
        # Verificar que los atributos del producto sean strings
        if isinstance (productoAIngresar.obtener_codigo(), int):
            productoAIngresar.establecer_codigo( str(productoAIngresar.obtener_codigo()))

        if isinstance(productoAIngresar.obtener_precio(), int):
            productoAIngresar.establecer_precio( str(productoAIngresar.obtener_precio()))
        
        if isinstance(productoAIngresar.obtener_stock(), int):
            productoAIngresar.establecer_stock( str(productoAIngresar.obtener_stock()))

        producto_elemento = ET.SubElement(root, "PRODUCTO", ID=productoAIngresar.obtener_codigo())
        ET.SubElement(producto_elemento, "CODIGO").text = productoAIngresar.obtener_codigo()
        ET.SubElement(producto_elemento, "NOMBRE").text = productoAIngresar.obtener_nombre()
        ET.SubElement(producto_elemento, "DESCRIPCION").text = productoAIngresar.obtener_descripion()
        ET.SubElement(producto_elemento, "PRECIO").text = productoAIngresar.obtener_precio()
        ET.SubElement(producto_elemento, "STOCK").text = productoAIngresar.obtener_stock()
        tree.write(self.ruta)
        
    # Obtiene todos los Productos del Archivo XML, en caso el archivo no exista retorna None    
    def obtenerTodosLosProductos(self):

        if path.exists(self.ruta):
            try:
                xml_file = open(self.ruta)
                
                if xml_file.readable():
                    listaProductos = []
                    xml_data = ET.fromstring(xml_file.read())
                    listaArchivo = xml_data.findall('PRODUCTO')
                    
                    for cliente in listaArchivo:
                        codigo = cliente.find('CODIGO').text
                        nombre = cliente.find('NOMBRE').text
                        descripcion = cliente.find('DESCRIPCION').text
                        precio = cliente.find('PRECIO').text
                        stock = cliente.find('STOCK').text
                        
                        producto = Producto(codigo, nombre, descripcion, precio, stock)
                        listaProductos.append(producto)
                        
                    return listaProductos
                
            except FileNotFoundError as err:
                print("Error: ", err)
            except  Exception as err:
                print("Error: ", err)

            finally:
                xml_file.close()
        return None
    
    # Obtiene un Producto en especifico localizado por medio del Codigo, en caso no haya concidencia o este vacia retorna None
    def obtenerProductoEspecifico(self, codigoProducto: int):
        listaProductos = self.obtenerTodosLosProductos()
        
        if listaProductos is not None:
            for i in range(len(listaProductos)):
                #producto_actual = listaProductos.obtenerContenido(i + 1).obtenerElementoNodo()
                producto_actual = listaProductos[i]
                if codigoProducto == producto_actual.obtener_codigo():
                    return producto_actual
        return None
    
    # Elimina un Producto en base a su Codigo y retorna True, caso contrario retorna False     
    def eliminarProducto(self, codigoProducto: int):
        
        if path.exists(self.ruta):
            try:
                tree = ET.parse(self.ruta)
                root = tree.getroot()
                
                for producto in root.findall('PRODUCTO'):
                    id = producto.get('ID')
                    
                    if int(id) == codigoProducto:
                        root.remove(producto)
                tree.write(self.ruta)
                return True
            except FileNotFoundError:
                root = ET.Element("PRODUCTO_BD")
                tree = ET.ElementTree(root)
        return False
    
    # Elimina un Proucto en base a su Codigo y retorna True, caso contrario retorna False     
    def actualizarProducto(self, codigoProducto: int, etiqueta, dato):
        
        if path.exists(self.ruta):
            try:
                tree = ET.parse(self.ruta)
                root = tree.getroot()
                
                productoEspecifico = self.obtenerProductoEspecifico(codigoProducto)
                cliente_existente = root.find(f"./PRODUCTO[@ID='{productoEspecifico.obtener_codigo()}'][CODIGO='{codigoProducto}']")
                cliente_existente.find(etiqueta).text = dato       
                tree.write(self.ruta)
                return True
            except FileNotFoundError:
                root = ET.Element("PRODUCTO_BD")
                tree = ET.ElementTree(root)
        return False