frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // Add indicator if secondary pricing is enabled
        if (frm.doc.custom_enable_secondary_pricing && frm.doc.custom_secondary_pricelist) {
            frm.dashboard.add_indicator(__('Secondary Pricing Enabled'), 'blue');
        }
    },
    
    custom_enable_secondary_pricing: function(frm) {
        if (!frm.doc.custom_enable_secondary_pricing) {
            frm.set_value('custom_secondary_pricelist', '');
        }
    },
    
    custom_secondary_pricelist: function(frm) {
        if (frm.doc.custom_secondary_pricelist && 
            frm.doc.custom_secondary_pricelist === frm.doc.selling_price_list) {
            frappe.msgprint(__('Secondary Price List cannot be the same as Primary Price List'));
            frm.set_value('custom_secondary_pricelist', '');
            return;
        }
        
        // Refresh pricing for all items
        if (frm.doc.custom_secondary_pricelist && frm.doc.items) {
            refresh_secondary_pricing(frm);
        }
    },
    
    selling_price_list: function(frm) {
        if (frm.doc.custom_secondary_pricelist && 
            frm.doc.custom_secondary_pricelist === frm.doc.selling_price_list) {
            frappe.msgprint(__('Secondary Price List cannot be the same as Primary Price List'));
            frm.set_value('custom_secondary_pricelist', '');
        }
    },
    
    currency: function(frm) {
        // Refresh secondary pricing when currency changes
        if (frm.doc.custom_enable_secondary_pricing && frm.doc.custom_secondary_pricelist && frm.doc.items) {
            refresh_secondary_pricing(frm);
        }
    },
    
    conversion_rate: function(frm) {
        // Refresh secondary pricing when conversion rate changes
        if (frm.doc.custom_enable_secondary_pricing && frm.doc.custom_secondary_pricelist && frm.doc.items) {
            refresh_secondary_pricing(frm);
        }
    }
});

frappe.ui.form.on('Sales Order Item', {
    item_code: function(frm, cdt, cdn) {
        // Trigger secondary pricing check after item selection
        if (frm.doc.custom_enable_secondary_pricing && frm.doc.custom_secondary_pricelist) {
            // Ensure primary pricing logic finishes first
            frappe.after_ajax(() => {
                check_and_apply_secondary_pricing(frm, cdt, cdn);
            });
        }
    }
});

function refresh_secondary_pricing(frm) {
    // Refresh pricing for all items when secondary pricelist or currency changes
    frm.doc.items.forEach(item => {
        if (!item.rate || item.rate === 0) {
            check_and_apply_secondary_pricing(frm, item.doctype, item.name);
        }
    });
}

function check_and_apply_secondary_pricing(frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    
    if (!item.item_code || !frm.doc.custom_secondary_pricelist) {
        return;
    }
    
    // Only apply if no rate found in primary pricelist
    if (!item.rate || item.rate === 0) {
        frappe.call({
            method: 'secondary_pricelist.overrides.sales_order.get_secondary_price',
            args: {
                item_code: item.item_code,
                secondary_pricelist: frm.doc.custom_secondary_pricelist,
                primary_pricelist: frm.doc.selling_price_list,
                uom: item.uom,
                qty: item.qty,
                transaction_date: frm.doc.transaction_date,
                sales_order_currency: frm.doc.currency,
                conversion_rate: frm.doc.conversion_rate,
                company: frm.doc.company  // Pass company for base currency
            },
            callback: function(r) {
                if (r.message && r.message.price_list_rate) {
                    // Set price_list_rate (Sales Order currency)
                    frappe.model.set_value(cdt, cdn, 'price_list_rate', r.message.price_list_rate);

                    // Set base_price_list_rate (Company currency) if provided
                    if (r.message.base_price_list_rate) {
                        frappe.model.set_value(cdt, cdn, 'base_price_list_rate', r.message.base_price_list_rate);
                    }

                    // Trigger ERPNext's rate calculations and refresh item row
                    frm.script_manager.trigger('price_list_rate', cdt, cdn);
                    frm.refresh_field('items');

                    frappe.show_alert({
                        message: __('Price applied from secondary pricelist: {0}', [frm.doc.custom_secondary_pricelist]),
                        indicator: 'blue'
                    }, 6);
                }
            }
        });
    }
}