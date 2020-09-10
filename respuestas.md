<p align="center">
    <img src="http://cdn.lowgif.com/full/4c0f211082b1edb6-.gif" height="450">
    <h1 align="center">Visualización de datos: Estrella de Norte de Datadog :star:</h1>
  </a>
  <p align="center">Mantén tus ojos en el horizonte</p>
</p>

Construir un negocio exitoso no se trata de subir escaleras o defenderse de la competencia en un espacio en particular; se trata de generar impulso y seguir avanzando. Pasar demasiado tiempo solucionando problemas con su producto no debería alejarlo de su objetivo.

Si siente que está pasando demasiado tiempo solucionando problemas técnicos, ha perdido de vista su horizonte, eso es realmente de lo que estoy aquí para hablar hoy.

La forma de Datadog de mantener lo visual abierto a través de métricas, seguimientos y visualizaciones de registros en una plataforma integrada es la forma más efectiva de mantener el rumbo; recopilar datos de cientos de tecnologías para la resolución de problemas, aprendizaje automático, alertas y más, mantenga su brújula afilada.

No se pierda en un mar de resolución de problemas, mire hacia la estrella del norte para ver la dirección.

Únase a mí y aprenda cómo funciona Datadog, qué ofrece y cómo puede ayudarlo.

### Configuración inteligente
Ya sea que sea un maestro de los sistemas operativos de Microsoft, un Linux Ninja o un asistente de Mac OS; o tener aplicaciones en contenedores para una empresa (mírelo, en serio, ¡eso es un logro!) Datadog lo tiene cubierto.

Regístrese para obtener una cuenta gratuita de Datadog, haga clic en ***Integrations > Agents***, descargue el agente específico de su sistema operativo y prepárese para analizar los datos.

A lo largo de esta guía, usaré un escritorio de desarrollo de Windows 10. He instalado el Agente, ahora puedo acceder al Administrador de agentes de Datadog (o DAM) visitando su ubicación predeterminada http://127.0.0.1:5002, o haciendo doble clic en el icono de Datadog en la barra de tareas.

![WindowsPCDatadogAgent](https://i.imgur.com/ZCVWw2Z.png)

:high_brightness: Pro Tip:
DAM le permite revisar el estado del agente, examinar los registros, revisar la configuración, comunicarse con el soporte mediante Flare y reiniciar el agente después de realizar cualquier cambio de configuración. Muy útil :thumbsup:
### Emocionante Tagging

Como parte de nuestra configuración, queremos usar etiquetas en el archivo de configuración datadog.yaml del agente. Piense en las etiquetas como una forma de agregar dimensiones a las telemetrías de Datadog para que se puedan filtrar, agregar y comparar en visualizaciones de Datadog.

Encontraremos el archivo de configuración del agente (en mi caso particular, usando Windows 10) en C:\ProgramData\Datadog\datadog.yaml

```yaml
...
syslog_key: ""
syslog_pem: ""
syslog_rfc: false
syslog_tls_verify: true
syslog_uri: ""
tag_value_split_separator: {}
tags: [ "env:dev", "os:win10pro", "location:columbia"]
telemetry:
  enabled: true
tracemalloc_blacklist: ""
tracemalloc_debug: false
tracemalloc_whitelist: ""
use_dogstatsd: true 
...
```

Como puede ver arriba, he agregado 3 etiquetas, Entorno (ENV), Sistema operativo (SO) y Ubicación (ubicación). "Columbia" me funciona porque es la calle donde vivo.

:point_up: No olvide reiniciar su agente a través de DAM una vez que haya agregado sus etiquetas al archivo de configuración del agente y vea el nuevo host en la consola de Datadog.

### Astuto conf.d 

Ahora que tenemos el Agente en ejecución, podemos empezar a personalizar nuestro Agente. Para Windows, navegue a ****C:\ProgramData\Datadog\conf.d\**** y encontrará todas las integraciones listas para usar con las que se comunica Datadog. Digamos que desea monitorear Apache, boom open ****apache.d/**** o tal vez una conexión a nagios, ingrese a esa carpeta ****nagios.d/****. El mundo es tu ostra (o al menos tu directorio de integración de Datadog lo es). :smirk:

Cada carpeta tiene un ****conf.yaml.example**** correspondiente para comenzar, copie el archivo de ejemplo y cámbiele el nombre a ****conf.yaml**** en la carpeta de cada integración, edite los valores correspondientes y reinicie su Agente.

¡Siguiente!
   Repasemos algunas integraciones que necesito configurar: smirk:


### Bases de datos Deliciosas

:question: ¿Y si queremos monitorear bases de datos?

Eso es EXACTAMENTE lo que necesitaba configurar a continuación ... Por cierto, Datadog tiene más de 400[supported integrations](https://docs.datadoghq.com/integrations/) and each integration has detailed instructions, I recommend you browse through and see what you can take advantage of

:point_up:Recuerde, asegúrese de editar el archivo de configuración correcto (conf.yaml) como lo he hecho a continuación, en mi caso necesitaba monitorear una base de datos postgreSQL en mi escritorio de Windows 10.

![PostgreSQLConf](https://i.imgur.com/7FuMCKn.png)

Creé el conf.yaml, siguiendo las instrucciones de la página de integración de Datadog. Pan comido. :thumbsup:


## Controles personalizados capaces

:question: ¿Qué pasa si escribe un guión y desea que el resultado se envíe a Datadog? *vamos*!

Siempre que la verificación del script esté escrita en un [supported language] (https://docs.datadoghq.com/developers/libraries/) (piense en Go, NodeJS, Python, etc.), no tendrá ningún problema.
De hecho, he escrito un breve script de Python al que puede hacer referencia a continuación.
Para crear una verificación de agente personalizada, ambos archivos deben tener el mismo nombre y deben crearse de la siguiente manera:

*Archivo de comandos:* (Este archivo esta en C:\ProgramData\Datadog\checks.d\)

Spanish

Este es mi script de Python, nuestro objetivo es obtener aleatoriamente un número entre 0 y 1000. Este número se enviará a Datadog para probar la funcionalidad de verificación personalizada.

```python
import random
    
try:
    from datadog_checks.base import AgentCheck
except ImportError:
    from checks import AgentCheck
        
__version__ = "1.0.0"
    
class cmetric(AgentCheck):
    def check(self, instance):
        self.gauge(
                "cmetric_gauge",
                random.randint(0,1000),
                tags=["cmetric_type:gauge"],
        )
```
    
*Conf file:* (Este archivo esta en  C:\ProgramData\Datadog\conf.d\)

Este es mi archivo de configuración para el script Python, nuestro objetivo es enviar un nuevo número a Datadog cada 45 segundos.

```python
init_config:
instances:
  - min_collection_interval: 45
```

Guardamos ambos archivos, reiniciamos el Agente a través de DAM y revisamos la Consola de Datadog ...:+1:

y...

![CMEtric](https://i.imgur.com/3zE46xt.png)

Muy bien hecho!

:high_brightness: Pro Tip:
¿Sabía que puede cambiar el intervalo de recopilación sin modificar los archivos de verificación de secuencia de comandos que creó?

En la consola de Datadog > ***Metrics > Summary > Selecciona la metrica >*** Under ****Metadata, Edit > Enter new Interval value****

![CMetricIntervalChangethroughConsole](https://i.imgur.com/ivXVdPB.png)



## Oh DAM

Suponiendo que no has reiniciado DAM, echemos un vistazo a cómo se vería DAM si todo lo que hemos hecho hasta ahora se ha configurado correctamente:

Volvamos a DAM, reiniciemos el Agente y echemos un vistazo a Status > Collector


![DAM PGSQL](https://i.imgur.com/bUWSh9y.png)
![DAM CMetrics](https://i.imgur.com/5B5PJz9.png)


¡Veo que cmetrics y postgres están listos para comenzar! Esto significa que deberíamos ver que la Consola de Datadog tenga estos datos disponibles para su uso.


![Datadog Console shows PGSQL & CMetrics](https://i.imgur.com/GW7MHVp.png)

Bien Hecho! La informacion llego a Datadog :hand:

## Visualización de datos de Datadog a través de API

Utilizando [Postman] (https://www.postman.com), una herramienta de desarrollo de software utilizada para probar las llamadas a la API, podemos hacer [Datadog API](https://docs.datadoghq.com/api/) 
llamadas para crear Timeboards. Para el próximo ejercicio, creemos tablas de tiempo con los siguientes requisitos:

- [ ] Gráfica 1: Nuestra métrica "CMetric" en mi escritorio de desarrollo de Windows
- [ ] Gráfica 2: Cualquier métrica de la Integración en su Base de Datos con la función de anomalía aplicada
- [ ] Gráfica 3: Nuestra métrica "CMétrica" ​​con la función de resumen aplicada para sumar todos los puntos de la última hora en un solo segmento

Lo primero que necesitaremos, suponiendo que tengamos Postman instalado, es obtener la colección de Datadog Postman e importarla.
Datadog tiene una muy buena guía [aquí] (https://docs.datadoghq.com/getting_started/api/) que repasa todo lo que necesitaremos. Sigue la guía, utilice la colección Authentication Check y su entorno, y envíe la solicitud. Si tiene todo configurado correctamente, debería obtener una respuesta "válida": verdadera de la API de Datadog.

:point_up: Algo que me gustaría señalar, si tiene problemas para abrir el archivo json de descarga de Datadog Collection, intente descomprimirlo primero. Creo que el archivo tiene una extensión .json, sin embargo, es un archivo.

![DatadogPostmanCollection](https://i.imgur.com/BJrcuA4.png)


Now we're ready to talk to Datadog's API through Postman, isn't that exciting!?  

Start off by selecting Dashboards > POST Create a Dashboard under Collections 

![DatadogPostmanDashboardCollection](https://i.imgur.com/6um5Hqh.png)


Ahora construyamos el cuerpo de la solicitud:

1. Título del panel
2. Título de la definición para cada gráfica
3. Llamada de API para cada gráfica
4. Título de cada gráfica

En cuanto al Dashboard, llamémoslo  :sparkles: "Postman Integration Dashboard" :sparkles: 

### Gráfico 1:
Estamos listos para definir cómo se verá el primer gráfico; Para q (que es consulta) queremos el promedio del indicador CMetric, creamos esta integración en un ejercicio anterior.

```JSON
...
"definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:cmetric_gauge{*}"
                    }
                ],
                "title": "CMetric Gauge Average"
            }
...
```
1 de 3 Completadas!

:white_check_mark: Gráfico 1: "CMetric" Average Gauge :thumbsup:

### Gráfico 2:
Para nuestro segundo gráfico, extraeremos métricas de nuestra integración de base de datos PostgreSQL, agregando la función de anomalía; esta función detecta fluctuaciones métricas y las muestra en nuestro gráfico, es muy útil para solucionar problemas.
La [anomaly function] (https://docs.datadoghq.com/monitors/monitor_types/anomaly/) espera un algoritmo sin patrones estacionales repetidos.
Como siempre, siéntase libre de profundizar en la documentación de Datadog. Nuestro panel mostrará anamolios basados en el porcentaje de conexiones de uso.


```JSON
...
"definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)"
                    }
                ],
                "title": "PostgreSQL Anomalies"
            }
        }
...
```

2 de 3! Bien hecho!

:white_check_mark: Grafica 2: PostgreSQL with Anomalies :thumbsup:

### Gráfico 3:
Por último, necesitamos "CMetric" con la [rollup function](https://docs.datadoghq.com/dashboards/functions/rollup/) para la agregación de tiempo personalizada, básicamente para resumir todos los puntos de la última hora en una sola entrada. 
Una vez que se crea el tablero, cambie el período de tiempo para este tablero a 24 horas, de modo que obtengamos 24 puntos de datos.

```JSON
...
"definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:cmetric.gauge{*}.rollup(sum, 3600)"
                    }
                ],
                "title": "CMetric with Rollup"
            }
        }
...
```


3 de 3 completados! Buen trabajo!

:white_check_mark: Grafica 3: CMetric with RollUp :thumbsup:

¡Bien hecho! Combinemos todos nuestros gráficos en una carga útil con formato JSON épica, envíelo y ...

```JSON
{
    "title": "Postman Integration Dashboard",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:cmetric_gauge{*}"
                    }
                ],
                "title": "CMetric Gauge Average"
            }
        },
         {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)"
                    }
                ],
                "title": "PostgreSQL Anomalies"
            }
        },
         {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:cmetric_gauge{*}.rollup(sum, 3600)"
                    }
                ],
                "title": "CMetric with Rollup"
            }
        }
    ],
    "layout_type": "ordered",
    "description": "Dashboard created by Postman Integration",
    "is_read_only": true,
    "notify_list": [],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "LUIS-DESKTOP"
        }
    ],
    "template_variable_presets": [
        {
            "name": "Saved views for hostname 2",
            "template_variables": [
                {
                    "name": "host",
                    "value": "<HOSTNAME_2>"
                }
            ]
        }
    ]
}
```

... ¡así es como se ve una vez enviado a través de Postman! Acabamos de crear un panel a través de API en unos minutos. Súper. Fácil. :ok_hand:
![PostmanDashboard](https://i.imgur.com/Epc79Ra.png)

Para su placer visual en vivo, puede encontrar el dashboard [aqui](https://p.datadoghq.com/sb/i3rc15h7hhkukyes-bd3e3184ece0639a6e384539b80d9fdc)

Para cerrar este capítulo sobre visualizaciones, quiero darte 2 Pro tips:

:high_brightness: Pro Tip - Visualizaciones #1:
Las anomolias le brindan una tendencia histórica para las métricas, cuando una métrica está fuera del umbral, la línea se vuelve roja.
Esto muestra que la métrica se comporta fuera del rango histórico "normal". Muy útil para rastrear métricas que no deberían estar fuera de un umbral normal.
¿Puedes pensar en otros casos de uso?

:high_brightness: Pro Tip - Visualizaciones #2:
Antes de pasar la página a Dashboards y Graphs, hay una característica más que me gustaría compartir con ustedes. Anotaciones.
Supongamos que encontramos algo interesante en un gráfico, si hace clic en el botón Compartir> Share button, puede anotar esa parte particular del gráfico y compartirlo con un miembro del equipo. Recibirán un correo electrónico con un enlace al gráfico con sus notas.
![DatadogAnnotation](https://i.imgur.com/YjcNVY3.png)

## Magníficos monitores (o monitoreando data)
Hasta ahora hemos instalado el agente en un sistema, agregamos integraciones (incorporadas y basadas en lenguaje de scripting); también hemos creado cuadros de mando de la línea de tiempo y podemos colaborar con los miembros del equipo en los datos existentes.

: pregunta: ¿Qué pasa con las notificaciones? pero no esperaríamos que alguien se sentara en un NOC 24/7/365 mirando monitores ...

Aquí es donde entran en juego los datos de seguimiento.

Para nuestro primer monitor, usemos "CMetric" (nuestro script Python de 45 segundos en ejecución, que devuelve un número aleatorio entre 0 y 1000) configuraremos algunos monitores que nos notificarán cuando la métrica supere un cierto valor. .
Navegar a Monitors > Create New Monitor: 

![MonitorNewMonitor](https://i.imgur.com/Ucc4XoO.png)

Usa la alerta de umbral para el método de detección, usaremos CMetric_gauge para la definición de la métrica y estableceremos las condiciones de alerta para 800 en Alerta y 500 en Advertencia.

Debería parecerse a esto:

![MonitorParameters] (https://i.imgur.com/DRaN2LN.png)

¡Personalicemos el mensaje del monitor! Queremos que:

- [ ] Enviarle un correo electrónico cada vez que se active el monitor.
- [ ] Cree mensajes diferentes en función de si el monitor está en estado de Alerta, Advertencia o Sin datos.
- [ ] Incluya el valor de la métrica que provocó que el monitor se activara y la IP del host cuando el monitor activara un estado de alerta.
- [ ] Cuando este monitor le envíe una notificación por correo electrónico, tome una captura de pantalla del correo electrónico que le envía.


### Say what's happening
Podemos personalizar todas estas configuraciones a través de "Say what's happening"
Digamos que esto es una Alerta, esto debe considerarse Prioridad 1 y debe abordarse de inmediato:

Podemos usar variables como {{value}} y {{#is_alert}} para especificar los componentes clave del mensaje. 
Puede dedicar mucho tiempo a personalizar esta configuración, así que seré amable y dejaré la [documentación de notificaciones aquí] (https://docs.datadoghq.com/monitors/notifications/?tab=is_warning#message-template-variables ) para ti.

También agregué un texto que es necesario en todos los tipos de notificación:

```
If you are on call and don't know what to do, maybe take a look at this guide [URL].
If you are confused about this alert, reach out to your Datadog Administrator.
If you're happy and you know it, clap your hands!

Good Luck!

-Datadog
```

Una vez que agregues el aspecto que deberían tener tus notificaciones, desplácese hacia abajo y selecciona Test Notifications para ver cómo se verán.
Te dejo el código asociado con cada tipo de notificación, así como la notificación real que recibimos por correo electrónico, cuando probamos la función de notificación.


#### Alerts
```
{{#is_alert}}
Priority 1 Alert!!
CMetric is at {{value}}, and has been above 800 for the past 5 minutes 
You should troubleshoot this ASAP, contact someone who knows how to fix this or maybe escalate!
REMEMBER, SENSE OF URGENCY!
{{/is_alert}}
```
![AlertP1](https://i.imgur.com/v122gl9.png)


```
{{#is_warning}}
Warning Alert!!
CMetric is at {{value}}, and has been above 500 for the past 5 minutes
You should probably look at this...
{{/is_warning}}
```
![AlertWarn](https://i.imgur.com/ze0SM5l.png)


```
{{#is_recovery}}
Recovery Alert! Phew!
CMetric has recovered! Current Value is {{value}}
Should this service be failing...?
{{/is_recovery}}
```
![AlertNoData](https://i.imgur.com/kTb5Epr.png)


```
{{#is_no_data}}
P1 Alert!!
CMetric has not reported any data over the last 5 minutes
You should troubleshoot this ASAP, contact someone who knows how to fix this or maybe escalate...
{{/is_no_data}}
```
![AlertRecovery](https://i.imgur.com/G9VHnqT.png)

:high_brightness: Pro Tip:
Las notificaciones por correo electrónico no son la única forma de notificar alertas a los humanos. 
Puede configurar [Slack] (https://docs.datadoghq.com/integrations/slack/?tab=standardintegration), [PagerDuty] (https://docs.datadoghq.com/integrations/pagerduty/), [Microsoft Teams ] (https://docs.datadoghq.com/integrations/microsoft_teams/) y otros. 
Si tienes curiosidad sobre qué integraciones están disponibles, consulta nuestra Documentación sobre integraciones [aquí] (https://docs.datadoghq.com/integrations)

#### Gestionar el tiempo de inactividad (hora de dormir)
Digamos que está fuera de la oficina de vacaciones, tal vez no trabaja los fines de semana o no es parte del grupo de rotación OnCall; ¿Realmente necesitas notificaciones en esos momentos? 
Administrar su tiempo de inactividad es tan fácil como navegar a *** Monitors> Manage Downtime *** y crear / personalizar monitores de tiempo de inactividad:

![SleepyTime](https://i.imgur.com/sGZ4W6X.png)

Deberías recibir una notificación por correo electrónico que explique el tiempo de inactividad:

![SleepyTimeExplanation](https://i.imgur.com/i0PStKT.png)


## Analizando datos de APM asombrosos
Desde el comienzo de esta guía, nuestra promesa ha sido que visualizamos y monitoreamos todo para que pueda administrar su negocio, para que pueda concentrarse en lo más 
importante. Hemos podido agregar y monitorear hosts, archivos de registro, integraciones, manejar notificaciones y administrar el tiempo de inactividad; lo que no sabe es que consideramos la gestión del rendimiento de aplicaciones (o APM para abreviar) uno de los componentes centrales de Datadog.
[APM](https://www.datadoghq.com/product/apm/), en su definición directa, le permite monitorear, solucionar problemas y optimizar el rendimiento de las aplicaciones 
de un extremo a otro; le otorga una vista de halcón granular y escalable de sus aplicaciones, y es SUPER fácil de implementar en sus aplicaciones.

En esta sección, me gustaría compartir contigo un ejemplo rápido sobre cómo logramos esto. (No se preocupe, asumiré que estoy hablando para una audiencia amplia, 
por lo que no necesitas ser muy técnico para escucharme)

Imaginemos un escenario. Su equipo de desarrollo ha estado trabajando en su última aplicación insignia , ¡y está lista para funcionar! 
Todo el mundo está emocionado al escuchar que van a dar un período de prueba, invitando a clientes específicos, antes de salir al mercado. Digamos que tus aplicaciones (BusinessApp.py) se parecen un poco a este script:

```Python
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```

Una aplicación sencilla con mínimo esfuerzo. Definiremos los parámetros de ingestión e iniciaremos la aplicación ejecutando esto:
(Si no comprendes lo que esto significa o necesita más detalles, no dudes en visitar nuestra [guia de documentacion](https://docs.datadoghq.com/tracing/). Tiene muchos ejemplos y está muy bien explicada.)


```python
export DD_SERVICE=flask
DD_SERVICE="flask" DD_ENV="test" DD_LOGS_INJECTION=true DD_TRACE_ANALYTICS_ENABLED=true DD_PROFILING_ENABLED=true ddtrace-run python BusinessApp.py
```

recibimos una notificación que se está ejecutando correctamente

![BusinessAppRunningCorrectly](https://i.imgur.com/3G71V7p.png)

y en unos minutos, este servicio de aplicación se muestra en Datadog Console. En este punto, se ha indicado al componente Flask que ingiera en APM.
Ahora estamos listos para revisar las métricas asociadas con BusinessApp.py

Navegue a *** APM> Services ***, encontraremos nuestra aplicación Flask aquí. La pestaña Services le brinda información específica sobre el estado de su servicio
(Cuántas solicitudes están entrando, cuál es nuestra tasa de error, hasta dónde llega la latencia, información específica del punto final y más).

~[APMServices](https://i.imgur.com/kyg0YIb.png)


Debajo del servicio específico, podemos ver cómo le está yendo a nuestro anfitrión. Uso promedio de CPU, memoria utilizable, uso de disco, etc.
Esto le da una idea de qué tan bien lo está haciendo el host y la relación con los usuarios finales que utilizan la aplicación web.

![APMInfraMetrics](https://i.imgur.com/YI5RTVz.png)


Pasemos a la siguiente pestaña, Traces.
Los Traces rastrean la cantidad de tiempo que una aplicación tarda en procesar una sola solicitud y el estado de dicha solicitud, y podemos ampliar nuestra búsqueda desde aquí 

![APMTraces](https://i.imgur.com/2eLzi78.png)


... y podemos ampliarlo desde aquí. Haz clic en un rastro específico. Encontrarás etiquetas asociadas con el seguimiento, así como una línea de tiempo.

![APMTracesSpecific](https://i.imgur.com/Ut26YRj.png)


También encontrarás cómo el seguimiento afectó a la infraestructura haciendo clic en Métricas.

![APMTracesSpecificMetrics](https://i.imgur.com/pFEpYvS.png)


Pasando a App Analytics, podemos usar filtros específicos para etiquetas, lo que nos permite obtener una vista más detallada de las solicitudes.

![APMAppAnalytics](https://i.imgur.com/vO42Gc4.png)



Y por último pero no de menos importancia:

Perfiles. Los perfiles permiten un mejor rendimiento de la resolución de problemas, utilizando funciones específicas del entorno que consumen recursos para la optimización. ¡Muy útil!

![APMProfiles](https://i.imgur.com/FvFt0kL.png)

Como último "regalo", he creado un panel que tiene la infraestructura subyacente asociada con nuestra aplicación web.

![APMFlaskDashboard](https://i.imgur.com/5cawALc.png)

con un [enlace directo](https://p.datadoghq.com/sb/i3rc15h7hhkukyes-10e5a3a67255d1cb2051e1f5ec7872ea) para tu placer visual.


:high_brightness: Pro Tip:
Recuerda que un Servicio es software que realiza tareas automatizadas, escucha en contra de solicitudes de datos, almacena datos o ejecuta según el diseñado por su desarrollador. 
Por lo general, se dividen en (interfaz web, api, caché y bases de datos).

Un recurso, sin embargo, es una acción para un servicio. Normalmente se ve como un query o un trabajo. Es un proceso que pertenece a un Servicio.

## ¿Qué más visualizarías?

Uno de los placeres de trabajar con Datadog es la capacidad de comunicarse visualmente. Como ingeniero de DevOps, debes saber que visualizaría todo lo que pudiera, si tuviera tiempo... (y lo voy a intentar)

Si tuviera una opción profesional, fuera de nuestros socios tecnológicos, sería integrar Datadog en hospitales, aeropuertos y negocios de venta general.

La integración para mostrar los tiempos de espera, la cantidad de incidentes personalizados y los mensajes de transmisión de emergencia es algo que me encantaría ver como consumidor. Como propietario de un negocio, comparar las ventas año tras año, ver los clientes que regresan o la mayoría de los artículos comprados en tiempo real, ciertamente puede tener un impacto en las decisiones.

La visualización de datos te permite comprender qué funciona y qué no. Y, en última instancia, eso es lo que estamos aquí para hacer.

..y acabamos de empezar. Establezce su horizonte con Datadog, concéntrate en lo que importa.





Luis Arano
Ingero Tecnico de Ventas, Datadog



¿Experimentaste algún problema con la guía? ¿Tienes alguna pregunta o te gustaría darnos su opinión?
Envíanos un mensaje a saleshelp@datadoghq.com
