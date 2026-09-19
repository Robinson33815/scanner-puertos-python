"""
Escáner de Puertos TCP
Autor: Robinson Sarabia
Materia: Seguridad Informática - Grupo# 14
Universidad Estatal de Milagro (UNEMI)

Escanea un rango de puertos TCP de un equipo usando sockets (connect_ex).

AVISO: usar únicamente en equipos propios, máquinas virtuales o
laboratorios autorizados.

Uso:
    python scanner_puertos.py
"""

import ipaddress
import socket
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

TIMEOUT = 0.5   # segundos de espera por puerto
HILOS = 100     # puertos que se revisan al mismo tiempo

SERVICIOS = {
    1: "TCPMUX", 2: "COMPRESSNET", 3: "COMPRESSNET", 5: "RJE", 7: "ECHO",
    9: "DISCARD", 11: "SYSTAT", 13: "DAYTIME", 17: "QOTD", 18: "MSP",
    19: "CHARGEN", 20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "TELNET",
    25: "SMTP", 37: "TIME", 42: "NAMESERVER", 43: "WHOIS", 49: "TACACS",
    53: "DNS", 67: "DHCP-SERVER", 68: "DHCP-CLIENT", 69: "TFTP",
    70: "GOPHER", 79: "FINGER", 80: "HTTP", 88: "KERBEROS", 110: "POP3",
    111: "RPCBIND", 119: "NNTP", 123: "NTP", 135: "MSRPC",
    137: "NETBIOS-NS", 138: "NETBIOS-DGM", 139: "NETBIOS-SSN",
    143: "IMAP", 161: "SNMP", 162: "SNMPTRAP", 389: "LDAP", 443: "HTTPS",
    445: "SMB", 465: "SMTPS", 500: "ISAKMP", 514: "SYSLOG", 515: "LPD",
    520: "RIP", 587: "SMTP-SUBMISSION", 631: "IPP", 636: "LDAPS",
    873: "RSYNC", 902: "VMWARE-AUTH", 989: "FTPS-DATA", 990: "FTPS",
    993: "IMAPS", 995: "POP3S", 1080: "SOCKS", 1194: "OPENVPN",
    1433: "MSSQL", 1521: "ORACLE", 1723: "PPTP", 2049: "NFS",
    2082: "CPANEL", 2083: "CPANEL-HTTPS", 2181: "ZOOKEEPER",
    2375: "DOCKER", 2376: "DOCKER-HTTPS", 3000: "HTTP-DEV",
    3306: "MYSQL", 3389: "RDP", 5432: "POSTGRESQL", 5900: "VNC",
    6379: "REDIS", 6443: "KUBERNETES-API", 8000: "HTTP-ALT",
    8008: "HTTP-ALT", 8080: "HTTP-ALT", 8081: "HTTP-PROXY",
    8443: "HTTPS-ALT", 8888: "HTTP-ALT", 9000: "PHP-FPM/HTTP-ALT",
    9090: "PROMETHEUS", 9200: "ELASTICSEARCH", 9300: "ELASTICSEARCH",
    11211: "MEMCACHED", 27017: "MONGODB",
}


def nombre_servicio(puerto):
    """Devuelve el nombre del servicio según el puerto estándar."""
    if puerto in SERVICIOS:
        return SERVICIOS[puerto]
    try:
        return socket.getservbyport(puerto, "tcp").upper()
    except OSError:
        return "DESCONOCIDO"


def ip_valida(texto):
    """Acepta solo IPv4 privadas o locales (127.x, 192.168.x, 10.x, 172.16-31.x)."""
    try:
        ip = ipaddress.ip_address(texto.strip())
    except ValueError:
        return False
    return ip.version == 4 and (ip.is_private or ip.is_loopback)


def escanear_puerto(ip, puerto):
    """Intenta una conexión TCP. Devuelve el puerto si está abierto."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)
        return puerto if s.connect_ex((ip, puerto)) == 0 else None


def escanear(ip, inicio, fin):
    """Escanea el rango indicado y devuelve la lista de puertos abiertos."""
    with ThreadPoolExecutor(max_workers=HILOS) as ejecutor:
        resultados = ejecutor.map(
            lambda p: escanear_puerto(ip, p), range(inicio, fin + 1)
        )
        return sorted(p for p in resultados if p is not None)


def pedir_puerto(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if 1 <= valor <= 65535:
                return valor
        except ValueError:
            pass
        print("  Ingresa un número entre 1 y 65535.")


def guardar(ip, inicio, fin, abiertos, tiempo):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lineas = [
        "==================================",
        "RESULTADO DEL ESCANEO DE PUERTOS TCP",
        "==================================",
        f"Fecha:               {fecha}",
        "Autor:               Robinson Sarabia",
        f"IP analizada:        {ip}",
        f"Rango evaluado:      {inicio}-{fin}",
    ]
    if abiertos:
        lineas += [f"  Puerto {p} ---> ABIERTO ({nombre_servicio(p)})" for p in abiertos]
    else:
        lineas.append("  No se encontraron puertos abiertos.")
    lineas += [f"Tiempo de ejecución: {tiempo:.2f} s",
               "=================================="]

    with open("resultado_escaneo.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print("Resultados guardados en resultado_escaneo.txt")


def main():
    print("=" * 40)
    print("   ESCÁNER DE PUERTOS TCP")
    print("   Autor: Robinson Sarabia")
    print("=" * 40)
    print("Usa esta herramienta solo en equipos propios o autorizados.\n")

    ip = input("IP objetivo: ").strip()
    if not ip_valida(ip):
        print("IP no válida o no permitida (solo IPv4 privadas o locales).")
        return

    inicio = pedir_puerto("Puerto inicial: ")
    fin = pedir_puerto("Puerto final: ")
    if fin < inicio:
        print("El puerto final debe ser mayor o igual al inicial.")
        return

    confirmar = input("¿El equipo es propio o cuentas con autorización? (s/n): ")
    if confirmar.strip().lower() not in ("s", "si", "sí"):
        print("Escaneo cancelado.")
        return

    print(f"\nEscaneando {ip} (puertos {inicio}-{fin})...\n")
    t0 = time.time()
    abiertos = escanear(ip, inicio, fin)
    tiempo = time.time() - t0

    for p in abiertos:
        print(f"Puerto {p:<5} ---> ABIERTO ({nombre_servicio(p)})")
    if not abiertos:
        print("No se encontraron puertos abiertos.")

    print("\n--- RESUMEN ---")
    print(f"IP analizada:        {ip}")
    print(f"Puertos evaluados:   {fin - inicio + 1}")
    print(f"Puertos abiertos:    {len(abiertos)}")
    print(f"Tiempo de ejecución: {tiempo:.2f} segundos")

    if input("\n¿Guardar resultados en un archivo? (s/n): ").strip().lower() in ("s", "si", "sí"):
        guardar(ip, inicio, fin, abiertos, tiempo)


if __name__ == "__main__":
    main()
