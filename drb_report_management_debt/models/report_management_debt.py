# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools

class DrbReportManagementDebt(models.Model):
    _name = 'drb.report.management.debt'
    _auto = False
    _description='Drb Report Management Debt'

    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
    )
    #sale order
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        readonly=True
    )
    sale_order = fields.Many2one(
        'sale.order',
        string='Sale Order'
    )
    confirmation_date = fields.Datetime(
        string='Confirmation Date',
        readonly=True,
    )
    commitment_date = fields.Datetime(
        string='Commitment Date', store=True,
        readonly=True
    )
    amount_untaxed = fields.Monetary(
        string='Amount Untaxed',
        currency_field='company_currency_id',
    )
    amount_total = fields.Monetary(
        string='Amount Total',
        currency_field='company_currency_id',
    )
    
    #invoice
    account_invoice = fields.Many2one(
        'account.invoice',
        string='Account Invoice'
    )
    invoice_amount_total = fields.Monetary(
        string='Invoice Total Amount',
        currency_field='company_currency_id',
    )
    residual = fields.Monetary(
        string='Residual Amount',
        currency_field='company_currency_id',
    )

    #payment
    payment = fields.Many2one(
        'account.payment',
        string='Payment'
    )
    payment_amount = fields.Monetary(
        string='Residual Amount',
        currency_field='company_currency_id',
    )
    payment_date = fields.Date(
        string='Date'
    )
    

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'drb_report_management_debt')
        self._cr.execute("""
            CREATE OR REPLACE VIEW drb_report_management_debt AS (
                SELECT row_number() OVER () AS id,
                    ai.currency_id as company_currency_id,
                    so.partner_id as partner_id,
                    so.id as sale_order,
                    so.confirmation_date,
                    so.commitment_date,
                    so.amount_untaxed,
                    so.amount_total,
                    ai.id as account_invoice,
                    ai.amount_total as invoice_amount_total,
                    ai.residual as residual,
 					ap.id as payment,
 					ap.amount as payment_amount,
 					ap.payment_date as payment_date			
                FROM  sale_order as so
				LEFT JOIN account_invoice as ai ON (ai.origin = so.name AND ai.state in ('open','paid') )
 				RIGHT JOIN account_move_line as aml ON (aml.invoice_id = ai.id and product_id > 0)
  				LEFT JOIN account_payment as ap ON (so.partner_id = ap.partner_id AND ap.state in ('posted'))
 				WHERE so.state in ('sale')
            )"""
        )