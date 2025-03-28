from odoo import models, fields

class InvoiceSalePaymentView(models.Model):
    _name = "invoice.sale.payment.view"  # Nombre del modelo en Odoo
    _description = "Vista que consolida facturas, ventas y pagos"
    _auto = False  # Indica que no es una tabla real
    _table_query = """
        SELECT 
            am.id AS id,  -- Identificador único de la factura
            am.name AS factura,  -- Número de la factura
            so.name AS orden_venta,  -- Nombre de la orden de venta
            am.partner_id AS cliente_id,  -- Cliente relacionado
            am.amount_total AS total_factura,  -- Total de la factura
            am.state AS estado_factura,  -- Estado de la factura
            COALESCE(SUM(ap.amount), 0) AS total_pagado  -- Total pagado, evitando valores NULL
        FROM account_move am
        LEFT JOIN sale_order so ON am.invoice_origin = so.name
        LEFT JOIN account_payment ap ON am.id = ap.reconciled_invoice_id
        GROUP BY am.id, so.name, am.partner_id, am.amount_total, am.state
    """

    # Definimos los campos en Odoo
    factura = fields.Char(string="Factura")
    orden_venta = fields.Char(string="Orden de Venta")
    cliente_id = fields.Many2one("res.partner", string="Cliente")
    total_factura = fields.Monetary(string="Total Factura")
    estado_factura = fields.Selection(
        [('draft', 'Borrador'), ('posted', 'Publicado'), ('cancel', 'Cancelado')],
        string="Estado de Factura"
    )
    total_pagado = fields.Monetary(string="Total Pagado")
    currency_id = fields.Many2one("res.currency", string="Moneda")  # Necesario para campos monetarios
