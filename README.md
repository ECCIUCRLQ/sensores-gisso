# Laboratorio inteligente

## Enunciado
En este proyecto, cada grupo de trabajo va a construir un sistema operativo capaz de almacenar de forma 
distribuida información recopilada por sensores. En el contexto de Internet de las Cosas (IoT, por sus siglas en inglés), 
es indispensable que exista una infraestructura capaz de almacenar grandes cantidades de información en tiempo real, 
sin que el usuario tenga que preocuparse por la complejidad subyacente. Típicamente, los sensores se conectan a 
dispositivos pequeños con capacidades limitadas, como son los Arduino o los Raspberry Pi. Esta limitación es la 
que justifica que exista un sistema distribuido.Cada grupo de trabajo recolectará datos usando al menos dos sensores 
diferentes y un Raspberry Pi. El proyecto comenzará tendrá tres fases de alto nivel. Primero, se almacenará la información 
recolectada por los sensores usando un proceso asistente. Luego, los datos se almacenarán en otra computadora. Finalmente, 
los datos se almacenarán en la red.

## Etapa 1

Una vez que cada equipo se hafamiliarizado con el sistema operativo, deberán conectarse los sensores proporcionados al 
Raspberry Pi con el objetivo de obtener datos.En esta fasecada equipo tomará los datos generados por los sensores y los 
enviará a un proceso recolector que se estará ejecutando en un dispositivo diferente(otro Raspberry Pi). Para ello todos 
los equipos deberán diseñar e implementar un mismo protocolo. 

Al final de esta fase se espera que sin importar el sensor que se esté usando, el proceso recolector de cada equipo deberá ser 
compatible con todos los sensores. 

<p align="center">
  <img src="https://imgur.com/Hugfuy2.png"">
</p>

## Etapa 2

En esta fase se espera que además de recolectar los datos generados por los sensores, también sea posible acumularlos datos un tiempo predefinido (recolector con memoria local). Por ejemplo, en esta fase debe ser posible tomar todos los datos de un sensor de temperatura y almacenarlos en un lugar de memoria específico. Para ello, cada equipo deberá implementar un sistema de asignación de memoria basado en el uso de páginas que permita guardarlas temporalmente en memoria. En cada página se almacenarán los datos obtenidos de los sensores, organizados de alguna forma definida por el equipo. Esto implica diseñar un sistema de administración de memoria para asignar dichas páginas. 

Finalmente, se tendrá un graficador que debe poder solicitar todos los datos de un sensor específico y generar un gráfico con dicha información. Para efectos prácticos, el graficador no conoce ni necesita conocer la estrategia de asignación de memoria implementada. 

<p align="center">
  <img src="https://imgur.com/Iz3uyNp.png"">
</p>

## Etapa 3

El objetivo de esta etapa es construir una memoria distribuida para el sistema de recolección de datos de sensores del proyecto. A continuación se describen los requerimientos de esta etapa.

### Swapping: 
Con el objetivo de mantener el servicio siempre listo para atender solicitudes, se contará con dos servicios de localización de páginas: uno activo y otro pasivo. El servicio activo será el que responderá las solicitudes de la interfaz. El servicio pasivo estará disponible para que en caso de que el servicio activo deje de funcionar, el servicio pasivo tomará su lugar y comenzará a responder solicitudes. En cualquier momento un servicio pasivo podrá registrarse para que sirva como soporte en caso de que el activo deje de funcionar.  

### Sistema de archivos:

En cada nodo de datos se contará con un archivo binario (de tamaño a discutir) que simulará ser una unidad de disco. Para implementar este sistema de archivos podrá basarse en cualquier sistema existente, y adaptarlo a las necesidades. De alguna forma, cada equipo deberá organizar las páginas dentro de la unidad. Cualquier estructura de datos, registros, etc. que se necesiten, deberán implementarse localmente en los nodos respectivos.

### Protocolo Memoria Local – Interfaz de memoria Distribuida(ML-ID):
Este protocolo debe permitir que: la memoria local solicite la asignación de una nueva página de memoria, la memoria local soliciteque se guarde una página, y la memoria local se comunica únicamente con una dirección IP conocida.

### Protocolo Interfaz distribuida –Interfaz distribuida(ID-ID):

Este protocolo debe permitir que: la primera interfaz en el sistema se apodere del rol activo en una dirección IP conocida, una interfaz sea elegida como activa cuando varias lo soliciten al mismo tiempo, y una interfaz pasiva asuma el rol activo cuando la activa no dé señal de vida por más de 10 segundos.

### Protocolo Interfaz distribuida-Nodo de memoria (ID-NM):

Este protocolo debe permitir que: un nodo de memoria comunique que quiere participar como almacenador de datos, la interfaz distribuida almacene una página de memoria en un nodo, y la interfaz de memoria recupere una página de memoria en un nodo.

<p align="center">
  <img src="https://imgur.com/jhDLah7.png"">
</p>





### Recursos

* [Raspberry Pi](https://es.wikipedia.org/wiki/Raspberry_Pi).

* [Sensor de movimiento HC-SR501](https://puntoflotante.net/MANUAL-DEL-USUARIO-SENSOR-DE-MOVIMIENTO-PIR-HC-SR501.pdf).

* [Sensor de Shock KY-002](http://robots-argentina.com.ar/didactica/modulo-detector-de-vibracion-ky-002-kit-de-sensores-keyes-2/).

* [Python](https://www.python.org/).

### Sobre este proyecto

Este es un trabajo para el curso de Proyecto Integrador de Redes – Oper de la Universidad de Costa Rica, impartido por 
los profesores Luis Quesada y Adrián Lara.

* Iván Chavarría ivan.chavarriavega@ucr.ac.cr.

* Gerald Bermúdez gerald.bermudez@ucr.ac.cr

* Steff Fernández steff.fernandez@ucr.ac.cr

* Sebastián Otárola sebastian.otarola@ucr.ac.cr
