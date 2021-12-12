# Copyright 2021 jeo Software Jorge Obiols <jorge.obiols@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

#   Para correr los tests
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben enpezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos para testing como sigue:
#   - Nombre sugerido: [nombre cliente]_test
#   - Debe ser creada con Load Demostration Data chequeado
#   - Usuario admin y password admin
#   - El modulo que se quiere testear debe estar instalado.
#
#   Arrancar el test con:
#
#   oe -Q ea_website_price -c ea -d ea_test
#
from odoo.tests.common import TransactionCase

class DocumentTestCase(TransactionCase):

    def test_01_check_prices(self):
        """ Testear los precios
        """
        # Tomar un producto de los datos de test.
        domain = [('default_code', '=', 'E-COM08')]
        product_id = self.env['product.product'].search(domain)

        list_price = 200

        product_id.list_price = list_price
        self.assertEqual(product_id.website_price, list_price * 0.5 * 1.21)
        self.assertEqual(product_id.website_public_price, list_price * 1.21)
        self.assertEqual(product_id.website_price_difference, True)

        product_id.list_price = 100
        self.assertEqual(product_id.website_price, list_price * 0.5 * 1.21)
        self.assertEqual(product_id.website_public_price, list_price * 1.21)
        self.assertEqual(product_id.website_price_difference, True)

        product_id.list_price = 50
        self.assertEqual(product_id.website_price, list_price * 0.5 * 1.21)
        self.assertEqual(product_id.website_public_price, list_price * 1.21)
        self.assertEqual(product_id.website_price_difference, True)

        product_id.list_price = 10
        self.assertEqual(product_id.website_price, list_price * 0.5 * 1.21)
        self.assertEqual(product_id.website_public_price, list_price * 1.21)
        self.assertEqual(product_id.website_price_difference, True)
