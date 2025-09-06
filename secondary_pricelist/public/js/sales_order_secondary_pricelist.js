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
            // Use setTimeout to ensure primary pricing logic completes first
            setTimeout(() => {
                check_and_apply_secondary_pricing(frm, cdt, cdn);
            }, 500); // 500ms delay to allow primary pricing to complete
        }
    }
    
    // Also trigger on price_list_rate change in case primary pricing sets it to 0
    //price_list_rate: function(frm, cdt, cdn) {
    //    let item = locals[cdt][cdn];
        
        // Only trigger if secondary pricing is enabled and price_list_rate is 0 or empty
    //    if (frm.doc.custom_enable_secondary_pricing && 
    //        frm.doc.custom_secondary_pricelist && 
    //        item.item_code &&
    //        (!item.price_list_rate || item.price_list_rate === 0)) {
    //        
    //        setTimeout(() => {
    //            check_and_apply_secondary_pricing(frm, cdt, cdn);
    //        }, 500); // Shorter delay since we're already in the pricing flow
    //    }
    //}
});

function refresh_secondary_pricing(frm) {
    // Refresh pricing for all items when secondary pricelist or currency changes
    frm.doc.items.forEach(item => {
        if (!item.price_list_rate || item.price_list_rate === 0) {
            check_and_apply_secondary_pricing(frm, item.doctype, item.name);
        }
    });
}

function check_and_apply_secondary_pricing(frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    
    if (!item.item_code || !frm.doc.custom_secondary_pricelist) {
        return;
    }
    
    // Only apply if no price_list_rate found in primary pricelist
    if (!item.price_list_rate || item.price_list_rate === 0) {
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
                company: frm.doc.company
            },
            callback: function(r) {
                if (r.message && r.message.price_list_rate && r.message.price_list_rate > 0) {
                    // Set price_list_rate (Sales Order currency)
                    frappe.model.set_value(cdt, cdn, 'price_list_rate', r.message.price_list_rate);

                    // Set base_price_list_rate (Company currency) if provided
                    if (r.message.base_price_list_rate) {
                        frappe.model.set_value(cdt, cdn, 'base_price_list_rate', r.message.base_price_list_rate);
                    }
                    
                    // Force refresh the item row to trigger ERPNext's calculations
                    frm.refresh_field('items');
                    
                    // Show success message
                    frappe.show_alert({
                        message: __('Price applied from secondary pricelist: {0}', [frm.doc.custom_secondary_pricelist]),
                        indicator: 'blue'
                    }, 5);
                }
            },
            error: function(r) {
                console.error('Secondary pricing error:', r);
            }
        });
    }
}
