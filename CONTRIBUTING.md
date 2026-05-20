# Contributing to Malnutrition Prediction and Analysis System

Thank you for your interest in contributing to this project! We welcome contributions from the community to help improve global food security analysis.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

### Suggesting Features

We welcome feature suggestions! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach
- Any relevant examples or references

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/AB-1817/Malnutrition-Prediction-and-Analysis-System.git
   cd Malnutrition-Prediction-and-Analysis-System
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines below
   - Add tests for new features
   - Update documentation as needed

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Ensure all tests pass

## 📝 Code Style Guidelines

### Python Code
- Follow **PEP 8** style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Maximum line length: 100 characters

Example:
```python
def predict_risk_level(features: np.ndarray) -> dict:
    """
    Predict malnutrition risk level from input features.
    
    Args:
        features: NumPy array of shape (n_samples, 8) containing nutrition indicators
        
    Returns:
        Dictionary with risk_level, confidence, and probabilities
    """
    # Implementation here
    pass
```

### Jupyter Notebooks
- Clear markdown explanations before code cells
- Remove unnecessary outputs before committing
- Use consistent naming conventions
- Include visualizations where appropriate

### Documentation
- Update README.md for major changes
- Add inline comments for complex logic
- Keep documentation up-to-date with code

## 🧪 Testing

Before submitting a PR:

1. **Run existing tests**
   ```bash
   pytest tests/ -v
   ```

2. **Add tests for new features**
   - Unit tests for functions
   - Integration tests for API endpoints
   - Validation tests for models

3. **Test manually**
   - Run the Streamlit dashboard
   - Test API endpoints
   - Verify notebook execution

## 📦 Dependencies

When adding new dependencies:
- Add to `requirements.txt` with version pinning
- Document why the dependency is needed
- Ensure compatibility with Python 3.9+

## 🔍 Code Review Process

All submissions require review. We use GitHub pull requests for this purpose:

1. Maintainers will review your PR within 3-5 business days
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

## 🎯 Areas for Contribution

We especially welcome contributions in:

- **Model Improvements**: New algorithms, better hyperparameters
- **Data Sources**: Integration with additional nutrition databases
- **Visualizations**: New charts, maps, or interactive elements
- **Documentation**: Tutorials, examples, translations
- **Testing**: Increased test coverage
- **Performance**: Optimization and efficiency improvements
- **Deployment**: CI/CD, cloud deployment guides
- **Accessibility**: UI/UX improvements for diverse users

## 📧 Questions?

If you have questions about contributing:
- Open a GitHub issue with the "question" label
- Email: akashbhuyan1817@gmail.com

## 🙏 Recognition

Contributors will be:
- Listed in the project README
- Credited in release notes
- Acknowledged in documentation

Thank you for helping improve global food security analysis! 🌍
