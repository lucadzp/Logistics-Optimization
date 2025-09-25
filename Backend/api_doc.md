# Documentación - API

# Aplicacion ResourceManagement

## Introducción

`ResourceManagement` es una aplicación desarrollada como parte de un sistema más grande, diseñada para gestionar eficientemente datos relacionados con la logística y la distribución. Esta aplicación específicamente manejará los modelos de datos para Depósitos, Vehículos, Demanda y Puntos de Entrega, facilitando así la optimización y coordinación de rutas y recursos dentro de un entorno empresarial.

## Propósito

El propósito de `ResourceManagement` es ofrecer una solución robusta para la administración de recursos esenciales en la logística de distribución. La aplicación permitirá a los usuarios crear, modificar, eliminar y consultar información relevante sobre los recursos gestionados, asegurando que los datos sean accesibles y manejables a través de una interfaz API clara y bien definida.


## ModelViewSet

Utilizaremos `ModelViewSet` de Django REST Framework, que nos permite crear un conjunto completo de operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para nuestros modelos de manera muy eficiente. Esto reduce la cantidad de código necesario para implementar la funcionalidad básica, manteniendo el código limpio y fácil de entender.

## Rutas

Las rutas estarán definidas utilizando el enrutador predeterminado de DRF, que facilita la conexión entre las URLs y nuestros `ViewSets`. Esto permite una configuración clara y sencilla de las rutas API, asegurando que cada acción en los modelos de `Depósito`, `Vehículo`, `Demanda` y `Punto de Entrega` sea accesible a través de métodos HTTP estándares.


# Uso de Serializadores en ResourceManagement

## Introducción a los Serializadores en Django

Los serializadores en Django son una herramienta fundamental para manejar la conversión de datos complejos, como objetos de modelos de base de datos, en tipos de datos nativos de Python que pueden ser fácilmente representados en formatos como JSON, XML, etc. Además, los serializadores también proporcionan funciones de deserialización, lo que permite que los datos analizados se conviertan de nuevo en objetos complejos después de validar los datos entrantes.

## Propósito de los Serializadores

Los serializadores cumplen varios propósitos importantes en el desarrollo de aplicaciones web:

Facilitar la Representación de Datos: Los serializadores permiten convertir objetos de modelos de Django en formatos que pueden ser transmitidos a través de la red y consumidos por aplicaciones cliente. Esto facilita la comunicación entre el backend y el frontend de la aplicación.

Validación de Datos Entrantes: Antes de guardar datos en la base de datos, es crucial validar que los datos entrantes sean correctos y cumplan con los requisitos del modelo. Los serializadores en Django proporcionan herramientas para validar los datos antes de que sean procesados y almacenados.

Desacoplamiento entre la Representación y el Modelo de Datos: Los serializadores permiten definir cómo se representan los datos en la API sin afectar directamente a la estructura del modelo de datos subyacente. Esto facilita la evolución y el mantenimiento de la API a medida que cambian los requisitos de la aplicación.

## Utilizando Serializadores en Django

En el contexto de la aplicación ResourceManagement, utilizaremos serializadores para convertir objetos de modelos de Django, como Deposito, Vehiculo, Demanda y Punto de Entrega, en representaciones legibles y manipulables en formato JSON u otros formatos compatibles con la web. Además, los serializadores permitirán validar y procesar los datos entrantes antes de almacenarlos en la base de datos.

A continuación, en la documentación, detallaremos cómo definir y utilizar serializadores para cada uno de los modelos de datos en la aplicación, describiendo cómo especificar los campos que se deben incluir en la representación, cómo validar los datos entrantes y cómo integrar los serializadores en las vistas de la API para interactuar con los clientes de manera eficiente y segura.


## Estructura de Directorios y Archivos

Para organizar de manera efectiva los componentes de nuestra API RESTful dentro de la aplicación ResourceManagement, vamos a crear un subdirectorio específico. Este enfoque nos ayudará a mantener una estructura clara y modular, facilitando así el mantenimiento y la escalabilidad del proyecto.

### Creación del directorio api_resourcemanagement

Dentro de la aplicación ResourceManagement, creamos un subdirectorio llamado api_resourcemanagement. Este directorio contendrá todos los archivos y módulos necesarios para gestionar las interacciones de la API RESTful.

        ResourceManagement/
        │
        ├── api_resourcemanagement/
        │   ├── __init__.py
        │   ├── serializers.py    # Archivo para los serializadores de la API
        │   ├── views.py          # Archivo para las vistas de la API
        │   ├── urls.py           # Archivo para la definición de rutas URL de la API
        │
        ├── models.py             # Modelos de Django utilizados en la aplicación
        ├── admin.py              # Configuración del administrador de Django
        ├── apps.py               # Configuraciones de la aplicación Django


#### Descripción de los componentes

    serializers.py: Contiene los serializadores de Django REST Framework que convierten los modelos de datos en formatos JSON/XML y viceversa. Estos son esenciales para el procesamiento de datos entrantes y salientes en las llamadas API.

    views.py: Define las vistas o controladores que manejan las solicitudes recibidas a la API. Utilizamos viewsets de Django REST Framework para manejar operaciones CRUD típicas de forma más eficiente.

    urls.py: Este archivo contiene las rutas URL específicas que apuntan a las vistas definidas. Ayuda a dirigir las solicitudes entrantes a los controladores apropiados.

#### Ventajas de esta estructura

    Modularidad: Cada componente tiene un propósito claro y está separado, lo que facilita la gestión y el desarrollo independiente de cada parte de la API.
    Escalabilidad: A medida que la aplicación crece y se agregan más recursos o se modifican los existentes, esta estructura permite una expansión fácil sin afectar otros componentes.
    Mantenibilidad: Simplifica la búsqueda de archivos y la resolución de problemas, ya que todo está organizado de manera lógica y coherente.

## Desarrollo de la API RESTful

En este capítulo, describimos el proceso de implementación de la API RESTful para nuestra aplicación ResourceManagement. Se detallarán las técnicas de serialización de datos, cómo configuramos las vistas para gestionar las solicitudes, y la manera en que se definen las rutas para facilitar el acceso a los recursos. Cada componente es vital para la interacción eficiente y efectiva entre el frontend y el backend de nuestra aplicación.

### Serialización de Datos

La serialización es el proceso de convertir los objetos del modelo en formatos que puedan ser fácilmente transmitidos y utilizados en aplicaciones cliente, como JSON. A continuación, se describe la configuración de los serializadores para cada uno de nuestros modelos en el archivo serializers.py:

        from rest_framework import serializers
        from ResourceManagement.models import Deposito, Vehiculo, Demanda, PuntoDeEntrega

        # Serializador para el modelo Deposito
        class DepositoSerializer(serializers.ModelSerializer):
            class Meta:
                model = Deposito  # Especifica el modelo al cual este serializador pertenece
                # Define los campos que se incluirán en la serialización/deserialización
                fields = ['id', 'nombre', 'latitud', 'longitud', 'direccion', 'numero_de_telefono']

        # Serializador para el modelo Vehiculo
        class VehiculoSerializer(serializers.ModelSerializer):
            # Campo relacionado que apunta al modelo Deposito, utilizando su clave primaria
            deposito = serializers.PrimaryKeyRelatedField(queryset=Deposito.objects.all())
            
            class Meta:
                model = Vehiculo
                fields = ['matricula', 'capacidad_de_carga', 'deposito']
                depth = 1  # Proporciona una representación anidada del objeto relacionado hasta 1 nivel de profundidad

        # Serializador para el modelo Demanda
        class DemandaSerializer(serializers.ModelSerializer):
            # Campo relacionado que apunta al modelo Deposito, permite seleccionar un deposito al crear/editar demandas
            deposito = serializers.PrimaryKeyRelatedField(queryset=Deposito.objects.all())
            class Meta:
                model = Demanda
                fields = ['id', 'peso_kg', 'fecha_creada', 'descripción', 'estado', 'deposito']
                depth = 1  # Permite ver detalles del objeto relacionado 'deposito' en el serializado

        # Serializador para el modelo PuntoDeEntrega
        class PuntoDeEntregaSerializer(serializers.ModelSerializer):
            # Campo relacionado que filtra las demandas por estado 'pendiente' para ser seleccionadas
            demanda = serializers.PrimaryKeyRelatedField(queryset=Demanda.objects.filter(estado='pendiente'))
            class Meta:
                model = PuntoDeEntrega
                fields = ['id', 'cliente', 'latitud', 'longitud', 'demanda', 'numero_de_telefono']
                depth = 1  # Muestra una representación anidada de la demanda relacionada


#### Explicacion del codigo 

##### Clase ModelSerializer

La clase base que estamos utilizando para cada serializador es `serializers.ModelSerializer`. Esta clase simplifica la tarea de crear serializadores automatica y convenientemente generar un conjunto de campos y validadores basados en el modelo de datos de Django que proporcionas. Aquí está cómo funciona para cada modelo:
Clases y Modelos

    Class DepositoSerializer: Serializa el modelo Deposito.
    Class VehiculoSerializer: Serializa el modelo Vehiculo.
    Class DemandaSerializer: Serializa el modelo Demanda.
    Class PuntoDeEntregaSerializer: Serializa el modelo PuntoDeEntrega.

###### Meta Clase Interna

Cada serializador define una clase Meta interna. Esta clase Meta es donde especificas configuraciones esenciales del serializador:

    model: El modelo Django al que el serializador está ligado. El serializador utilizará este modelo para determinar qué campos deben ser serializados/deserializados.
    fields: Una lista o tupla de nombres de campos del modelo que deseas incluir en la serialización. Esto determina qué información se incluye en la salida serializada y qué se espera al deserializar datos.
    depth: Este parámetro se usa para controlar cuán profundamente se deben serializar las relaciones; por ejemplo, si tienes un campo que es una clave foránea, depth = 1 significa que también se incluirá información del modelo relacionado a un nivel de profundidad.


## Vistas

En el desarrollo de APIs con Django REST Framework (DRF), las vistas juegan un papel crucial al actuar como el enlace entre los modelos de datos y las representaciones de esos datos que se envían a los usuarios. Las vistas en DRF son responsables de procesar las solicitudes entrantes, interactuar con el modelo de datos según sea necesario y luego devolver una respuesta adecuada al cliente.

DRF proporciona varias clases base para construir vistas, cada una optimizada para diferentes estilos de APIs y requisitos de acceso a datos. Entre las más comunes están APIView, para cuando necesitas un control detallado sobre la lógica de las vistas, y las clases basadas en ViewSet, que simplifican la construcción de interfaces CRUD (Crear, Leer, Actualizar, Eliminar) convencionales a través de un enfoque más declarativo.

En nuestro caso, como habiamos dicho al principio utilizaremos las ViewSet, especificamente el ModelViewSet.

#### ModelViewSet

ModelViewSet es particularmente poderoso porque combina automáticamente los comportamientos de las vistas genéricas para las operaciones de modelo más comunes. Con ModelViewSet, puedes crear rápidamente una interfaz completa para un modelo con una cantidad mínima de código. 

Nos vamos al archivo views.py ubicado en el subdirectorio creado previamente.

    from rest_framework import viewsets
    from ResourceManagement.models import Deposito, Vehiculo, Demanda, PuntoDeEntrega
    from .serializers import DepositoSerializer, VehiculoSerializer, DemandaSerializer, PuntoDeEntregaSerializer

    class DepositoViewSet(viewsets.ModelViewSet):
        queryset = Deposito.objects.all()
        serializer_class = DepositoSerializer
        # Gestiona todas las operaciones CRUD para el modelo Deposito, utilizando el serializador especificado.

    class VehiculoViewSet(viewsets.ModelViewSet):
        queryset = Vehiculo.objects.all()
        serializer_class = VehiculoSerializer
        # Maneja operaciones CRUD para el modelo Vehiculo.

    class DemandaViewSet(viewsets.ModelViewSet):
        queryset = Demanda.objects.all()
        serializer_class = DemandaSerializer
        # Permite realizar operaciones CRUD sobre el modelo Demanda.

    class PuntoDeEntregaViewSet(viewsets.ModelViewSet):
        queryset = PuntoDeEntrega.objects.all()
        serializer_class = PuntoDeEntregaSerializer
        # Proporciona manejo CRUD para PuntoDeEntrega y personaliza la creación para validar estados de demanda.

        def perform_create(self, serializer):
            demanda = serializer.validated_data['demanda']
            
            # Verifica el estado de la demanda antes de permitir la creación del punto de entrega.
            if demanda.estado != 'pendiente':
                raise serializers.ValidationError("La demanda ya está asignada o entregada y no está disponible para un nuevo punto de entrega.")
            
            punto_de_entrega = serializer.save()
            demanda.estado = 'asignada'
            demanda.save()
            # Este método personaliza la creación de un punto de entrega, asegurando que se respeten las reglas de negocio.


Cada ViewSet permite la realización de operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los modelos correspondientes.


##### DepositoViewSet

Clase: DepositoViewSet

Modelo Relacionado: Deposito

Serializador: DepositoSerializer

Descripción:
La clase DepositoViewSet extiende ModelViewSet, proporcionando una interfaz completa para operar con el modelo Deposito. Permite a los usuarios realizar las siguientes operaciones:

Crear Depositos: Se pueden añadir nuevos depósitos especificando atributos como nombre, latitud, longitud, dirección y número de teléfono.
Leer Depositos: Permite la consulta de todos los depósitos existentes o detalles de un depósito específico.
Actualizar Depositos: Los detalles de un depósito existente pueden ser modificados.
Eliminar Depositos: Se puede eliminar un depósito existente.

##### VehiculoViewSet

Clase: VehiculoViewSet

Modelo Relacionado: Vehiculo

Serializador: VehiculoSerializer

Descripción:
VehiculoViewSet ofrece una interfaz CRUD para el modelo Vehiculo, facilitando la gestión de vehículos dentro del sistema. Las operaciones incluyen:

Crear Vehículos: Permite añadir vehículos al sistema, incluyendo detalles como matrícula, capacidad de carga y el depósito asociado.
Leer Vehículos: Los usuarios pueden listar todos los vehículos o ver detalles específicos de un vehículo.
Actualizar Vehículos: Modificación de los datos de un vehículo existente.
Eliminar Vehículos: Eliminación de registros de vehículos.

##### DemandaViewSet

Clase: DemandaViewSet

Modelo Relacionado: Demanda

Serializador: DemandaSerializer

Descripción:
La clase DemandaViewSet gestiona el modelo Demanda, permitiendo operaciones como:

Crear Demandas: Se pueden registrar nuevas demandas, incluyendo información como peso, descripción, estado, y el depósito relacionado.
Leer Demandas: Posibilita la visualización de todas las demandas o los detalles de una demanda específica.
Actualizar Demandas: Permite actualizar la información de demandas existentes.
Eliminar Demandas: Facilita la eliminación de demandas.

##### PuntoDeEntregaViewSet

Clase: PuntoDeEntregaViewSet

Modelo Relacionado: PuntoDeEntrega

Serializador: PuntoDeEntregaSerializer

Descripción:
PuntoDeEntregaViewSet administra el modelo PuntoDeEntrega e incluye una lógica personalizada en la creación de puntos de entrega para asegurar la integridad del proceso:

Crear Puntos de Entrega: Los usuarios pueden crear nuevos puntos de entrega si la demanda asociada está en estado 'pendiente'. Si la demanda está en otro estado, se lanzará un error.
Leer Puntos de Entrega: Permite consultar todos los puntos de entrega o un punto específico.
Actualizar Puntos de Entrega: Los usuarios pueden modificar los detalles de un punto de entrega existente.
Eliminar Puntos de Entrega: Permite la eliminación de puntos de entrega del sistema.

Cada ViewSet está diseñado para facilitar la interacción con el modelo respectivo de manera eficiente y segura, asegurando que las operaciones de la base de datos se realicen conforme a las reglas del negocio establecidas.


#### Explicacion del funcionamiento de las vistas

Cada ViewSet en Django REST Framework funciona como un controlador que maneja las operaciones HTTP sobre los recursos de la aplicación. Los ViewSets están diseñados para simplificar la lógica detrás del manejo de los modelos y reducir la cantidad de código necesario para crear interfaces API completas. Aquí detallamos cómo se procesan las solicitudes y qué se devuelve:
Flujo General de Operaciones en ViewSets

    Recepción de Datos:
        Cuando un cliente realiza una solicitud (POST, GET, PUT, DELETE, etc.), Django REST Framework recibe los datos en formato JSON (o otro formato soportado, dependiendo de los parsers configurados).

    Deserialización:
        Los datos recibidos son deserializados utilizando el serializer correspondiente. Esto significa que los datos en formato JSON son convertidos a estructuras de datos de Python que Django puede entender y validar según las reglas establecidas en el serializer.

    Procesamiento de Datos:
        Dependiendo del tipo de solicitud, se realiza una operación CRUD sobre el modelo asociado. Por ejemplo, en una solicitud POST, los datos deserializados son utilizados para crear un nuevo registro en la base de datos.

    Serialización:
        Para las solicitudes que devuelven datos (principalmente GET, pero también PUT y POST si se retorna el objeto modificado), los modelos de Django son convertidos de nuevo a JSON mediante el proceso de serialización. El serializer toma los datos del modelo y los transforma en JSON para ser enviados de vuelta al cliente.

    Respuesta:
        La API envía una respuesta al cliente, que incluye los datos serializados en JSON y los códigos de estado HTTP adecuados para indicar el éxito o fallo de la operación.

Descripción Detallada por ViewSet
DepositoViewSet

    Recibe: JSON con datos de depósitos para crear o actualizar registros.
    Devuelve: JSON con datos de los depósitos en las operaciones de lectura o tras crear/actualizar un depósito.

VehiculoViewSet

    Recibe: JSON con datos de vehículos para nuevas adiciones o actualizaciones.
    Devuelve: JSON que representa los vehículos en respuesta a solicitudes de consulta o tras modificaciones.

DemandaViewSet

    Recibe: JSON con información de demandas para registrar o actualizar.
    Devuelve: JSON con información detallada de demandas en operaciones de lectura o después de realizar cambios.

PuntoDeEntregaViewSet

    Recibe: JSON con detalles de nuevos puntos de entrega, considerando validaciones especiales como el estado de la demanda asociada.
    Devuelve: JSON con detalles de los puntos de entrega en respuestas a consultas o tras crear/modificar puntos.

Cada uno de estos ViewSets utiliza la configuración de serializadores para garantizar que los datos son correctamente validados antes de su procesamiento y adecuadamente formateados al ser enviados como respuesta, proporcionando una interfaz robusta y flexible para trabajar con la API.


### Rutas

Las rutas en Django REST Framework son esenciales para definir cómo se accede a los recursos a través de la API. Estas rutas son las URLs que los clientes utilizarán para interactuar con la aplicación, permitiendo realizar operaciones CRUD sobre los modelos a través de los ViewSets que hemos definido. Veamos cómo configurar estas rutas usando routers que simplifican este proceso de mapeo.

En el archivo urls.py creado en el subdirectorio previamente, y mencionado al principio.

        from django.urls import include, path
        from rest_framework.routers import DefaultRouter
        from .views import DepositoViewSet, VehiculoViewSet, DemandaViewSet, PuntoDeEntregaViewSet


        router = DefaultRouter()
        router.register(r'depositos', DepositoViewSet)
        router.register(r'vehiculos', VehiculoViewSet)
        router.register(r'demandas', DemandaViewSet)
        router.register(r'puntosdeentrega', PuntoDeEntregaViewSet)


        urlpatterns = [
            path('', include(router.urls)),  # Incluye todas las rutas del router en la raíz de la aplicación
        ]


##### Uso de DefaultRouter

El DefaultRouter de Django REST Framework es una herramienta muy poderosa que automáticamente genera rutas para todas las acciones estándar en un ViewSet. Estas acciones incluyen operaciones CRUD (create, read, update, delete) y también manejan la singularización/pluralización de los nombres de los recursos automáticamente, proporcionando un estilo coherente para tus URLs.
Pasos para Configurar las Rutas

    Importar Dependencias:
        Importamos DefaultRouter de rest_framework.routers que nos ayudará a crear un router que maneje nuestras rutas de forma automática.
        Importamos path y include de django.urls para definir las URLs de la aplicación.
        Importamos los ViewSets desde views.py que ya han sido definidos.

    Crear una Instancia de DefaultRouter:
        Creamos una instancia de DefaultRouter. Este objeto es el que registrará nuestras rutas.

    Registrar ViewSets con el Router:
        Usamos el método register() del router para conectar cada ViewSet con un prefijo de ruta específico:
            r'depositos' para DepositoViewSet
            r'vehiculos' para VehiculoViewSet
            r'demandas' para DemandaViewSet
            r'puntosdeentrega' para PuntoDeEntregaViewSet
        El primer argumento del método register() es el prefijo de la ruta (parte de la URL), y el segundo argumento es el ViewSet correspondiente. Esto dirá al router cómo responder a las solicitudes a esas rutas.

    Definir las URL Patterns:
        Las urlpatterns son una lista de rutas que Django usará para recibir y dirigir las solicitudes entrantes.
        Usamos path() con una cadena vacía como primer argumento y include(router.urls) como segundo. Esto incluye todas las rutas generadas por el router en la URL raíz de la aplicación. Es decir, todas las rutas registradas en el router serán accesibles desde la raíz del sitio.

##### ¿Qué Hace Cada Registro?

    router.register(r'depositos', DepositoViewSet): Registra las rutas para operaciones CRUD en el modelo Deposito. Esto incluye rutas para listar depósitos (GET), crear un nuevo depósito (POST), obtener detalles de un depósito específico (GET con ID), actualizar (PUT/PATCH) y eliminar (DELETE) depósitos.

    router.register(r'vehiculos', VehiculoViewSet): Similar al anterior pero para el modelo Vehiculo.

    router.register(r'demandas', DemandaViewSet) y router.register(r'puntosdeentrega', PuntoDeEntregaViewSet): Funcionan de manera idéntica, registrando las rutas necesarias para manejar las demandas y los puntos de entrega respectivamente.


# Aplicacion Optimizer

## Introduccion

"Optimizer" emplea algoritmos avanzados de optimización para determinar la secuencia óptima de entrega y la distribución de cargas entre varios vehículos. La aplicación cuenta con dos modelos de datos principales, Rutas de Entrega y Detalle de Ruta de Entrega, que trabajan conjuntamente para registrar y gestionar las rutas optimizadas.
Modelos de Datos

Rutas de Entrega
    Descripción: Este modelo almacena la información general de cada ruta de optimización realizada. Incluye detalles como la distancia total recorrida, que es la suma de las distancias de todos los puntos en la ruta optimizada.
    Campos Principales:
        ruta_id: Identificador único de cada ruta.
        fecha_creacion: Fecha y hora en la que se creó la ruta.
        distancia_total_recorrida: Distancia total que el vehículo recorre durante la entrega, medida en kilómetros.

    Cada registro en este modelo representa una ruta completa planificada para uno o más vehículos, integrando todas las entregas asignadas a esa ruta en particular.

Detalle Ruta de Entrega
    Descripción: Este modelo detalla cada segmento individual de la ruta, especificando qué vehículo entregará qué demanda en qué punto de entrega y en qué orden.
    
    Campos Principales:
        ruta: Llave foránea que enlaza con el modelo Rutas de Entrega.
        punto_de_entrega: Llave foránea que refiere a los puntos específicos de entrega dentro de la ruta.
        orden_de_entrega: Secuencia numérica que indica el orden en el que los puntos de entrega deben ser visitados.
        distancia_recorrida_al_punto: Distancia recorrida desde el punto anterior al punto actual.
        demanda_a_entregar: Cantidad de producto o servicio que debe ser entregado en ese punto.

    El propósito de este modelo es proporcionar un desglose detallado de cada ruta, permitiendo una trazabilidad precisa y la posibilidad de ajustar o reevaluar segmentos específicos de la ruta si fuera necesario.


### Estructura de Directorios y Archivos para la Aplicación Optimizer

Para manejar eficientemente la logística y optimización de rutas en nuestra aplicación Optimizer, estructuraremos nuestro proyecto de manera que facilite la claridad, mantenimiento y escalabilidad. Este enfoque modular nos ayudará a organizar los componentes de la API RESTful de forma intuitiva.
Creación del Directorio api_optimizer

Dentro de la aplicación Optimizer, crearemos un subdirectorio llamado api_optimizer. Este directorio albergará todos los archivos y módulos necesarios para gestionar las interacciones de la API RESTful que interactúan con los modelos de rutas y detalles de rutas de entrega.

    Optimizer/
    │
    ├── api_optimizer/
    │   ├── __init__.py
    │   ├── serializers.py    # Archivo para los serializadores de la API
    │   ├── views.py          # Archivo para las vistas de la API
    │   ├── urls.py           # Archivo para la definición de rutas URL de la API
    │
    ├── models.py             # Modelos de Django utilizados en la aplicación
    ├── admin.py              # Configuración del administrador de Django
    ├── apps.py               # Configuraciones de la aplicación Django



#### Descripción de los Componentes

serializers.py: Aquí se definen los serializadores de Django REST Framework que convierten los modelos de datos (Rutas de Entrega y Detalle Ruta de Entrega) en formatos JSON/XML y viceversa, facilitando el procesamiento de los datos de entrada y salida en las llamadas API.

views.py: Este archivo contiene las vistas o controladores que manejan las solicitudes recibidas por la API. Utilizaremos viewsets de Django REST Framework para administrar operaciones CRUD de manera eficiente sobre los modelos de datos.

urls.py: Contiene las rutas URL específicas que apuntan a las vistas definidas. Este archivo es crucial para dirigir las solicitudes entrantes hacia los controladores apropiados, asegurando una correcta interacción con la API.


#### Ventajas de esta Estructura

Modularidad: Cada componente de la API tiene un propósito bien definido y está separado del resto, lo que facilita su gestión y desarrollo de manera independiente.

Escalabilidad: A medida que la aplicación crece y se añaden nuevas funcionalidades o se modifican las existentes, esta estructura permite una expansión ordenada y lógica.

Mantenibilidad: La organización clara y coherente de los archivos simplifica tanto la búsqueda como la resolución de problemas, permitiendo un mantenimiento más sencillo y directo.


#### Desarrollo de la API RESTful para Optimizer

En este segmento, describiremos el proceso de implementación de la API RESTful para nuestra aplicación Optimizer. Detallaremos cómo se configuran los serializadores para manejar los modelos de datos, las vistas para procesar solicitudes y las rutas para acceder a los servicios. Este diseño contribuye a una interacción eficaz y fluida entre el frontend y el backend de la aplicación, optimizando la logística de entregas de manera significativa.

### Serialización de Datos

        from rest_framework import serializers
        from .models import RutasDeEntrega, DetalleRutaDeEntrega
        from ResourceManagement.serializers import PuntoDeEntregaSerializer

        class RutasDeEntregaSerializer(serializers.ModelSerializer):
            class Meta:
                model = RutasDeEntrega
                fields = ['ruta_id', 'fecha_creacion', 'distancia_total_recorrida']

        class DetalleRutaDeEntregaSerializer(serializers.ModelSerializer):
            ruta = serializers.PrimaryKeyRelatedField(read_only=True)
            punto_de_entrega = PuntoDeEntregaSerializer(read_only=True)

            class Meta:
                model = DetalleRutaDeEntrega
                fields = [
                    'ruta',
                    'punto_de_entrega',
                    'orden_de_entrega',
                    'distancia_recorrida_al_punto',
                    'demanda_a_entregar'
                ]


Explicación del Código:

RutasDeEntregaSerializer:
    Este serializador maneja la serialización de los datos para el modelo RutasDeEntrega.
    Se incluyen campos básicos como el identificador de la ruta (ruta_id), la fecha de creación (fecha_creacion), y la distancia total recorrida (distancia_total_recorrida).

DetalleRutaDeEntregaSerializer:
    Este serializador se encarga de serializar los detalles de cada punto en una ruta de entrega.
    ruta: Se utiliza un campo PrimaryKeyRelatedField para representar la relación con el modelo RutasDeEntrega. Este campo es sólo de lectura porque normalmente la ruta estaría preestablecida y no cambiante a través de esta interfaz.
    punto_de_entrega: Aquí se utiliza el PuntoDeEntregaSerializer importado para incluir detalles completos del punto de entrega en la serialización. Este también es un campo de sólo lectura, ideal para evitar cambios en este punto a través de este endpoint.
    orden_de_entrega, distancia_recorrida_al_punto, y demanda_a_entregar son campos directos del modelo que se incluyen en la serialización.


## Vistas

archivo views.py

        from rest_framework import viewsets, mixins
        from Optimizer.models import RutasDeEntrega, DetalleRutaDeEntrega
        from .serializers import RutasDeEntregaSerializer, DetalleRutaDeEntregaSerializer

        class RutasDeEntregaViewSet(mixins.ListModelMixin, 
                                    mixins.RetrieveModelMixin, 
                                    viewsets.GenericViewSet):
            queryset = RutasDeEntrega.objects.all()
            serializer_class = RutasDeEntregaSerializer

        class DetalleRutaDeEntregaViewSet(mixins.ListModelMixin, 
                                        mixins.RetrieveModelMixin, 
                                        viewsets.GenericViewSet):
            queryset = DetalleRutaDeEntrega.objects.all()
            serializer_class = DetalleRutaDeEntregaSerializer


Se importan las clases necesarias de Django Rest Framework (DRF) para definir viewsets y mixins.
Se importan los modelos RutasDeEntrega y DetalleRutaDeEntrega, así como los serializadores asociados.
Se define la clase RutasDeEntregaViewSet, que es un viewset que hereda de mixins.ListModelMixin, mixins.RetrieveModelMixin, y viewsets.GenericViewSet.
Este viewset maneja las operaciones de listar y recuperar para el modelo RutasDeEntrega.
Se especifica el queryset para obtener todas las instancias de RutasDeEntrega.
Se especifica el serializador a utilizar para serializar los datos del modelo.
Se define la clase DetalleRutaDeEntregaViewSet, que es similar al RutasDeEntregaViewSet.
Este viewset maneja las operaciones de listar y recuperar para el modelo DetalleRutaDeEntrega.
Se especifica el queryset para obtener todas las instancias de DetalleRutaDeEntrega.
Se especifica el serializador a utilizar para serializar los datos del modelo.

Estos viewsets proporcionan endpoints RESTful para interactuar con los modelos RutasDeEntrega y DetalleRutaDeEntrega, permitiendo realizar operaciones de listado y recuperación de datos a través de la API. 


## Routes

archivo urls.py

    from rest_framework.routers import DefaultRouter
    from django.urls import path, include
    from .views import RutasDeEntregaViewSet, DetalleRutaDeEntregaViewSet

    app_name = 'Optimizer'

    router = DefaultRouter()
    router.register(r'rutas', RutasDeEntregaViewSet)
    router.register(r'detalles', DetalleRutaDeEntregaViewSet)

    urlpatterns = [
        path('', include(router.urls)),
    ]

Importaciones de módulos necesarios:

    from rest_framework.routers import DefaultRouter
    from django.urls import path, include
    from .views import RutasDeEntregaViewSet, DetalleRutaDeEntregaViewSet

Se importa DefaultRouter del módulo rest_framework.routers. Este enrutador es útil para generar automáticamente las URL para los viewsets.
Se importa path e include del módulo django.urls. Estos son necesarios para definir las rutas de URL de Django.
Se importan los viewsets RutasDeEntregaViewSet y DetalleRutaDeEntregaViewSet desde el archivo de vistas local (views.py).

Definición del nombre de la aplicación:

    app_name = 'Optimizer'

Se establece el nombre de la aplicación como 'Optimizer'. Esto es útil para organizar y distinguir las URL de esta aplicación dentro de Django.

Configuración del enrutador:


    router = DefaultRouter()
    router.register(r'rutas', RutasDeEntregaViewSet)
    router.register(r'detalles', DetalleRutaDeEntregaViewSet)

Se crea una instancia de DefaultRouter().
Se registran los viewsets RutasDeEntregaViewSet y DetalleRutaDeEntregaViewSet con el enrutador.
Para cada viewset, se especifica una ruta base y el viewset asociado. En este caso, las rutas serán 'rutas/' y 'detalles/', respectivamente.

Definición de las URL:

    urlpatterns = [
        path('', include(router.urls)),
    ]

Se define la variable urlpatterns que contiene la lista de rutas URL para esta aplicación.
Se incluyen las rutas generadas por el enrutador usando include(router.urls). Esto incluye automáticamente las URL generadas por el enrutador para los viewsets registrados.

