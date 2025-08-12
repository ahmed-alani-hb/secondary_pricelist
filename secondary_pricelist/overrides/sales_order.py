import frappe
from frappe import _
from frappe.utils import flt, nowdate
from erpnext.setup.utils import get_exchange_rate
from erpnext.stock.get_item_details import get_item_details

def before_validate(doc, method):
    """Process secondary pricing before validation"""
    if not doc.get("custom_enable_secondary_pricing") or not doc.get("custom_secondary_pricelist"):
        return
    
    process_secondary_pricing(doc)

def validate_secondary_pricing(doc, method):
    """Validate secondary pricing logic"""
    if not doc.get("custom_enable_secondary_pricing"):
        return
    
    # Ensure secondary pricelist is different from primary
    if doc.get("custom_secondary_pricelist") == doc.get("selling_price_list"):
        frappe.throw(_("Secondary Price List cannot be the same as Primary Price List"))

def before_sales_order_item_insert(doc, method):
    """Handle item insertion with secondary pricing"""
    if hasattr(doc, "parent_doc") and doc.parent_doc:
        parent = doc.parent_doc
        if parent.get("custom_enable_secondary_pricing") and parent.get("custom_secondary_pricelist"):
            apply_secondary_pricing_to_item(doc, parent)

def validate_sales_order_item(doc, method):
    """Validate sales order item with secondary pricing"""
    pass

def process_secondary_pricing(sales_order):
    """
    Process all items in sales order for secondary pricing
    """
    if not sales_order.get("items"):
        return
    
    primary_pricelist = sales_order.get("selling_price_list")
    secondary_pricelist = sales_order.get("custom_secondary_pricelist")
    
    if not primary_pricelist or not secondary_pricelist:
        return
    
    # Get primary and secondary pricelist currencies
    primary_currency = frappe.db.get_value("Price List", primary_pricelist, "currency")
    secondary_currency = frappe.db.get_value("Price List", secondary_pricelist, "currency")
    
    for item in sales_order.items:
        if should_apply_secondary_pricing(item, primary_pricelist):
            apply_secondary_pricing_to_item(item, sales_order, secondary_pricelist, 
                                          primary_currency, secondary_currency)

def should_apply_secondary_pricing(item, primary_pricelist):
    """
    Check if secondary pricing should be applied to an item
    """
    # If item already has a rate, don't override
    if flt(item.rate) > 0:
        return False
    
    # Check if price exists in primary pricelist
    primary_price = get_item_price_from_pricelist(item.item_code, primary_pricelist, 
                                                item.uom, item.qty)
    
    return not primary_price or flt(primary_price.get("price_list_rate", 0)) == 0

def apply_secondary_pricing_to_item(item, sales_order, secondary_pricelist=None, 
                                  primary_currency=None, secondary_currency=None):
    """
    Apply secondary pricing to a specific item
    """
    if not secondary_pricelist:
        secondary_pricelist = sales_order.get("custom_secondary_pricelist")
    
    if not secondary_pricelist:
        return
    
    # Get currencies if not provided
    if not primary_currency:
        primary_currency = frappe.db.get_value("Price List", 
                                             sales_order.get("selling_price_list"), "currency")
    if not secondary_currency:
        secondary_currency = frappe.db.get_value("Price List", secondary_pricelist, "currency")
    
    # Get price from secondary pricelist
    secondary_price = get_item_price_from_pricelist(item.item_code, secondary_pricelist,
                                                  item.uom, item.qty)
    
    if secondary_price and flt(secondary_price.get("price_list_rate", 0)) > 0:
        rate = flt(secondary_price.get("price_list_rate"))
        
        # Convert currency if needed
        if secondary_currency != primary_currency:
            rate = convert_currency_rate(rate, secondary_currency, primary_currency, 
                                       sales_order.transaction_date)
        
        # Apply the rate
        item.rate = rate
        item.price_list_rate = rate
        item.base_rate = flt(rate * flt(sales_order.conversion_rate))
        item.base_price_list_rate = flt(rate * flt(sales_order.conversion_rate))
        
        # Add comment to track secondary pricing
        item.add_comment("Info", 
            f"Price applied from secondary pricelist: {secondary_pricelist} "
            f"(Original: {secondary_price.get('price_list_rate')} {secondary_currency}, "
            f"Converted: {rate} {primary_currency})")

def get_item_price_from_pricelist(item_code, price_list, uom=None, qty=1):
    """
    Get item price from specific pricelist
    """
    try:
        # Use ERPNext's standard method to get item price
        args = {
            "item_code": item_code,
            "price_list": price_list,
            "uom": uom,
            "qty": qty,
            "transaction_date": nowdate()
        }
        
        price_data = frappe.get_all("Item Price",
            filters={
                "item_code": item_code,
                "price_list": price_list,
                "selling": 1
            },
            fields=["price_list_rate", "uom", "min_qty", "valid_from", "valid_upto"],
            order_by="valid_from desc, creation desc",
            limit=1
        )
        
        if price_data:
            price = price_data[0]
            # Check validity dates
            if is_price_valid(price):
                return price
        
        return None
        
    except Exception as e:
        frappe.log_error(f"Error getting price for {item_code} from {price_list}: {str(e)}")
        return None

def is_price_valid(price_data):
    """
    Check if price is valid based on dates
    """
    from frappe.utils import getdate
    
    today = getdate()
    valid_from = price_data.get("valid_from")
    valid_upto = price_data.get("valid_upto")
    
    if valid_from and getdate(valid_from) > today:
        return False
    
    if valid_upto and getdate(valid_upto) < today:
        return False
    
    return True

def convert_currency_rate(rate, from_currency, to_currency, transaction_date):
    """
    Convert rate from one currency to another
    """
    if from_currency == to_currency:
        return rate
    
    try:
        exchange_rate = get_exchange_rate(from_currency, to_currency, transaction_date)
        return flt(rate * exchange_rate)
    except Exception as e:
        frappe.log_error(f"Currency conversion error: {str(e)}")
        return rate

@frappe.whitelist()
def get_secondary_price(item_code, secondary_pricelist, primary_pricelist, 
                       uom=None, qty=1, transaction_date=None):
    """
    API method to get secondary price for client script
    """
    # Check if price exists in primary pricelist first
    primary_price = get_item_price_from_pricelist(item_code, primary_pricelist, uom, qty)
    
    if primary_price and flt(primary_price.get("price_list_rate", 0)) > 0:
        return {"rate": 0}  # Primary price exists, don't use secondary
    
    # Get secondary price
    secondary_price = get_item_price_from_pricelist(item_code, secondary_pricelist, uom, qty)
    
    if not secondary_price or flt(secondary_price.get("price_list_rate", 0)) == 0:
        return {"rate": 0}
    
    rate = flt(secondary_price.get("price_list_rate"))
    
    # Handle currency conversion
    primary_currency = frappe.db.get_value("Price List", primary_pricelist, "currency")
    secondary_currency = frappe.db.get_value("Price List", secondary_pricelist, "currency")
    
    if secondary_currency != primary_currency:
        rate = convert_currency_rate(rate, secondary_currency, primary_currency, 
                                   transaction_date or nowdate())
    
    return {
        "rate": rate,
        "original_rate": secondary_price.get("price_list_rate"),
        "currency_converted": secondary_currency != primary_currency,
        "secondary_currency": secondary_currency,
        "primary_currency": primary_currency
    }