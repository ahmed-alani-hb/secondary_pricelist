app_name = "secondary_pricelist"
app_title = "Secondary Pricelist"
app_publisher = "Your Company"
app_description = "Adds secondary pricelist functionality to Sales Order"
app_icon = "fa fa-list"
app_color = "blue"
app_email = "support@yourcompany.com"
app_license = "MIT"
app_version = "1.0.0"

# Document Events
doc_events = {
    "Sales Order": {
        "before_validate": "secondary_pricelist.overrides.sales_order.before_validate",
        "validate": "secondary_pricelist.overrides.sales_order.validate_secondary_pricing"
    },
    "Sales Order Item": {
        "before_insert": "secondary_pricelist.overrides.sales_order.before_sales_order_item_insert",
        "validate": "secondary_pricelist.overrides.sales_order.validate_sales_order_item"
    }
}

# Installation hooks
after_install = "secondary_pricelist.install.after_install"

# Include CSS files
app_include_css = [
    "/assets/secondary_pricelist/css/secondary_pricelist.css"
]

# Boot session
boot_session = "secondary_pricelist.boot.boot_session"
