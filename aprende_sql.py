from odoo import models, fields

class InvoiceSalePaymentView(models.Model):
    _name = "invoice.sale.payment.view"  # Nombre del modelo en Odoo
    _description = "Vista que consolida facturas, ventas y pagos"
    _auto = False  # Indica que no es una tabla real
    _table_query = """
        SELECT 
    am.id AS id,  
    am.name AS factura,  
    so.name AS orden_venta,  
    am.partner_id AS cliente_id,  
    am.amount_total AS total_factura,  
    am.state AS estado_factura,  
    COALESCE(SUM(ap.amount), 0) AS total_pagado  
FROM account_move am
LEFT JOIN sale_order so ON am.invoice_origin = so.name
LEFT JOIN account_move_line aml ON aml.move_id = am.id  
LEFT JOIN account_partial_reconcile apr ON apr.debit_move_id = aml.id  
LEFT JOIN account_move_line aml_pago ON aml_pago.id = apr.credit_move_id  
LEFT JOIN account_payment ap ON ap.id = aml_pago.payment_id  
WHERE am.state = 'posted'
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
