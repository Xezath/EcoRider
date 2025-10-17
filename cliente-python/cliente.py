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


# URLs del servidor (Usuarios)
api_usuarios_url_listar = None
api_usuarios_url_crear = None
api_usuarios_url_actualizar = None
api_usuarios_url_eliminar = None
api_usuarios_url_por_id = None


# URLs del servidor (Reservas)
api_reservas_url_listar = None
api_reservas_url_crear = None
api_reservas_url_actualizar = None
api_reservas_url_eliminar = None
api_reservas_url_por_id = None


# Cargar variables desde ConfigFile.properties
def cargar_variables():
    global api_viajes_url_listar, api_viajes_url_crear, api_viajes_url_actualizar, api_viajes_url_eliminar, api_viajes_url_por_id
    global api_vehiculos_url_listar, api_vehiculos_url_crear, api_vehiculos_url_actualizar, api_vehiculos_url_eliminar, api_vehiculos_url_por_id
    global api_usuarios_url_listar, api_usuarios_url_crear, api_usuarios_url_actualizar, api_usuarios_url_eliminar, api_usuarios_url_por_id
    global api_reservas_url_listar, api_reservas_url_crear, api_reservas_url_actualizar, api_reservas_url_eliminar, api_reservas_url_por_id

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


    # USUARIOS
    api_usuarios_url_listar = config.get('SeccionApi', 'api_usuarios_url_listar')
    api_usuarios_url_crear = config.get('SeccionApi', 'api_usuarios_url_crear')
    api_usuarios_url_actualizar = config.get('SeccionApi', 'api_usuarios_url_actualizar')
    api_usuarios_url_eliminar = config.get('SeccionApi', 'api_usuarios_url_eliminar')
    api_usuarios_url_por_id = config.get('SeccionApi', 'api_usuarios_url_por_id')


    # RESERVAS
    api_reservas_url_listar = config.get('SeccionApi', 'api_reservas_url_listar')
    api_reservas_url_crear = config.get('SeccionApi', 'api_reservas_url_crear')
    api_reservas_url_actualizar = config.get('SeccionApi', 'api_reservas_url_actualizar')
    api_reservas_url_eliminar = config.get('SeccionApi', 'api_reservas_url_eliminar')
    api_reservas_url_por_id = config.get('SeccionApi', 'api_reservas_url_por_id')


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
# USUARIOS
# --------------------------

def listar_usuarios():
    headers = {"Accept": "application/json"}
    r = requests.get(api_usuarios_url_listar, headers=headers)
    if r.status_code == 200:
        usuarios = r.json()
        if not usuarios:
            print("No hay usuarios registrados.")
        else:
            for u in usuarios:
                print(f"ID: {u.get('id')}, Nombre: {u.get('nombre')}, Email: {u.get('email')}, Teléfono: {u.get('telefono')}, VehículoID: {u.get('vehiculoId')}")
    else:
        print(f"❌ Error al listar usuarios ({r.status_code})")


def crear_usuario():
    nombre = input("Ingrese nombre del usuario: ")
    email = input("Ingrese email: ")
    telefono = input("Ingrese teléfono: ")
    vehiculo_id = input("Ingrese ID del vehículo (Enter para omitir): ").strip()

    datos = {
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "vehiculoId": int(vehiculo_id) if vehiculo_id else None
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    r = requests.post(api_usuarios_url_crear, headers=headers, json=datos)
    if 200 <= r.status_code < 300:
        print("✅ Usuario creado con éxito!")
    else:
        print(f"❌ Error al crear usuario: {r.status_code}", r.text)


def actualizar_usuario():
    id = int(input("Ingrese ID del usuario a actualizar: "))
    usuario_actual = obtener_usuario_por_id(id)
    if not usuario_actual:
        return

    nombre = input(f"Ingrese nuevo nombre (Enter para mantener '{usuario_actual.get('nombre')}'): ").strip()
    email = input(f"Ingrese nuevo email (Enter para mantener '{usuario_actual.get('email')}'): ").strip()
    telefono = input(f"Ingrese nuevo teléfono (Enter para mantener '{usuario_actual.get('telefono')}'): ").strip()
    vehiculo_id = input(f"Ingrese nuevo ID del vehículo (Enter para mantener '{usuario_actual.get('vehiculoId')}'): ").strip()

    datos = {
        "nombre": nombre if nombre else usuario_actual.get("nombre"),
        "email": email if email else usuario_actual.get("email"),
        "telefono": telefono if telefono else usuario_actual.get("telefono"),
        "vehiculoId": int(vehiculo_id) if vehiculo_id else usuario_actual.get("vehiculoId")
    }

    url = f"{api_usuarios_url_actualizar}/{id}"
    r = requests.put(url, headers={"Accept": "application/json", "Content-Type": "application/json"}, json=datos)
    if r.status_code == 200:
        print("✅ Usuario actualizado con éxito!")
    else:
        print(f"❌ Error al actualizar usuario: {r.status_code}", r.text)


def eliminar_usuario():
    id = int(input("Ingrese ID del usuario a eliminar: "))
    url = f"{api_usuarios_url_eliminar}/{id}"
    r = requests.delete(url)
    if r.status_code == 204:
        print("✅ Usuario eliminado con éxito!")
    elif r.status_code == 404:
        print("❌ Usuario no encontrado.")
    else:
        print(f"❌ Error al eliminar usuario: {r.status_code}", r.text)


def obtener_usuario_por_id(id: int):
    url = f"{api_usuarios_url_por_id}/{id}"
    r = requests.get(url, headers={"Accept": "application/json"})
    if r.status_code == 200:
        return r.json()
    else:
        print("❌ Usuario no encontrado.")
        return None


# --------------------------
# RESERVAS
# --------------------------

def listar_reservas():
    headers = {"Accept": "application/json"}
    r = requests.get(api_reservas_url_listar, headers=headers)
    if r.status_code == 200:
        reservas = r.json()
        if not reservas:
            print("No hay reservas registradas.")
        else:
            for res in reservas:
                print(f"ID: {res.get('id')}, UsuarioID: {res.get('usuarioId')}, ViajeID: {res.get('viajeId')}, Estado: {res.get('estado')}, Fecha: {res.get('fechaReserva')}")
    else:
        print(f"❌ Error al listar reservas ({r.status_code})")


def crear_reserva():
    usuario_id = int(input("Ingrese ID del usuario: "))
    viaje_id = int(input("Ingrese ID del viaje: "))
    estado = input("Ingrese estado (pendiente/confirmada/cancelada): ")
    fecha_reserva = input("Ingrese fecha de reserva (YYYY-MM-DD): ")

    datos = {
        "usuarioId": usuario_id,
        "viajeId": viaje_id,
        "estado": estado,
        "fechaReserva": fecha_reserva
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    r = requests.post(api_reservas_url_crear, headers=headers, json=datos)
    if 200 <= r.status_code < 300:
        print("✅ Reserva creada con éxito!")
    else:
        print(f"❌ Error al crear reserva: {r.status_code}", r.text)


def actualizar_reserva():
    id = int(input("Ingrese ID de la reserva a actualizar: "))
    reserva_actual = obtener_reserva_por_id(id)
    if not reserva_actual:
        return

    usuario_id = input(f"Ingrese nuevo ID del usuario (Enter para mantener '{reserva_actual.get('usuarioId')}'): ").strip()
    viaje_id = input(f"Ingrese nuevo ID del viaje (Enter para mantener '{reserva_actual.get('viajeId')}'): ").strip()
    estado = input(f"Ingrese nuevo estado (Enter para mantener '{reserva_actual.get('estado')}'): ").strip()
    fecha_reserva = input(f"Ingrese nueva fecha de reserva (Enter para mantener '{reserva_actual.get('fechaReserva')}'): ").strip()

    datos = {
        "usuarioId": int(usuario_id) if usuario_id else reserva_actual.get("usuarioId"),
        "viajeId": int(viaje_id) if viaje_id else reserva_actual.get("viajeId"),
        "estado": estado if estado else reserva_actual.get("estado"),
        "fechaReserva": fecha_reserva if fecha_reserva else reserva_actual.get("fechaReserva")
    }

    url = f"{api_reservas_url_actualizar}/{id}"
    r = requests.put(url, headers={"Accept": "application/json", "Content-Type": "application/json"}, json=datos)
    if r.status_code == 200:
        print("✅ Reserva actualizada con éxito!")
    else:
        print(f"❌ Error al actualizar reserva: {r.status_code}", r.text)


def eliminar_reserva():
    id = int(input("Ingrese ID de la reserva a eliminar: "))
    url = f"{api_reservas_url_eliminar}/{id}"
    r = requests.delete(url)
    if r.status_code == 204:
        print("✅ Reserva eliminada con éxito!")
    elif r.status_code == 404:
        print("❌ Reserva no encontrada.")
    else:
        print(f"❌ Error al eliminar reserva: {r.status_code}", r.text)


def obtener_reserva_por_id(id: int):
    url = f"{api_reservas_url_por_id}/{id}"
    r = requests.get(url, headers={"Accept": "application/json"})
    if r.status_code == 200:
        return r.json()
    else:
        print("❌ Reserva no encontrada.")
        return None

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
        print("6. Usuarios")
        print("7. Reservas")
        print("8. Salir")
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
            menu_usuarios()  # Submenú de usuarios
        elif opcion == "7":
            menu_reservas()  # Submenú de reservas
        elif opcion == "8":
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

def menu_usuarios():
    while True:
        print("\n--- Gestión de Usuarios ---")
        print("1. Listar usuarios")
        print("2. Crear usuario")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("5. Volver")
        op = input("Seleccione una opción: ")

        if op == "1":
            listar_usuarios()
        elif op == "2":
            crear_usuario()
        elif op == "3":
            actualizar_usuario()
        elif op == "4":
            eliminar_usuario()
        elif op == "5":
            break
        else:
            print("Opción inválida.")

def menu_reservas():
    while True:
        print("\n--- Gestión de Reservas ---")
        print("1. Listar reservas")
        print("2. Crear reserva")
        print("3. Actualizar reserva")
        print("4. Eliminar reserva")
        print("5. Volver")
        op = input("Seleccione una opción: ")

        if op == "1":
            listar_reservas()
        elif op == "2":
            crear_reserva()
        elif op == "3":
            actualizar_reserva()
        elif op == "4":
            eliminar_reserva()
        elif op == "5":
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