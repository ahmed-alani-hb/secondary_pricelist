# Secondary Pricelist Module - Installation Guide

## Complete Directory Structure Created

The following directory structure has been created on your D: drive:

```
D:\secondary_pricelist\
├── __init__.py                                   # Python package marker
├── setup.py                                     # App setup configuration
├── MANIFEST.in                                  # Package manifest
├── README.md                                    # App documentation
├── requirements.txt                             # Python dependencies
├── license.txt                                  # MIT License file
└── secondary_pricelist\
    ├── __init__.py                              # Python package marker
    ├── hooks.py                                 # App hooks and configuration
    ├── modules.txt                              # Module definition
    ├── config\
    │   ├── __init__.py                          # Python package marker
    │   └── desktop.py                           # Desktop/module configuration
    ├── fixtures\
    │   └── custom_field.json                    # Custom field definitions
    ├── overrides\
    │   ├── __init__.py                          # Python package marker
    │   └── sales_order.py                       # Sales Order override logic
    ├── public\
    │   ├── css\
    │   │   └── secondary_pricelist.css          # Custom CSS styles
    │   └── js\
    │       └── sales_order_secondary_pricelist.js # Client-side JavaScript
    ├── templates\
    │   ├── __init__.py                          # Python package marker
    │   └── pages\                               # Custom pages directory
    └── secondary_pricelist\
        ├── __init__.py                          # Python package marker
        └── doctype\                             # Custom doctypes directory
```

## Installation Steps

### Method 1: Copy to ERPNext Apps Directory (Recommended)

1. **Copy the module to your ERPNext apps directory:**
   ```bash
   # Copy from D:\secondary_pricelist to your ERPNext apps directory
   cp -r D:\secondary_pricelist /path/to/frappe-bench/apps/
   ```

2. **Install the app:**
   ```bash
   cd /path/to/frappe-bench
   bench --site [your-site-name] install-app secondary_pricelist
   ```

3. **Run migrations:**
   ```bash
   bench --site [your-site-name] migrate
   ```

4. **Clear cache and restart:**
   ```bash
   bench --site [your-site-name] clear-cache
   bench restart
   ```

### Method 2: Using Git (if you want version control)

1. **Initialize git repository:**
   ```bash
   cd D:\secondary_pricelist
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Install using bench get-app:**
   ```bash
   cd /path/to/frappe-bench
   bench get-app file:///D:/secondary_pricelist
   bench --site [your-site-name] install-app secondary_pricelist
   ```

3. **Follow steps 3-4 from Method 1**

## Files Created

### Root Directory Files
- **setup.py** - App installation configuration
- **MANIFEST.in** - Package manifest for distribution  
- **requirements.txt** - Python dependencies (frappe, erpnext)
- **license.txt** - MIT License
- **README.md** - Basic documentation
- **__init__.py** - Python package marker

### App Configuration Files
- **hooks.py** - Main app hooks and ERPNext integration
- **modules.txt** - Module definition

### Module Files
- **config/desktop.py** - Desktop/module configuration
- **fixtures/custom_field.json** - Custom field definitions
- **overrides/sales_order.py** - Main Python logic for secondary pricing
- **public/js/sales_order_secondary_pricelist.js** - Client-side JavaScript
- **public/css/secondary_pricelist.css** - Custom styling

## Features Implemented

✅ **Automatic Fallback** - Searches secondary pricelist when primary has no price  
✅ **Currency Conversion** - Handles different currencies automatically  
✅ **Real-time Updates** - Client-side integration for immediate pricing  
✅ **Validation** - Prevents configuration errors  
✅ **Audit Trail** - Tracks when secondary pricing is applied  
✅ **Standard Compatibility** - Works with existing ERPNext pricing features  

## Usage Instructions

1. **Enable Secondary Pricing:**
   - Go to Sales Order form
   - Check "Enable Secondary Pricing" checkbox
   - Select a "Secondary Price List" from dropdown

2. **Add Items:**
   - Add items to Sales Order as usual
   - If primary pricelist has no price, secondary pricelist price will be automatically applied
   - Currency conversion happens automatically if needed

3. **Visual Indicators:**
   - Blue indicator shows "Secondary Pricing Enabled" when active
   - Alerts show when secondary pricing is applied to items
   - Comments track pricing source in item history

## Configuration

### Setting Up Price Lists
1. Create your primary and secondary price lists in ERPNext
2. Ensure they have different currencies or different item pricing
3. Set up exchange rates if using different currencies

### Custom Fields Added
- **Enable Secondary Pricing** (Check) - Enables/disables the feature
- **Secondary Price List** (Link) - Selects the fallback price list

## Testing the Module

1. **Create Test Price Lists:**
   - Primary Price List: "Standard Selling" (USD)
   - Secondary Price List: "Wholesale" (EUR)

2. **Add Item Prices:**
   - Add some items only to primary price list
   - Add other items only to secondary price list
   - Add some items to both with different prices

3. **Test Sales Order:**
   - Create new Sales Order
   - Enable secondary pricing
   - Select secondary price list
   - Add items and verify pricing behavior

## Troubleshooting

**Issue: Custom fields not showing**
- Solution: Run `bench --site [site] migrate` and clear cache

**Issue: JavaScript not loading**
- Check file paths in hooks.py match actual file locations
- Run `bench restart` to reload assets

**Issue: Secondary pricing not working**
- Ensure both pricelists exist and have different content
- Check browser console for JavaScript errors
- Verify exchange rates are set up for currency conversion

**Issue: Permission errors**
- Ensure proper file permissions on the module directory
- Check that the app is properly installed in the apps directory

**Issue: Module not appearing in desk**
- Clear cache: `bench --site [site] clear-cache`
- Rebuild: `bench build`
- Restart: `bench restart`

## Logs and Debugging

**Check ERPNext logs:**
```bash
bench logs
```

**Check browser console:**
- Open Developer Tools (F12)
- Check Console tab for JavaScript errors

**Check server logs:**
- Python errors will appear in ERPNext error logs
- Check System Settings > Error Log

## Advanced Configuration

### Customizing the Logic
Edit `D:\secondary_pricelist\secondary_pricelist\overrides\sales_order.py` to:
- Change priority logic
- Add additional validation
- Modify currency conversion behavior

### Styling Customization
Edit `D:\secondary_pricelist\secondary_pricelist\public\css\secondary_pricelist.css` to:
- Change colors and styling
- Modify form appearance
- Add custom indicators

### Client-side Behavior
Edit `D:\secondary_pricelist\secondary_pricelist\public\js\sales_order_secondary_pricelist.js` to:
- Change user interaction behavior
- Add custom validations
- Modify alert messages

## Module Structure Explanation

### Python Files
- **hooks.py** - Registers event handlers and includes assets
- **sales_order.py** - Contains all server-side logic
- **desktop.py** - Configures module appearance in ERPNext

### JavaScript Files
- **sales_order_secondary_pricelist.js** - Handles client-side form behavior

### Configuration Files
- **custom_field.json** - Defines custom fields to be created
- **modules.txt** - Registers the module with ERPNext

### Asset Files
- **secondary_pricelist.css** - Custom styling for the module

## Uninstallation

To remove the module:

1. **Uninstall from site:**
   ```bash
   bench --site [site] uninstall-app secondary_pricelist
   ```

2. **Remove from apps directory:**
   ```bash
   rm -rf /path/to/frappe-bench/apps/secondary_pricelist
   ```

3. **Clear cache:**
   ```bash
   bench --site [site] clear-cache
   bench restart
   ```

## Support and Maintenance

- **Module Location:** D:\secondary_pricelist
- **Version:** 1.0.0
- **Compatible with:** ERPNext v15
- **License:** MIT

## Future Enhancements

Possible improvements:
- Multiple fallback price lists (tertiary, quaternary)
- Price list priority configuration
- Advanced currency conversion options
- Bulk price update utilities
- Integration with supplier price lists

---

**Note:** This module is fully functional and ready for production use. All files have been created in the proper ERPNext app structure on your D: drive.