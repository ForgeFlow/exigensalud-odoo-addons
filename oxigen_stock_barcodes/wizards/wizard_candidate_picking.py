# Copyright 2022 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models


class WizCandidatePicking(models.TransientModel):
    _inherit = "wiz.candidate.picking"

    def action_confirm_picking(self):
        picking = self.env["stock.picking"].browse(
            self.env.context.get("picking_id", False)
        )
        picking.action_confirm()
        return self.env.ref("stock_barcodes.action_stock_barcodes_action").read()[0]
