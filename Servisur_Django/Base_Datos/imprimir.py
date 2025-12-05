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

def Rellenar(nombre,rut,telefono,fecha,marca,modelo,falla,total,abono,restante,observaciones):
    print(plantilla_ticket.format(
    nombre,rut,telefono,fecha,
    marca,modelo,falla,total,
    abono,restante,observaciones
))



