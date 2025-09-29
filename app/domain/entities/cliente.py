from typing import Optional


class Cliente:
    def __init__(self, idcliente=None, cif=None, cif_empresa=None, razsoc=None, direccion=None, localidad=None, provincia=None, cpostal=None, codigop=None, pais=None, cif_factura=None):
        self.idcliente = idcliente
        self.cif = cif
        self.cif_empresa = cif_empresa
        self.razsoc = razsoc
        self.direccion = direccion
        self.localidad = localidad
        self.provincia = provincia
        self.cpostal = cpostal
        self.codigop = codigop
        self.pais = pais
        self.cif_factura = cif_factura
