# Secondary Pricelist for ERPNext

A powerful ERPNext v15 module that adds secondary pricelist functionality to Sales Orders with automatic fallback pricing and multi-currency support.

## 🎯 Features

- **🔄 Automatic Fallback Pricing** - When primary pricelist has no price, automatically searches secondary pricelist
- **💱 Multi-Currency Support** - Handles different currencies with automatic conversion using ERPNext exchange rates
- **⚡ Real-time Integration** - Client-side JavaScript for immediate pricing updates
- **✅ Smart Validation** - Prevents configuration errors and validates pricelist selections
- **📝 Audit Trail** - Tracks when secondary pricing is applied with detailed comments
- **🔧 ERPNext v15 Compatible** - Full compatibility with standard ERPNext pricing logic

## 📸 Screenshots

### Sales Order with Secondary Pricing
![Secondary Pricing Fields](https://via.placeholder.com/800x300/007bff/ffffff?text=Secondary+Pricing+Fields)

### Automatic Price Application
![Price Application Alert](https://via.placeholder.com/800x200/28a745/ffffff?text=Price+Applied+from+Secondary+Pricelist)

## 🚀 Quick Start

### Prerequisites
- ERPNext v15
- Frappe Framework
- Python 3.8+

### Installation

1. **Download or clone this repository:**
   ```bash
   cd /path/to/frappe-bench/apps
   git clone https://github.com/YOUR_USERNAME/secondary-pricelist.git
   ```

2. **Install the app:**
   ```bash
   bench --site your-site-name install-app secondary_pricelist
   ```

3. **Run migrations:**
   ```bash
   bench --site your-site-name migrate
   ```

4. **Clear cache and restart:**
   ```bash
   bench --site your-site-name clear-cache
   bench restart
   ```

## 📖 Usage

### Basic Setup

1. **Go to Sales Order**
2. **Enable "Enable Secondary Pricing"** checkbox
3. **Select a "Secondary Price List"** from the dropdown
4. **Add items** - secondary pricing will be applied automatically when needed

### Configuration

1. **Create Price Lists:**
   - Set up your primary selling price list
   - Create a secondary price list (can be different currency)
   - Add item prices to both lists with different coverage

2. **Set Exchange Rates:**
   - If using different currencies, ensure exchange rates are configured
   - Go to Setup > Currency Exchange

### Example Workflow

```
Primary Price List: "Standard Selling" (USD)
- Item A: $100
- Item B: Not priced
- Item C: $50

Secondary Price List: "Wholesale" (EUR)  
- Item A: €80
- Item B: €75
- Item C: €40

Result in Sales Order:
- Item A: $100 (from primary)
- Item B: $82.50 (€75 converted from secondary)
- Item C: $50 (from primary)
```

## 🏗️ Architecture

### File Structure
```
secondary_pricelist/
├── 📁 config/                    # Module configuration
├── 📁 fixtures/                  # Custom field definitions
├── 📁 overrides/                 # Python business logic
├── 📁 public/                    # Client-side assets
│   └── css/                      # Custom styling
└── 📁 templates/                 # Custom templates
```

### Key Components

- **`overrides/sales_order.py`** - Core pricing logic and currency conversion
- **`fixtures/custom_field.json`** - Custom field definitions
- **`hooks.py`** - ERPNext integration hooks

## 🔧 Customization

### Modifying Pricing Logic

Edit `overrides/sales_order.py` to customize:
- Priority rules for price selection
- Currency conversion behavior
- Validation logic
- Audit trail format

### Styling Changes

Edit `public/css/secondary_pricelist.css` to modify:
- Form field appearance
- Alert styling
- Dashboard indicators

## 🧪 Testing

### Test Scenarios

1. **Basic Fallback:**
   - Primary has price → Use primary
   - Primary missing → Use secondary

2. **Currency Conversion:**
   - Different currencies → Automatic conversion
   - Same currency → Direct price application

3. **Validation:**
   - Same pricelist selected → Error prevention
   - Missing secondary → Graceful handling

### Creating Test Data

```python
# Create test price lists
frappe.get_doc({
    "doctype": "Price List",
    "price_list_name": "Test Secondary",
    "currency": "EUR",
    "selling": 1
}).insert()

# Add test item prices
frappe.get_doc({
    "doctype": "Item Price",
    "item_code": "TEST-ITEM",
    "price_list": "Test Secondary",
    "price_list_rate": 100,
    "selling": 1
}).insert()
```

## 🐛 Troubleshooting

### Common Issues

**Custom fields not showing:**
```bash
bench --site your-site migrate
bench --site your-site clear-cache
```

**JavaScript not loading:**
```bash
bench restart
# Check browser console for errors
```

**Secondary pricing not working:**
- Verify both price lists exist
- Check exchange rates are set up
- Ensure items have different pricing coverage

### Debug Mode

Enable debug mode in `site_config.json`:
```json
{
    "developer_mode": 1,
    "debug": true
}
```

## 📊 Performance

- **Minimal overhead** - Only processes when secondary pricing is enabled
- **Efficient queries** - Single database calls for price lookup
- **Client-side caching** - Reduces server requests
- **Async processing** - Non-blocking currency conversion

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone for development
git clone https://github.com/YOUR_USERNAME/secondary-pricelist.git
cd secondary-pricelist

# Install in development mode
bench get-app .
bench --site your-site install-app secondary_pricelist
```

## 📋 Roadmap

- [ ] **v1.1**: Multiple fallback price lists (tertiary, quaternary)
- [ ] **v1.2**: Bulk price update utilities  
- [ ] **v1.3**: Price list priority configuration
- [ ] **v1.4**: Integration with supplier price lists
- [ ] **v1.5**: Advanced reporting and analytics

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](license.txt) file for details.

## 🙏 Acknowledgments

- ERPNext community for the excellent framework
- Frappe team for the development tools
- Contributors who help improve this module

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/secondary-pricelist/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/secondary-pricelist/discussions)
- **Documentation:** [Installation Guide](INSTALLATION_GUIDE.md)

---

**Made with ❤️ for the ERPNext community**