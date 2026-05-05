import abc
from abc import ABC, abstractmethod
import logging
from typing import List, Optional

# ==================== CONFIGURACIÓN DE LOGS ====================
logging.basicConfig(
    filename='logs_eventos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    force=True
)

# ==================== EXCEPCIONES PERSONALIZADAS ====================
class DatosInvalidosError(Exception):
    pass
class OperacionNoPermitidaError(Exception):
    pass
class ReservaInvalidaError(Exception):
    pass
class ServicioNoDisponibleError(Exception):
    pass

# ==================== CLASE ABSTRACTA GENERAL ====================
class EntidadAbstracta(ABC):
    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad
   
    @abstractmethod
    def validar(self) -> bool:
        pass
   
    def __str__(self):
        return f"Entidad ID: {self._id_entidad}"

# ==================== CLASE CLIENTE ====================
class Cliente(EntidadAbstracta):
    def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str):
        super().__init__(id_cliente)
        self.__nombre = nombre
        self.__email = email
        self.__telefono = telefono
        self.validar()
   
    def validar(self) -> bool:
        if not self.__nombre or "@" not in self.__email or len(str(self.__telefono)) < 7:
            logging.error(f"Datos inválidos para cliente {self._id_entidad}")
            raise DatosInvalidosError("Datos del cliente inválidos: nombre vacío, email incorrecto o teléfono inválido")
        logging.info(f"Cliente validado correctamente: {self.__nombre} (ID: {self._id_entidad})")
        return True

    def get_nombre(self): return self.__nombre
    def get_email(self): return self.__email
    def get_telefono(self): return self.__telefono
   
    def __str__(self):
        return f"Cliente: {self.get_nombre()} (ID: {self._id_entidad})"

# ==================== CLASE ABSTRACTA SERVICIO ====================
class Servicio(EntidadAbstracta):
    def __init__(self, id_servicio: str, nombre: str, precio_base: float):
        super().__init__(id_servicio)
        self._nombre = nombre
        self._precio_base = precio_base
        self.validar()

    def validar(self) -> bool:
        if not self._nombre or self._precio_base <= 0:
            logging.error(f"Datos inválidos para servicio {self._id_entidad}")
            raise DatosInvalidosError("Nombre del servicio vacío o precio base inválido")
        logging.info(f"Servicio validado: {self._nombre} (ID: {self._id_entidad})")
        return True

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio_base(self):
        return self._precio_base

    @abstractmethod
    def calcular_costo(self, duracion: float) -> float:
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    def validar_parametros(self, **kwargs) -> bool:
        return True

    def calcular_costo_con_impuestos(self, duracion: float, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        costo_base = self.calcular_costo(duracion)
        costo_final = costo_base * (1 + impuesto)
        if descuento > 0:
            costo_final *= (1 - descuento)
        return round(costo_final, 2)

# ==================== SERVICIOS ESPECIALIZADOS ====================
class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, precio_base: float, capacidad: int):
        super().__init__(id_servicio, nombre, precio_base)
        self._capacidad = capacidad

    @property
    def capacidad(self):
        return self._capacidad

    def calcular_costo(self, duracion: float) -> float:
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor a cero")
        return self._precio_base * duracion

    def describir_servicio(self) -> str:
        return f"Reserva de sala '{self.nombre}' (capacidad: {self.capacidad} personas)"

    def validar_parametros(self, **kwargs) -> bool:
        numero_personas = kwargs.get('numero_personas')
        if numero_personas is not None and numero_personas > self.capacidad:
            raise ReservaInvalidaError(f"El número de personas ({numero_personas}) excede la capacidad de la sala ({self.capacidad})")
        return True

class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, precio_base: float, tipo_equipo: str):
        super().__init__(id_servicio, nombre, precio_base)
        self._tipo_equipo = tipo_equipo

    @property
    def tipo_equipo(self):
        return self._tipo_equipo

    def calcular_costo(self, duracion: float) -> float:
        return self._precio_base * duracion * 1.1

    def describir_servicio(self) -> str:
        return f"Alquiler de equipo '{self.tipo_equipo}'"

class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, nombre: str, precio_base: float, especialidad: str):
        super().__init__(id_servicio, nombre, precio_base)
        self._especialidad = especialidad

    @property
    def especialidad(self):
        return self._especialidad

    def calcular_costo(self, duracion: float) -> float:
        return self._precio_base + (duracion * 50)

    def describir_servicio(self) -> str:
        return f"Asesoría especializada en {self.especialidad}"

# ==================== CLASE RESERVA ====================
class Reserva:
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, 
                 duracion: float, **parametros_extra):
        if not isinstance(cliente, Cliente):
            raise TypeError("El cliente debe ser una instancia de la clase Cliente")
        if not isinstance(servicio, Servicio):
            raise TypeError("El servicio debe ser una instancia de la clase Servicio")

        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "pendiente"
        self.validar_reserva(**parametros_extra)

    def validar_reserva(self, **parametros_extra):
        if self.duracion <= 0:
            raise ReservaInvalidaError("La duración de la reserva debe ser mayor a cero")
        self.servicio.validar_parametros(**parametros_extra)

    def confirmar(self):
        if self.estado != "pendiente":
            raise OperacionNoPermitidaError("No se puede confirmar una reserva que no está pendiente")
        self.estado = "confirmada"
        logging.info(f"Reserva {self.id_reserva} CONFIRMADA exitosamente")

    def cancelar(self):
        if self.estado == "procesada":
            raise OperacionNoPermitidaError("No se puede cancelar una reserva ya procesada")
        self.estado = "cancelada"
        logging.info(f"Reserva {self.id_reserva} CANCELADA")

    def procesar(self):
        if self.estado != "confirmada":
            raise OperacionNoPermitidaError("La reserva debe estar confirmada antes de procesarla")
        self.estado = "procesada"
        costo = self.servicio.calcular_costo_con_impuestos(self.duracion, descuento=0.05)
        logging.info(f"Reserva {self.id_reserva} PROCESADA. Costo final: ${costo}")

    def __str__(self):
        return f"Reserva {self.id_reserva} | {self.cliente.get_nombre()} | {self.servicio.nombre} | Estado: {self.estado}"
