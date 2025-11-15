plantilla_ticket = """
========================================
              SERVISUR
        Comprobante de Reparación
========================================

Nombre:        {nombre}
RUT:           {rut}
Teléfono:      {telefono}
Fecha:         {fecha}

----------------------------------------
Equipo
----------------------------------------
Marca:         {marca}
Modelo:        {modelo}
Tipo de falla: {falla}

----------------------------------------
Detalle de Pago
----------------------------------------
Total a pagar: ${total}
Abono:         ${abono}
Restante:      ${restante}

----------------------------------------
Observaciones:
{observaciones}

----------------------------------------
Firma Cliente: _________________________

========================================
        ¡Gracias por su preferencia!
========================================
"""

print(plantilla_ticket.format(
    nombre="Kevin Fuenmayor",
    rut="9098749-8",
    telefono="+56994160745",
    fecha="14/11/2025",
    marca="Samsung",
    modelo="Galaxy A51",
    falla="Pantalla rota",
    total="60000",
    abono="40000",
    restante="20000",
    observaciones="Entrega estimada en 3 días"
))