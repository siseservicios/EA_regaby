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
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        readonly=True,
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
        readonly=True,
    )
    amount_total = fields.Monetary(
        string='Amount Total',
        currency_field='company_currency_id',
        readonly=True,
    )

    #invoice
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Account Invoice',
        readonly=True,
    )
    invoice_amount_total = fields.Monetary(
        string='Invoice Total Amount',
        currency_field='company_currency_id',
        readonly=True,
    )

    balance_to_billed = fields.Monetary(
        string='Balance to Billed',
        currency_field='company_currency_id',
        default = 0,
        store=True,
        readonly=True,
    )

    #payment
    payment_id = fields.Many2one(
        'account.payment',
        string='Payment',
        readonly=True,
    )
    payment_amount = fields.Monetary(
        string='Payment Amount',
        currency_field='company_currency_id',
        readonly=True,
    )
    total_payment_amount = fields.Monetary(
        string='Total Payment Amount',
        currency_field='company_currency_id',
        readonly=True,
    )
    payment_date = fields.Date(
        string='Date',
        readonly=True,
    )

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'drb_report_management_debt')
        self._cr.execute("""
            CREATE OR REPLACE VIEW drb_report_management_debt AS (
                (SELECT coalesce(so.partner_id,0)+coalesce(so.id, 0)+coalesce(ai.id, 0)+coalesce(ap.id,0) id,
                    ai.currency_id as company_currency_id,
                    so.partner_id as partner_id,
                    so.id as sale_order_id,
                    so.confirmation_date,
                    so.commitment_date,
                    so.amount_untaxed as amount_untaxed,
                    so.amount_total,
                    ai.id as invoice_id,
                    ai.amount_total as invoice_amount_total,
                    (so.amount_total - ai.amount_total) as balance_to_billed,
                    ai.residual as residual,
 					ap.id as payment_id,
 					ap.amount as payment_amount,
                    (so.amount_total - ap.amount) as total_payment_amount,
 					ap.payment_date as payment_date
                FROM  sale_order as so
				LEFT JOIN account_invoice as ai ON (ai.origin = so.name AND ai.state in ('open','paid') )
 				left join account_invoice_payment_rel inv_pay on (ai.id=inv_pay.invoice_id)
				left join account_payment ap on (inv_pay.payment_id=ap.id)
 				WHERE so.state in ('sale'))
                UNION
                (select coalesce(ap.partner_id) + coalesce(ap.id) + 50000,
                ap.currency_id as company_currency_id,
                ap.partner_id as partner_id,
                    null as sale_order_id,
                    null as confirmation_date,
                    null as commitment_date,
                    null as amount_untaxed,
                    null as amount_total,
                    null as invoice_id,
                    null as invoice_amount_total,
                    null as balance_to_billed,
                    null as  residual,
 					ap.id as payment_id,
 					ap.amount as payment_amount,
 					null as total_payment_amount,
 					ap.payment_date as payment_date
                from account_payment ap
				join res_partner rp on (ap.partner_id = rp.id)
				where ap.id not in (select payment_id from account_invoice_payment_rel))
            )"""
        )