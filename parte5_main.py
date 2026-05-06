# ==================== MAIN ====================
def main():
    print("=== SISTEMA INTEGRAL DE GESTIÓN - Software FJ ===\n")
    gestor = GestorSistema()
   
    # Simulación obligatoria
    simulacion_automatica(gestor)
   
    # Menú interactivo opcional
    respuesta = input("\n¿Desea entrar al modo interactivo? (s/n): ").strip().lower()
    if respuesta == "s":
        menu_interactivo(gestor)
    else:
        print("✅ Ejecución finalizada. ¡Gracias!")

if __name__ == "__main__":
    main()
