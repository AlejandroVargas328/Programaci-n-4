# ==================== GESTOR DEL SISTEMA ====================
class GestorSistema:
    def _init_(self):
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []

    def registrar_cliente(self, cliente: Cliente):
        self.clientes.append(cliente)
        logging.info(f"Cliente registrado: {cliente}")

    def crear_servicio(self, servicio: Servicio):
        self.servicios.append(servicio)
        logging.info(f"Servicio creado: {servicio.describir_servicio()}")

    def crear_reserva(self, reserva: Reserva):
        self.reservas.append(reserva)
        logging.info(f"Reserva creada: {reserva}")

    def buscar_cliente(self, id_cliente: str) -> Optional[Cliente]:
        for c in self.clientes:
            if c._id_entidad == id_cliente:
                return c
        return None

    def buscar_servicio(self, id_servicio: str) -> Optional[Servicio]:
        for s in self.servicios:
            if s._id_entidad == id_servicio:
                return s
        return None

    def buscar_reserva(self, id_reserva: str) -> Optional[Reserva]:
        for r in self.reservas:
            if r.id_reserva == id_reserva:
                return r
        return None

    def listar_todo(self):
        print("\n=== CLIENTES REGISTRADOS ===")
        for c in self.clientes: 
            print(c)
        print("\n=== SERVICIOS DISPONIBLES ===")
        for s in self.servicios: 
            print(s.describir_servicio())
        print("\n=== RESERVAS REALIZADAS ===")
        for r in self.reservas: 
            print(r)
