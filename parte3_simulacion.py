# Sebastian Benito Garzon

def simulacion_automatica(gestor):
    print("Ejecutando simulacion automatica de 11 operaciones (obligaorio).../n")

    # op1: Cliente válido
    try:
        c1 = cliente("C001", "Juan Perez", "Juan@email.com", "3101234567")
        gestor.registrar_cliente(c1)
        print("✅ Operacion 1: cliente valido registrado")
    except Exception as e:
        print(f"❌ Op1: {e}")

    # op2: cliente invalido
    try:
        Cliente("C002", "", "mal@.com", "123")
    except DatosInvalidosError as e:
        logging.error(f"Error controlado (cliente invalido): {e}")
        print(f"✅ Operación 2: Error controlado (cliente inválido): {e}")
      
    # Op3-5: Servicios
    try:
        sala = ReservaSala("S001", "Sala Ejecutiva", 120.0, 20)
        gestor.crear_servicio(sala)
        equipo 0 AlquilarEquipo("S002", "Laptop", 80.0, "Dell XPS")
        gestor.crear_servicio(equipo)
        asesoria = AsesoriaEspecializada("S003", "Python OOP", 250.0, "Prograacion Avanzada")
        gestor.crear_servicio(asesoria)
        print("✅ Operaciones 3-5: Servicios creados correctamente")
    except Exception as e:
        print(f"❌ Op3-5: {e}")

    # Op6: Reserva exitosa
    try:
        r1 = Reserva("R001", c1, sala, 5.0, numero_personas=12)
        gestor.crear_reserva(r1)
        r1.confirmar()
        r1.procesar()
        print("✅ Operación 6: Reserva exitosa procesada")
    except Exception as e:
        logging.error(f"Error Op6: {e}")
        print(f"❌ Op6: {e}")

    # Op7: Reserva inválida
    try:
        Reserva("R002", c1, sala, -1.0)
    except ReservaInvalidaError as e:
        logging.error(f"Error controlado Op7: {e}")
        print(f"✅ Operación 7: Error controlado (reserva inválida): {e}")

    # Op8: Cancelar reserva ya procesada
    try:
        r1.cancelar()
    except OperacionNoPermitidaError as e:
        logging.error(f"Error controlado Op8: {e}")
        print(f"✅ Operación 8: Error controlado (cancelación no permitida): {e}")

    # Op9: Manejo avanzado de excepciones
    print("\n--- Operación 9: Manejo avanzado de excepciones (try/except/else/finally + encadenamiento) ---")
    try:
        try:
            resultado = 100 / 0
        except ZeroDivisionError as e:
            logging.error(f"Error interno Op9: {e}")
            raise OperacionNoPermitidaError("Error en cálculo de costos") from e
    except OperacionNoPermitidaError as e:
        logging.error(f"Error controlado Op9 (encadenada): {e}")
        print(f"✅ Operación 9: Excepción encadenada capturada: {e}")
    else:
        print("✅ Bloque else Op9")
    finally:
        print("✅ Bloque finally Op9: Siempre se ejecuta")

    # Op10: Reserva de asesoría
    try:
        r2 = Reserva("R003", c1, asesoria, 3.0)
        gestor.crear_reserva(r2)
        r2.confirmar()
        r2.procesar()
        print("✅ Operación 10: Reserva de asesoría exitosa")
    except Exception as e:
        logging.error(f"Error Op10: {e}")
        print(f"❌ Op10: {e}")

    # Op11: Mostrar estado final
    gestor.listar_todo()
    print("\n✅ Simulación de 11 operaciones completada correctamente."
