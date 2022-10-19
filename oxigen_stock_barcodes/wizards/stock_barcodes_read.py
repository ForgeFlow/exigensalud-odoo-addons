# Copyright 2022 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models


class WizStockBarcodesRead(models.AbstractModel):
    _inherit = "wiz.stock.barcodes.read"


    def process_barcode_lot_id(self):
        # overrides method from OCA method in stock_barcodes
        if self.env.user.has_group("stock.group_production_lot"):
            # START OF CHANGES
            lot = self.env["stock.production.lot"]
            if len(self.barcode) == 6:
                lot_domain = [("nos", "=", self.barcode)]
                lot = self.env["stock.production.lot"].search(lot_domain)
            if not lot:
                lot_domain = [("name", "=", self.barcode)]
            # END OF CHANGES
            if self.product_id:
                lot_domain.append(("product_id", "=", self.product_id.id))
            lot = self.env["stock.production.lot"].search(lot_domain)
            if len(lot) == 1:
                if self.option_group_id.fill_fields_from_lot:
                    quant_domain = [
                        ("lot_id.name", "=", self.barcode),
                        ("quantity", ">", 0.0),
                    ]
                    if self.location_id:
                        quant_domain.append(("location_id", "=", self.location_id.id))
                    else:
                        quant_domain.append(("location_id.usage", "=", "internal"))
                    if self.owner_id:
                        quant_domain.append(("owner_id", "=", self.owner_id.id))
                    quants = self.env["stock.quant"].search(quant_domain)
                    if (
                        not self._name == "wiz.stock.barcodes.read.inventory"
                        and not quants
                        and not self.option_group_id.allow_negative_quant
                    ):
                        self._set_messagge_info(
                            "more_match",
                            _("No stock available for this lot with screen values"),
                        )
                        return False
                    if quants:
                        self.set_info_from_quants(quants)
                    else:
                        self.product_id = lot.product_id
                        self.action_lot_scaned_post(lot)
                    return True
                else:
                    self.product_id = lot.product_id
                    self.action_lot_scaned_post(lot)
                return True
            elif lot:
                self._set_messagge_info(
                    "more_match", _("More than one lot found\nScan product before")
                )
            elif self.product_id and self.option_group_id.create_lot:
                new_lot = self._create_new_lot(self.barcode)
                self.action_lot_scaned_post(new_lot)
                return True
        return False
