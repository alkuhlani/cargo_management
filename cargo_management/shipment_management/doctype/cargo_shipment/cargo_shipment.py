import frappe
from cargo_management.utils import get_list_from_child_table
from frappe.model.document import Document


class CargoShipment(Document):

    def on_update(self):
        """ Add Departure Date to all Warehouse Receipt Linked """
        # TODO: What if cargo shipment is deleted?

        # TODO: Validate if any problem!
        frappe.db.sql("""
            UPDATE tabPackage
            SET cargo_shipment = %(cs_name)s
            WHERE `name` IN %(packages)s AND COALESCE(cargo_shipment, '') != %(cs_name)s
        """, {
            'cs_name': self.name,
            'packages': get_list_from_child_table(self.cargo_shipment_lines, 'package')
        })

        wrs_in_cs = get_list_from_child_table(self.cargo_shipment_lines, 'warehouse_receipt')
        if wrs_in_cs:  # If empty we don't touch the DB  # FIXME: Performance?
            frappe.db.sql("UPDATE `tabWarehouse Receipt` SET departure_date = %(date)s WHERE name IN %(wrs_in_cs)s", {
                'date': self.departure_date, 'wrs_in_cs': wrs_in_cs
            })

    def change_status(self, new_status):
        """ Validates the current status of the cargo shipment and change it if it's possible. """
        # TODO: Validate this when status is changed on Form-View or List-View

        # TODO: Finish
        if self.status != new_status and \
                (self.status == 'Awaiting Departure' and new_status == 'In Transit') or \
                (self.status in ['Awaiting Departure', 'In Transit'] and new_status == 'Sorting') or \
                (self.status == 'Sorting' and new_status =='Finished'):
            self.status = new_status
            return True

        return False
