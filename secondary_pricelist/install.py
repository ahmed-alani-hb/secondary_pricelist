import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    """
    Install custom fields after app installation
    """
    create_custom_fields_for_secondary_pricelist()

def create_custom_fields_for_secondary_pricelist():
    """
    Create custom fields for Secondary Pricelist functionality
    """
    custom_fields = {
        "Sales Order": [
            {
                "fieldname": "custom_enable_secondary_pricing",
                "fieldtype": "Check",
                "label": "Enable Secondary Pricing",
                "insert_after": "selling_price_list",
                "default": "1",
                "description": "Enable automatic fallback to secondary pricelist when primary pricelist has no price",
                "allow_on_submit": 0,
                "bold": 0,
                "collapsible": 0,
                "depends_on": "",
                "hidden": 0,
                "ignore_user_permissions": 0,
                "ignore_xss_filter": 0,
                "in_global_search": 0,
                "in_list_view": 0,
                "in_preview": 0,
                "in_standard_filter": 0,
                "mandatory_depends_on": "",
                "no_copy": 0,
                "permlevel": 0,
                "print_hide": 0,
                "read_only": 0,
                "read_only_depends_on": "",
                "report_hide": 0,
                "reqd": 0,
                "search_index": 0,
                "translatable": 0,
                "unique": 0
            },
            {
                "fieldname": "custom_secondary_pricelist",
                "fieldtype": "Link",
                "label": "Secondary Price List",
                "options": "Price List",
                "insert_after": "custom_enable_secondary_pricing",
                "depends_on": "custom_enable_secondary_pricing",
                "description": "Fallback price list when primary price list has no pricing",
                "allow_on_submit": 0,
                "bold": 0,
                "collapsible": 0,
                "hidden": 0,
                "ignore_user_permissions": 0,
                "ignore_xss_filter": 0,
                "in_global_search": 0,
                "in_list_view": 0,
                "in_preview": 0,
                "in_standard_filter": 0,
                "mandatory_depends_on": "",
                "no_copy": 0,
                "permlevel": 0,
                "print_hide": 0,
                "read_only": 0,
                "read_only_depends_on": "",
                "report_hide": 0,
                "reqd": 0,
                "search_index": 0,
                "translatable": 0,
                "unique": 0
            }
        ]
    }
    
    create_custom_fields(custom_fields, update=True)