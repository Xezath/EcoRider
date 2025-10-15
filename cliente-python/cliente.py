import sys
import datetime
import configparser
import requests
from requests.structures import CaseInsensitiveDict

# Archivo de configuración
archivo_config = 'ConfigFile.properties'

# URLs del servidor (Viajes) (se cargan desde el config)
api_viajes_url_listar = None
api_viajes_url_crear = None
api_viajes_url_actualizar = None
api_viajes_url_eliminar = None
api_viajes_url_por_id = None


# URLs del servidor (Vehículos)
api_vehiculos_url_listar = None
api_vehiculos_url_crear = None
api_vehiculos_url_actualizar = None
api_vehiculos_url_eliminar = None
api_vehiculos_url_por_id = None


# Cargar variables desde ConfigFile.properties
def cargar_variables():
    global api_viajes_url_listar, api_viajes_url_crear, api_viajes_url_actualizar, api_viajes_url_eliminar, api_viajes_url_por_id
    global api_vehiculos_url_listar, api_vehiculos_url_crear, api_vehiculos_url_actualizar, api_vehiculos_url_eliminar, api_vehiculos_url_por_id

    config = configparser.RawConfigParser()
    config.read(archivo_config)

    # VIAJES    
    api_viajes_url_listar = config.get('SeccionApi', 'api_viajes_url_listar')
    api_viajes_url_crear  = config.get('SeccionApi', 'api_viajes_url_crear')
    api_viajes_url_actualizar = config.get('SeccionApi', 'api_viajes_url_actualizar')
    api_viajes_url_eliminar   = config.get('SeccionApi', 'api_viajes_url_eliminar')
    api_viajes_url_por_id = config.get('SeccionApi', 'api_viajes_url_por_id')


    # VEHICULOS
    api_vehiculos_url_listar = config.get('SeccionApi', 'api_vehiculos_url_listar')
    api_vehiculos_url_crear = config.get('SeccionApi', 'api_vehiculos_url_crear')
    api_vehiculos_url_actualizar = config.get('SeccionApi', 'api_vehiculos_url_actualizar')
    api_vehiculos_url_eliminar = config.get('SeccionApi', 'api_vehiculos_url_eliminar')
    api_vehiculos_url_por_id = config.get('SeccionApi', 'api_vehiculos_url_por_id')


# --------------------------
# VIAJES
# --------------------------

# Listar todos los viajes o con filtros
def listar():
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    # Pedimos filtros opcionales
    origen_filtro = input("Filtrar por ciudad de origen (Enter para ignorar): ").strip()
    destino_filtro = input("Filtrar por ciudad de destino (Enter para ignorar): ").strip()

    params = {}
    if origen_filtro:
        params["origen"] = origen_filtro
    if destino_filtro:
        params["destino"] = destino_filtro

    r = requests.get(api_viajes_url_listar, headers=headers, params=params)
    if r.status_code == 200:
        listado = r.json()
        if not listado:
            print("No hay viajes disponibles con esos filtros.")
        else:
            for v in listado:
                print(f"ID: {v.get('id')}, Origen: {v.get('origen')}, Destino: {v.get('destino')}, Hora: {v.get('hora')}, Cupos: {v.get('cupo')}")
    else:
        print(f"Error al listar viajes. Código: {r.status_code}")


# Crear un nuevo viaje
def crear():
    origen = input("Ingrese ciudad de origen: ")
    destino = input("Ingrese ciudad de destino: ")
    hora = input("Ingrese hora (HH:MM): ")
    cupo = int(input("Ingrese cantidad de cupos: "))
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    datos = {'origen': origen, 'destino': destino, 'hora': hora, 'cupo': cupo}
    r = requests.post(api_viajes_url_crear, headers=headers, json=datos)
    if 200 <= r.status_code < 300:
        print("✅ Viaje creado con éxito!")
    else:
        print(f"❌ Error al crear viaje: {r.status_code}")
        try:
            print("Detalles:", r.json())
        except:
            print(r.text)


# ACTUALIZAR VIAJE
def actualizar():
    id = int(input("Ingrese ID del viaje a actualizar: "))
    viaje_actual = obtener_viaje_por_id(id)
    if not viaje_actual:
        return

    origen = input(f"Ingrese nueva ciudad de origen (Enter para mantener '{viaje_actual.get('origen')}'): ").strip()
    destino = input(f"Ingrese nueva ciudad de destino (Enter para mantener '{viaje_actual.get('destino')}'): ").strip()
    hora = input(f"Ingrese nueva hora (HH:MM) (Enter para mantener '{viaje_actual.get('hora')}'): ").strip()
    cupo = input(f"Ingrese nueva cantidad de cupos (Enter para mantener '{viaje_actual.get('cupo')}'): ").strip()

    datos = {
        "origen": origen if origen else viaje_actual.get("origen"),
        "destino": destino if destino else viaje_actual.get("destino"),
        "hora": hora if hora else viaje_actual.get("hora"),
        "cupo": int(cupo) if cupo else viaje_actual.get("cupo")
    }

    url = f"{api_viajes_url_actualizar}/{id}"
    r = requests.put(url, headers={"Accept": "application/json", "Content-Type": "application/json"}, json=datos)
    if r.status_code == 200:
        print("✅ Viaje actualizado con éxito!")
    else:
        print(f"❌ Error al actualizar viaje: {r.status_code}", r.text)


# ELIMINAR VIAJE
def eliminar():
    id = int(input("Ingrese ID del viaje a eliminar: "))
    url = f"{api_viajes_url_eliminar}/{id}"
    r = requests.delete(url)
    if r.status_code == 204:
        print("✅ Viaje eliminado con éxito!")
    elif r.status_code == 404:
        print("❌ Viaje no encontrado.")
    else:
        print(f"❌ Error al eliminar viaje: {r.status_code}", r.text)


def obtener_viaje_por_id(id: int):
    url = f"{api_viajes_url_por_id}/{id}"  # usar la URL de actualizar/eliminar base
    r = requests.get(url, headers={"Accept": "application/json"})
    if r.status_code == 200:
        return r.json()
    else:
        print("❌ Viaje no encontrado.")
        return None



# --------------------------
# VEHÍCULOS
# --------------------------

def listar_vehiculos():
    headers = {"Accept": "application/json"}
    r = requests.get(api_vehiculos_url_listar, headers=headers)
    if r.status_code == 200:
        vehiculos = r.json()
        if not vehiculos:
            print("No hay vehículos registrados.")
        else:
            for v in vehiculos:
                print(f"ID: {v.get('id')}, Placa: {v.get('placa')}, Modelo: {v.get('modelo')}, Capacidad: {v.get('capacidad')}, Tipo: {v.get('tipo')}")
    else:
        print(f"❌ Error al listar vehículos ({r.status_code})")


def crear_vehiculo():
    placa = input("Ingrese número de placa: ")
    modelo = input("Ingrese modelo del vehículo: ")
    capacidad = int(input("Ingrese capacidad (número de asientos): "))
    tipo = input("Ingrese tipo (auto, van, moto, etc.): ")

    datos = {"placa": placa, "modelo": modelo, "capacidad": capacidad, "tipo": tipo}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    r = requests.post(api_vehiculos_url_crear, headers=headers, json=datos)
    if 200 <= r.status_code < 300:
        print("✅ Vehículo creado con éxito!")
    else:
        print(f"❌ Error al crear vehículo: {r.status_code}", r.text)

# --------------------------
# MENÚ INTERACTIVO
# --------------------------
def menu():
    while True:
        print("\n--- Cliente EcoRide ---")
        print("1. Listar viajes")
        print("2. Crear viaje")
        print("3. Actualizar viaje")
        print("4. Eliminar viaje")
        print("5. Vehículos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            listar()
        elif opcion == "2":
            crear()
        elif opcion == "3":
            actualizar()
        elif opcion == "4":
            eliminar()
        elif opcion == "5":
            menu_vehiculos()  # Submenú de vehículos
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

def menu_vehiculos():
    while True:
        print("\n--- Gestión de Vehículos ---")
        print("1. Listar vehículos")
        print("2. Crear vehículo")
        print("3. Volver")
        op = input("Seleccione una opción: ")

        if op == "1":
            listar_vehiculos()
        elif op == "2":
            crear_vehiculo()
        elif op == "3":
            break
        else:
            print("Opción inválida.")

# --------------------------
# EJECUCIÓN PRINCIPAL
# --------------------------
if __name__ == "__main__":
    print("Iniciando cliente EcoRide -", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cargar_variables()
    menu()
    print("Finalizando -", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# # --------------------------
# #     EJECUCIÓN PRINCIPAL
# # --------------------------
# print("Iniciando cliente EcoRide -", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# cargar_variables()

# print("\nPrimer listado de viajes:")
# listar()
# print("________________")

# print("\nCrear nuevo viaje:")
# origen = input("Ingrese ciudad de origen: ")
# destino = input("Ingrese ciudad de destino: ")
# hora = input("Ingrese hora (HH:MM): ")
# cupo = int(input("Ingrese cantidad de cupos: "))
# crear(origen, destino, hora, cupo)

# print("\nListado actualizado de viajes:")
# listar()
# print("\nFinalizando -", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
