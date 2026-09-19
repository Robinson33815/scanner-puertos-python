# Manual de Uso — Escáner de Puertos TCP

**Autor:** Robinson Sarabia
**Materia:** Seguridad Informática — Grupo# 14
**Universidad:** Universidad Estatal de Milagro (UNEMI)
**Repositorio:** https://github.com/Robinson33815/scanner-puertos-python

---

## 1. Introducción

Este proyecto es un escáner de puertos **TCP** con interfaz web. El backend está hecho en **Python + Django** y usa la librería estándar `socket` (método `connect_ex()`) para comprobar qué puertos de un equipo aceptan conexiones. La interfaz, hecha en HTML, CSS y JavaScript, permite indicar la IP y el rango de puertos, ver el avance del análisis, leer un informe final y guardar los resultados en un archivo de texto.

## 2. Aviso legal y ético

> Esta herramienta **solo debe usarse en equipos propios, máquinas virtuales o laboratorios autorizados**. Escanear equipos ajenos sin permiso puede ser ilegal.

Por seguridad, la aplicación pide confirmar que el equipo es propio o autorizado antes de iniciar cada escaneo.

## 3. Requisitos

- Windows, Linux o macOS
- Python 3.10 o superior
- Git (para clonar el repositorio)
- Un navegador web (Chrome, Edge o Firefox)

## 4. Instalación

**1. Clonar el repositorio**

```bash
git clone https://github.com/Robinson33815/scanner-puertos-python.git
cd scanner-puertos-python
```

**2. Crear y activar el entorno virtual**

En Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instalar las dependencias**

```bash
pip install -r requirements.txt
```

**4. Iniciar el servidor**

```bash
python manage.py runserver
```

**5. Abrir la aplicación**

Entrar en el navegador a:

```
http://127.0.0.1:8000/
```

Para detener el servidor, presionar `Ctrl + C` en la terminal.

![Servidor iniciado](capturas/01_servidor_iniciado.png)

## 5. Uso de la aplicación

### 5.1 Pantalla principal

Al abrir la página se muestra el escáner con sus tres campos y dos botones.

![Pantalla principal](capturas/02_pantalla_principal.png)

| Campo | Descripción |
|---|---|
| `ip_objetivo` | Dirección IP del equipo a analizar. Solo se aceptan IP privadas o locales (127.0.0.1, 192.168.x.x, 10.x.x.x). |
| `puerto_inicio` | Primer puerto del rango (mínimo 1). |
| `puerto_fin` | Último puerto del rango (máximo 65535). Debe ser mayor o igual al inicial. |

| Botón | Función |
|---|---|
| ▶ Iniciar Escaneo | Ejecuta el análisis. |
| ⬇ Guardar resultados | Descarga el resultado en `resultado_escaneo.txt`. Se habilita al terminar el escaneo. |

### 5.2 Realizar un escaneo

1. Escribir la **IP** del equipo (por ejemplo `192.168.1.10`).
2. Escribir el **rango de puertos** (por ejemplo, del 1 al 100).
3. Pulsar **▶ Iniciar Escaneo**.
4. Aparecerá una ventana que pregunta si el equipo es propio o autorizado. Pulsar **Aceptar** solo si es así.
5. Esperar a que termine. Se muestra una barra superior con el estado y la consola va imprimiendo la información.

![Confirmación de autorización](capturas/03_confirmacion.png)
![Escaneo en progreso](capturas/04_escaneo_en_progreso.png)

> **Nota:** el tiempo depende del número de puertos y de la respuesta del equipo. Un rango de 500 puertos puede tardar varios minutos. La barra de progreso es solo visual y no indica el porcentaje real.

### 5.3 Resultados

Al terminar, la consola muestra:

- Cada puerto abierto con el nombre de su servicio, por ejemplo `Puerto 80 ---> ABIERTO (HTTP)`.
- Una observación de riesgo (ALTO, MEDIO o BAJO) debajo de cada puerto abierto.
- Un **resumen**: IP analizada, puertos evaluados, puertos abiertos y tiempo de ejecución.
- Un **informe del analista de ciberseguridad** con nivel de exposición, hallazgos, recomendaciones priorizadas y conclusión.

![Resultados del escaneo](capturas/05_resultados.png)
![Informe del analista](capturas/06_informe_analista.png)

### 5.4 Guardar los resultados

Pulsar **⬇ Guardar resultados**. Se descarga el archivo `resultado_escaneo.txt` con la fecha, la IP, el rango evaluado, los puertos abiertos con su observación, el tiempo de ejecución y el informe del analista.

![Archivo guardado](capturas/07_archivo_guardado.png)

### 5.5 Uso por consola (opcional)

También se puede usar sin la interfaz web, con el script independiente:

```bash
python scanner_puertos.py
```

El programa pregunta la IP objetivo, el puerto inicial y el final, y solicita confirmar que el equipo es propio o autorizado. Al terminar muestra los puertos abiertos con su servicio, un resumen y ofrece guardar el resultado en `resultado_escaneo.txt`.

![Uso por consola](capturas/09_consola.png)

## 6. Cómo interpretar los resultados

| Nivel | Significado |
|---|---|
| **ALTO** | Servicio delicado si está expuesto (por ejemplo SMB, RDP, bases de datos). Conviene cerrarlo o restringirlo con firewall. |
| **MEDIO** | Servicio que requiere una configuración segura (por ejemplo SSH, DNS). |
| **BAJO** | Servicio habitual, con riesgo bajo si está bien configurado (por ejemplo HTTP/HTTPS). |

Niveles de exposición global del informe: NINGUNO, BAJO, MEDIO, ALTO y CRÍTICO.

## 7. Prueba experimental

Escaneo realizado sobre un equipo de la red local, con el fin de comprobar el funcionamiento de la herramienta.

| Elemento | Resultado |
|---|---|
| Tipo de equipo | *(completar: equipo propio / máquina virtual / laboratorio autorizado)* |
| IP utilizada | 192.168.1.19 |
| Rango de puertos | 1 – 500 |
| Puertos evaluados | 500 |
| Puertos abiertos | 80 (HTTP), 139 (NETBIOS-SSN), 445 (SMB) |
| Tiempo de ejecución | 248.84 segundos |
| Observación | Los puertos 139 y 445 indican un equipo con servicios de Windows (NetBIOS/SMB) expuestos, considerados de riesgo alto. El puerto 80 indica un servidor web sin cifrado (HTTP). Se recomienda actualizar el sistema, restringir SMB con firewall y usar HTTPS. |

![Prueba experimental](capturas/08_prueba_experimental.png)

## 8. Limitaciones

- El escaneo es únicamente **TCP**. No detecta puertos **UDP**.
- El nombre del servicio se asigna según el **número de puerto estándar**; no se verifica qué programa está realmente escuchando ni su versión.
- Las observaciones y el informe del analista se generan con **reglas predefinidas** según los puertos abiertos. Indican riesgos posibles, no vulnerabilidades confirmadas.
- La barra de progreso es decorativa.
- Para confirmar servicios y versiones se recomienda usar herramientas como Nmap (`nmap -sV`), siempre en entornos autorizados.

## 9. Solución de problemas

| Problema | Solución |
|---|---|
| La página sale en blanco | Verificar que `scanner/templates/scanner/index.html` tenga contenido y esté guardado. Recargar con `Ctrl + F5`. |
| "Sin conexión con el servidor" | El servidor Django no está corriendo. Ejecutar `python manage.py runserver` y abrir la página desde `http://127.0.0.1:8000/`. |
| Error de puerto en uso | Cerrar el otro servidor o iniciar en otro puerto: `python manage.py runserver 8001`. |
| Error al activar el entorno virtual en PowerShell | Ejecutar `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` y volver a activarlo. |
| El escaneo tarda mucho | Reducir el rango de puertos. Los puertos filtrados esperan el tiempo de espera completo. |
| Muestra "IP no permitida" | Solo se aceptan IP privadas o locales. |

## 10. Estructura del repositorio

```
scanner-puertos-python/
├── scanner_puertos.py    # Lógica de escaneo TCP
├── README.md             # Presentación del proyecto
├── MANUAL_USO.md         # Este manual
├── manage.py
├── requirements.txt
├── escaner_web/          # Configuración del proyecto Django
├── scanner/              # App: vistas, rutas y plantilla HTML
└── capturas/             # Capturas de pantalla del manual
```
