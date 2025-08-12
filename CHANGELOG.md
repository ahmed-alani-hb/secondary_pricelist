# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-08-12

### Added
- Initial release of Secondary Pricelist module
- Automatic fallback pricing functionality
- Multi-currency support with automatic conversion
- Real-time client-side integration
- Custom fields for Sales Order:
  - Enable Secondary Pricing (checkbox)
  - Secondary Price List (link field)
- Server-side validation and error handling
- Audit trail with comments tracking
- CSS styling for enhanced user experience
- Comprehensive documentation and installation guide

### Features
- ✅ Automatic price lookup from secondary pricelist when primary has no price
- ✅ Currency conversion using ERPNext exchange rates
- ✅ Client-side form validation and real-time updates
- ✅ Dashboard indicators for secondary pricing status
- ✅ Comment tracking for pricing source audit trail
- ✅ Full compatibility with ERPNext v15 standard pricing logic

### Technical Implementation
- Python override hooks for Sales Order document events
- JavaScript client script for form interaction
- JSON fixtures for custom field creation
- CSS styling for visual enhancements
- Proper ERPNext app structure with all required files

### Documentation
- Complete installation guide
- Usage instructions with examples
- Troubleshooting section
- Architecture documentation
- Contributing guidelines

## [Unreleased]

### Planned Features
- Multiple fallback price lists (tertiary, quaternary)
- Price list priority configuration
- Bulk price update utilities
- Advanced currency conversion options
- Integration with supplier price lists
- Enhanced reporting and analytics

---

## Version History

- **v1.0.0** - Initial release with core functionality
- **Future versions** - See roadmap in README.md