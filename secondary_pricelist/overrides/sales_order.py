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
    
    # Get all relevant currencies
    secondary_currency = frappe.db.get_value("Price List", secondary_pricelist, "currency")
    company = sales_order.get("company")
    company_currency = frappe.db.get_value("Company", company, "default_currency")
    
    for item in sales_order.items:
        if should_apply_secondary_pricing(item, primary_pricelist):
            apply_secondary_pricing_to_item(item, sales_order, secondary_pricelist, 
                                          secondary_currency, company_currency)

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
                                  secondary_currency=None, company_currency=None):
    """
    Apply secondary pricing to item following ERPNext's standard currency flow:
    Secondary Pricelist Currency → Company Base Currency → Sales Order Currency
    
    CORRECT FORMULA:
    - Secondary to Company: secondary_rate × exchange_rate
    - Company to Sales Order: company_rate × conversion_rate (NOT divide!)
    """
    if not secondary_pricelist:
        secondary_pricelist = sales_order.get("custom_secondary_pricelist")
    
    if not secondary_pricelist:
        return
    
    # Get currencies if not provided
    if not secondary_currency:
        secondary_currency = frappe.db.get_value("Price List", secondary_pricelist, "currency")
    if not company_currency:
        company = sales_order.get("company")
        company_currency = frappe.db.get_value("Company", company, "default_currency")
    
    # Get price from secondary pricelist
    secondary_price = get_item_price_from_pricelist(item.item_code, secondary_pricelist,
                                                  item.uom, item.qty)
    
    if secondary_price and flt(secondary_price.get("price_list_rate", 0)) > 0:
        original_rate = flt(secondary_price.get("price_list_rate"))
        
        # Step 1: Convert from secondary pricelist currency to company base currency
        # EUR 40.85 → USD 47 (40.85 × 1.16)
        base_rate = convert_to_company_currency(
            rate=original_rate,
            from_currency=secondary_currency,
            to_currency=company_currency,
            transaction_date=sales_order.transaction_date
        )
        
        # Step 2: Convert from company base currency to sales order currency
        # USD 47 → IQD 65,799
        # ERPNext conversion_rate = rate to convert FROM sales order currency TO company currency
        # So: sales_order_rate = base_rate ÷ conversion_rate
        conversion_rate = flt(sales_order.conversion_rate) or 1.0
        if conversion_rate > 0:
            # conversion_rate = 0.000714286 means 1 IQD = 0.000714286 USD
            # So: IQD_amount = USD_amount ÷ conversion_rate
            sales_order_rate = flt(base_rate / conversion_rate)
        else:
            sales_order_rate = base_rate
        
        # Apply only price list rates; ERPNext will derive discounted rates
        # price_list_rate should be in Sales Order currency (e.g. IQD)
        # base_price_list_rate should be in Company currency (e.g. USD)
        item.price_list_rate = sales_order_rate  # IQD 65,799
        item.base_price_list_rate = base_rate  # USD 47
        
        # Add detailed comment to track secondary pricing with currency conversion info
        conversion_info = f" (Conversion: {original_rate} {secondary_currency} → {base_rate} {company_currency} → {sales_order_rate} {sales_order.currency})"
        
        item.add_comment("Info", 
            f"Price applied from secondary pricelist: {secondary_pricelist}"
            f"{conversion_info}")
        
        # Log the conversion for debugging
        frappe.logger().info(
            f"Secondary pricing applied: {original_rate} {secondary_currency} → "
            f"{base_rate} {company_currency} → {sales_order_rate} {sales_order.currency} "
            f"(conversion_rate: {conversion_rate})"
        )

def convert_to_company_currency(rate, from_currency, to_currency, transaction_date):
    """
    Convert rate from any currency to company base currency
    """
    if from_currency == to_currency:
        return rate
    
    try:
        # Use ERPNext's built-in exchange rate system to convert to company currency
        exchange_rate = get_exchange_rate(from_currency, to_currency, transaction_date or nowdate())
        converted_rate = flt(rate * exchange_rate)
        
        frappe.logger().info(
            f"Exchange rate conversion: {rate} {from_currency} → {converted_rate} {to_currency} "
            f"(Exchange rate: {exchange_rate})"
        )
        
        return converted_rate
    except Exception as e:
        frappe.log_error(f"Currency conversion error from {from_currency} to {to_currency}: {str(e)}")
        frappe.msgprint(
            _("Could not convert from {0} to {1}. Please check exchange rate setup.").format(
                from_currency, to_currency
            ),
            alert=True
        )
        return rate

def get_item_price_from_pricelist(item_code, price_list, uom=None, qty=1):
    """
    Get item price from specific pricelist - ERPNext v15 compatible
    Based on actual field analysis: price_list_rate, uom, valid_from, valid_upto exist
    min_qty and minimum_qty do NOT exist in this v15 installation
    """
    try:
        # Only use fields that actually exist in ERPNext v15
        fields = [
            "price_list_rate",
            "uom", 
            "valid_from",
            "valid_upto"
        ]
        
        # Query Item Price with only existing fields
        price_data = frappe.get_all("Item Price",
            filters={
                "item_code": item_code,
                "price_list": price_list,
                "selling": 1
            },
            fields=fields,
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
    try:
        from frappe.utils import getdate
        
        today = getdate()
        valid_from = price_data.get("valid_from")
        valid_upto = price_data.get("valid_upto")
        
        if valid_from and getdate(valid_from) > today:
            return False
        
        if valid_upto and getdate(valid_upto) < today:
            return False
        
        return True
    except:
        # If date validation fails, assume price is valid
        return True

@frappe.whitelist()
def get_secondary_price(item_code, secondary_pricelist, primary_pricelist, 
                       uom=None, qty=1, transaction_date=None, sales_order_currency=None, 
                       conversion_rate=None, company=None):
    """
    API method to get secondary price for client script following ERPNext's currency flow
    """
    # Check if price exists in primary pricelist first
    primary_price = get_item_price_from_pricelist(item_code, primary_pricelist, uom, qty)
    
    if primary_price and flt(primary_price.get("price_list_rate", 0)) > 0:
        return {"price_list_rate": 0, "base_price_list_rate": 0}  # Primary price exists, don't use secondary
    
    # Get secondary price
    secondary_price = get_item_price_from_pricelist(item_code, secondary_pricelist, uom, qty)
    
    if not secondary_price or flt(secondary_price.get("price_list_rate", 0)) == 0:
        return {"price_list_rate": 0, "base_price_list_rate": 0}
    
    original_rate = flt(secondary_price.get("price_list_rate"))
    
    # Get currencies
    secondary_currency = frappe.db.get_value("Price List", secondary_pricelist, "currency")
    
    # Get company currency
    if not company:
        company = frappe.defaults.get_global_default("company")
    company_currency = frappe.db.get_value("Company", company, "default_currency")
    
    # Step 1: Convert to company base currency
    # EUR 40.85 → USD 47
    base_rate = convert_to_company_currency(
        rate=original_rate,
        from_currency=secondary_currency,
        to_currency=company_currency,
        transaction_date=transaction_date or nowdate()
    )
    
    # Step 2: Convert to sales order currency using conversion_rate
    # USD 47 → IQD 65,799 (47 ÷ 0.000714286)
    # conversion_rate = 0.000714286 means 1 IQD = 0.000714286 USD
    conversion_rate = flt(conversion_rate) or 1.0
    if conversion_rate > 0:
        price_list_rate = flt(base_rate / conversion_rate)
    else:
        price_list_rate = base_rate

    # Return only price list rates; ERPNext will calculate discounted rates
    return {
        "price_list_rate": price_list_rate,  # In Sales Order currency (e.g. IQD)
        "base_price_list_rate": base_rate    # In Company base currency (e.g. USD)
    }
