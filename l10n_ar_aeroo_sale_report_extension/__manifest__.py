# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    All Rights Reserved.
#
############################################################################
#
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Sale Order Report extension",
    "version": "1.0",
    'author': 'Ing. Gabriela Rivero',
    'version' : '11.0.0.0.0',
    "summary": """
        Adaptación del reporte de presupuesto/orden de venta
    """,
    "license": "AGPL-3",
    "depends": ['l10n_ar_aeroo_sale'],
    "data": [
        'sale_order_report.xml',
    ],
    'qweb': [],
    "installable": True,
    "active": False,
}
