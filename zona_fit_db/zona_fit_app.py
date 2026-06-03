print('*** Clientes Zona Fit ***')

opcion = None

while opcion != '5':
    print('1. Listar clientes')
    print('2. Agregar cliente')
    print('3. Actualizar cliente')
    print('4. Eliminar cliente')
    print('5. Salir')

    opcion = input('Seleccione una opción: ')

    if opcion == '1':
        from cliente_dao import ClienteDAO

        clientes = ClienteDAO.seleccionar()
        for cliente in clientes:
            print(cliente)
    elif opcion == '2':
        from cliente import Cliente
        from cliente_dao import ClienteDAO

        nombre = input('Ingrese el nombre del cliente: ')
        apellido = input('Ingrese el apellido del cliente: ')
        membresia = input('Ingrese la membresía del cliente: ')
        nuevo_cliente = Cliente(nombre=nombre, apellido=apellido, membresia=membresia)
        resultado = ClienteDAO.insertar(nuevo_cliente)
        print(f'Clientes insertados: {resultado}')
    elif opcion == '3':
        from cliente import Cliente
        from cliente_dao import ClienteDAO

        id_cliente = input('Ingrese el ID del cliente a actualizar: ')
        nombre = input('Ingrese el nuevo nombre del cliente: ')
        apellido = input('Ingrese el nuevo apellido del cliente: ')
        membresia = input('Ingrese la nueva membresía del cliente: ')
        cliente_actualizado = Cliente(id=id_cliente, nombre=nombre, apellido=apellido, membresia=membresia)
        resultado = ClienteDAO.actualizar(cliente_actualizado)
        print(f'Clientes actualizados: {resultado}')
    elif opcion == '4':
        from cliente import Cliente
        from cliente_dao import ClienteDAO

        id_cliente = input('Ingrese el ID del cliente a eliminar: ')
        cliente_a_eliminar = Cliente(id=id_cliente)
        resultado = ClienteDAO.eliminar(cliente_a_eliminar)
        print(f'Clientes eliminados: {resultado}')
    elif opcion == '5':
        print('Saliendo del programa...')
    else:
        print('Opción no válida. Por favor, seleccione una opción del 1 al 5.')