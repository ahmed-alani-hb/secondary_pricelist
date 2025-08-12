# Contributing to Secondary Pricelist

Thank you for considering contributing to the Secondary Pricelist ERPNext module! This document provides guidelines and information for contributors.

## 🎯 How to Contribute

### Reporting Bugs

1. **Check existing issues** first to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Provide detailed information:**
   - ERPNext version
   - Python version
   - Browser and version (for client-side issues)
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### Suggesting Features

1. **Check the roadmap** in README.md first
2. **Open a discussion** before creating feature requests
3. **Describe the use case** and business value
4. **Provide mockups or examples** if possible

### Code Contributions

#### Development Setup

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/secondary-pricelist.git
   cd secondary-pricelist
   ```

3. **Set up development environment:**
   ```bash
   # Copy to ERPNext apps directory
   cp -r . /path/to/frappe-bench/apps/secondary_pricelist
   
   # Install in development mode
   cd /path/to/frappe-bench
   bench --site your-site install-app secondary_pricelist
   bench --site your-site migrate
   ```

4. **Enable developer mode** in `site_config.json`:
   ```json
   {
     "developer_mode": 1,
     "debug": true
   }
   ```

#### Development Guidelines

**Python Code:**
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Handle exceptions appropriately
- Use ERPNext's built-in utilities where possible

**JavaScript Code:**
- Use ES6+ features where supported
- Follow consistent indentation (2 spaces)
- Add comments for complex logic
- Use Frappe's JavaScript utilities
- Test across different browsers

**CSS:**
- Use meaningful class names
- Follow BEM methodology where applicable
- Ensure responsive design
- Test across different screen sizes

#### Testing Your Changes

1. **Create test scenarios:**
   - Test basic functionality
   - Test edge cases
   - Test different currencies
   - Test validation logic

2. **Test in different environments:**
   - Fresh ERPNext installation
   - Existing production-like setup
   - Different browsers

3. **Check for regressions:**
   - Ensure existing functionality still works
   - Test standard ERPNext pricing behavior

#### Submitting Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clean, documented code
   - Add appropriate comments
   - Update documentation if needed

3. **Test thoroughly:**
   - Test all affected functionality
   - Ensure no regressions
   - Test in multiple scenarios

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request:**
   - Provide clear description of changes
   - Reference any related issues
   - Include testing instructions
   - Add screenshots if applicable

## 📋 Pull Request Guidelines

### PR Title Format
- `Feature: Add [feature description]`
- `Fix: Resolve [bug description]`
- `Docs: Update [documentation area]`
- `Refactor: Improve [code area]`

### PR Description Template
```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Testing
- [ ] Tested on fresh ERPNext installation
- [ ] Tested with existing data
- [ ] Tested multiple currencies
- [ ] Tested validation scenarios
- [ ] Browser testing completed

## Screenshots
(if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

## 🔍 Code Review Process

1. **Automated checks** must pass
2. **Manual review** by maintainers
3. **Testing** in development environment
4. **Discussion** if changes needed
5. **Merge** when approved

## 🐛 Bug Reports

### Bug Report Template
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- ERPNext version:
- Python version:
- Browser:
- Operating System:

**Screenshots**
(if applicable)

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description**
Clear description of the requested feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this work?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Any other relevant information
```

## 📖 Documentation

### Documentation Guidelines
- Keep documentation up-to-date with code changes
- Use clear, simple language
- Include examples where helpful
- Update relevant sections:
  - README.md for major features
  - INSTALLATION_GUIDE.md for setup changes
  - CHANGELOG.md for all changes

### Documentation Structure
- **README.md** - Main project overview and quick start
- **INSTALLATION_GUIDE.md** - Detailed installation instructions
- **CHANGELOG.md** - Version history and changes
- **CONTRIBUTING.md** - This file
- **Code comments** - Inline documentation

## 🚀 Release Process

1. **Feature freeze** for upcoming version
2. **Testing phase** with beta testers
3. **Documentation update** and review
4. **Version tagging** following semantic versioning
5. **Release notes** preparation
6. **GitHub release** creation

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions
- Respect different viewpoints and experiences

### Communication Channels
- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Pull Requests** - Code contributions and reviews

## 🏆 Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- Release notes
- GitHub contributor graph
- Special mentions for significant contributions

## 📞 Getting Help

If you need help contributing:
1. Check existing documentation
2. Search GitHub issues and discussions
3. Create a new discussion with your question
4. Tag maintainers if urgent

---

Thank you for contributing to make Secondary Pricelist better for the ERPNext community! 🙏