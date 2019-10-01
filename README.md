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
