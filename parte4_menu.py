# ==================== MENÚ INTERACTIVO ====================
def menu_interactivo(gestor):
    print("\n" + "="*70)
    print("🚀 MODO INTERACTIVO - Software FJ")
    print("="*70)
    while True:
        print("\nMenú principal:")
        print("1. Registrar nuevo cliente")
        print("2. Crear nuevo servicio")
        print("3. Crear nueva reserva")
        print("4. Confirmar reserva")
        print("5. Cancelar reserva")
        print("6. Procesar reserva")
        print("7. Mostrar todo el sistema")
        print("8. Ejecutar simulación automática otra vez")
        print("0. Salir")
       
        opcion = input("\nElige una opción (0-8): ").strip()

        if opcion == "0":
            print("👋 Gracias por usar el Sistema Software FJ. ¡Hasta pronto!")
            break

        elif opcion == "1":
            try:
                id_c = input("ID cliente: ")
                nombre = input("Nombre: ")
                email = input("Email: ")
                tel = input("Teléfono: ")
                c = Cliente(id_c, nombre, email, tel)
                gestor.registrar_cliente(c)
                print("✅ Cliente registrado")
            except Exception as e:
                logging.error(f"Error al registrar cliente: {e}")
                print(f"❌ {e}")

        elif opcion == "2":
            try:
                print("\nTipo de servicio:")
                print("1. Reserva de Sala")
                print("2. Alquiler de Equipo")
                print("3. Asesoría Especializada")
                tipo = input("Elige tipo (1-3): ").strip()

                id_s = input("ID servicio: ")
                nombre = input("Nombre del servicio: ")
                precio = float(input("Precio base: "))

                if tipo == "1":
                    cap = int(input("Capacidad de la sala: "))
                    serv = ReservaSala(id_s, nombre, precio, cap)
                elif tipo == "2":
                    tipo_eq = input("Tipo de equipo: ")
                    serv = AlquilerEquipo(id_s, nombre, precio, tipo_eq)
                elif tipo == "3":
                    esp = input("Especialidad: ")
                    serv = AsesoriaEspecializada(id_s, nombre, precio, esp)
                else:
                    print("❌ Tipo inválido")
                    continue

                gestor.crear_servicio(serv)
                print("✅ Servicio creado correctamente")
            except Exception as e:
                logging.error(f"Error al crear servicio: {e}")
                print(f"❌ {e}")

        elif opcion == "3":
            try:
                id_r = input("ID reserva: ")
                id_cliente = input("ID del cliente: ")
                cliente = gestor.buscar_cliente(id_cliente)
                if not cliente:
                    print("❌ Cliente no encontrado")
                    continue

                id_servicio = input("ID del servicio: ")
                servicio = gestor.buscar_servicio(id_servicio)
                if not servicio:
                    print("❌ Servicio no encontrado")
                    continue

                duracion = float(input("Duración en horas: "))

                parametros = {}
                if isinstance(servicio, ReservaSala):
                    num_personas = int(input("Número de personas: "))
                    parametros['numero_personas'] = num_personas

                r = Reserva(id_r, cliente, servicio, duracion, **parametros)
                gestor.crear_reserva(r)
                print("✅ Reserva creada correctamente")
            except Exception as e:
                logging.error(f"Error al crear reserva: {e}")
                print(f"❌ {e}")

        elif opcion in ["4", "5", "6"]:
            try:
                id_r = input("ID de la reserva: ")
                reserva = gestor.buscar_reserva(id_r)
                if not reserva:
                    print("❌ Reserva no encontrada")
                    continue

                if opcion == "4":
                    reserva.confirmar()
                    print("✅ Reserva confirmada")
                elif opcion == "5":
                    reserva.cancelar()
                    print("✅ Reserva cancelada")
                elif opcion == "6":
                    reserva.procesar()
                    print("✅ Reserva procesada")
            except Exception as e:
                logging.error(f"Error en operación de reserva: {e}")
                print(f"❌ {e}")

        elif opcion == "7":
            gestor.listar_todo()
        elif opcion == "8":
            simulacion_automatica(gestor)
        else:
            print("❌ Opción inválida")
