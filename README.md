# App-Web-Gestion-Clientes-y-Proveedores
Proyecto Final Python TokioSchool.

<br>
<h2>Introduccion</h2>
Este es un proyecto de Aplicacion web basada en la gestion de clientes y proveedores. Para la realizacion del proyecto se ha empleado el framework Flask de Python.

Se trata de una web con conexion a una base de datos SQLite3, que nos proporciona datos necesarios para: el funcionamiento del CRUD de administrador,
carrito de compras, registro de usuarios, almacenamiento de productos...

Al acceder a la web, se nos abrira un formulario de inicio de sesion. El inicio de sesion queda protegido al almacenar la contraseña proporcionada para el registro como un hash en la Base de Datos. En el caso de no estar registrados, se da la opcion de registro. Es importante señalar que esto es posible en tres roles diferentes: Cliente, Proveedor y Administrador.


<br>
<br>
<br>
<h2>Cliente</h2>
Es el perfil basico de nuestra web. En la pagina principal podemos ver una barra de navegacion para poder buscar entre los distintos productos.
A su vez, tenemos un grafico con el historial de las compras realizadas, para poder ver un balance de gastos; y un carrito de la compra para comprar
los productos que almacenemos en el mismo (destacar que el carrito no es funcional, no tiene pasarela de pago. Simplemente se realiza la compra y se disminuye el stock de los productos que haya en el carrito y este queda vacio.)


<h2>Proveedor</h2>
Es el perfil de nuestra web dedicado al usuario con rol de 'reponedor'. 
En la pagina principal, nos aparecera una seccion con los pedidos que nos ha realizado el administrador. Si accedemos, nos caragara una especie de carrito con todos los productos solicitados, y se nos dara informacion del importe totla de produccion de dichos productos.

Por su parte, tambien es posible buscar y enviar stock de cada producto de manera individual, seleccionando el numero de unidades que deseamos enviar al momento de realizar la consulta.

<h2>Administrador</h2>
Es el perfil de nuestra pagina web que se encarga de controlar la misma.
En la pagina principal, se nos permitira acceder a un CRUD de los articulos que tenemos disponibles, para modificar cualquier informacion del mismo A EXCEPCION  de la columna Stock. Para modificar el valor Stock, se debera realizar una peticion al proveedor, seleccionando el numero de unidades que deseamos añadir.

Por otro lado, tambien tenemos a nuestra disposicion dos graficas que nos permitiran analizar de una manera mas grafica el total de ingresos (ganancias de los pedidos de clientes) y perdidas (costes de solicitud y compra al proveedor).


