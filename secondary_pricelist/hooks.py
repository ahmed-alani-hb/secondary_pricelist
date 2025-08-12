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

# Fixtures
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["name", "in", [
                "Sales Order-custom_secondary_pricelist",
                "Sales Order-custom_enable_secondary_pricing"
            ]]
        ]
    }
]

# Include JS/CSS files
app_include_js = [
    "/assets/secondary_pricelist/js/sales_order_secondary_pricelist.js"
]

app_include_css = [
    "/assets/secondary_pricelist/css/secondary_pricelist.css"
]