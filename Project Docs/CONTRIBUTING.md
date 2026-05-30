# Contributing to LAI-PrEP Bridge Period Decision Support Tool

Thank you for your interest in contributing to the LAI-PrEP Bridge Period Decision Support Tool! This project aims to improve HIV prevention by optimizing Long-Acting Injectable PrEP initiation.

## 🌟 Ways to Contribute

We welcome contributions from:
- **Clinicians** - Clinical insights, validation, real-world testing
- **Researchers** - Evidence synthesis, outcome data, evaluation
- **Developers** - Code improvements, bug fixes, new features
- **Healthcare Administrators** - Implementation insights, workflow optimization
- **Patients & Advocates** - Lived experience, barrier identification, user experience

---

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button at the top right of this repository.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/lai-prep-bridge-tool.git
cd lai-prep-bridge-tool
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 4. Set Up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests to ensure everything works
python -m pytest tests/
```

---

## 📝 Contribution Types

### 🐛 Bug Reports

**Before submitting:**
- Search existing issues to avoid duplicates
- Test with the latest version
- Gather relevant information

**Include:**
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Python version, OS, and environment details
- Error messages or logs
- Screenshots if applicable

**Template:**
```markdown
**Bug Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- Python version:
- OS:
- Tool version:

**Additional Context:**
Any other relevant information
```

### 💡 Feature Requests

**Before requesting:**
- Check if feature already exists or is planned
- Consider if it aligns with project goals
- Think about implementation approach

**Include:**
- Clear use case and rationale
- How it improves HIV prevention outcomes
- Target user group (clinicians, patients, etc.)
- Alternative approaches considered
- Willingness to help implement

### 🔬 Clinical Validation

We especially welcome contributions from clinicians testing the tool in practice:

**Share:**
- Real-world testing results
- Patient outcome data (de-identified)
- Workflow integration experiences
- Suggested algorithm improvements
- Population-specific insights

**Format:**
```markdown
**Clinical Setting:**
Type of practice, location, patient population

**Implementation Period:**
Start and end dates

**Outcomes:**
- Number of patients assessed
- Bridge period success rates
- Intervention effectiveness
- Barriers encountered

**Recommendations:**
Suggested improvements based on experience
```

### 📚 Documentation

Documentation improvements are always welcome:

- Clarify existing documentation
- Add examples and use cases
- Translate to other languages
- Create video tutorials
- Improve installation instructions
- Add troubleshooting guides

### 💻 Code Contributions

#### Code Style

We follow PEP 8 with these specifics:

```python
# Use type hints
def assess_patient(patient: PatientProfile) -> Assessment:
    ...

# Maximum line length: 88 characters (Black formatter)

# Use descriptive variable names
bridge_success_probability = 0.53  # Good
bsp = 0.53  # Bad

# Add docstrings
def calculate_risk(patient: PatientProfile) -> float:
    """
    Calculate bridge period failure risk.
    
    Args:
        patient: Patient profile with demographics and barriers
        
    Returns:
        Risk score from 0.0 (low risk) to 1.0 (high risk)
        
    Example:
        >>> patient = PatientProfile(age=24, population=Population.MSM)
        >>> risk = calculate_risk(patient)
        >>> print(f"Risk: {risk:.2%}")
    """
    ...
```

#### Code Review Checklist

Before submitting:
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No sensitive data (PHI) in code or commits
- [ ] HIPAA compliance maintained
- [ ] Changes improve clinical utility

#### Testing Requirements

All code contributions must include tests:

```python
# tests/test_patient_assessment.py
import pytest
from lai_prep_decision_tool import PatientProfile, assess_patient, Population

def test_high_risk_patient():
    """Test assessment of high-risk patient"""
    patient = PatientProfile(
        age=18,
        population=Population.ADOLESCENT,
        has_insurance=False,
        barriers=[
            Barrier.TRANSPORTATION,
            Barrier.HOUSING_INSTABILITY,
            Barrier.NO_IDENTIFICATION
        ]
    )
    
    assessment = assess_patient(patient)
    
    assert assessment.success_probability < 0.40
    assert len(assessment.recommended_interventions) >= 3
    assert Intervention.PATIENT_NAVIGATION in assessment.recommended_interventions
```

**Test Coverage:**
- Maintain >80% code coverage
- Test edge cases and error conditions
- Test all populations and barrier combinations
- Test intervention recommendations

---

## 🔄 Development Workflow

### 1. Write Code

Make your changes following our coding standards.

### 2. Write Tests

```bash
# Run tests
python -m pytest tests/

# Check coverage
python -m pytest --cov=lai_prep_decision_tool tests/
```

### 3. Format Code

```bash
# Auto-format with Black
black lai_prep_decision_tool tests

# Check with flake8
flake8 lai_prep_decision_tool tests

# Type check with mypy
mypy lai_prep_decision_tool
```

### 4. Update Documentation

Update relevant documentation files:
- README.md
- TECHNICAL_DOCUMENTATION.md
- Docstrings
- CHANGELOG.md

### 5. Commit Changes

Use clear, descriptive commit messages:

```bash
# Good commit messages
git commit -m "Add RNA testing intervention for adolescent population"
git commit -m "Fix: Correct risk calculation for PWID with insurance"
git commit -m "Docs: Add examples for pharmacy-based implementation"

# Bad commit messages
git commit -m "Update code"
git commit -m "Fix bug"
git commit -m "Changes"
```

**Commit Message Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring
- `style:` - Code formatting
- `chore:` - Maintenance tasks

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Create Pull Request

**Pull Request Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Clinical validation data
- [ ] Code refactoring

## Clinical Impact
How does this change improve HIV prevention outcomes?

## Testing
- [ ] All existing tests pass
- [ ] New tests added
- [ ] Manual testing completed
- [ ] Clinical validation performed (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No PHI included
- [ ] HIPAA compliance maintained
- [ ] Backward compatible (or migration guide provided)

## Related Issues
Closes #(issue number)
```

---

## 🔍 Code Review Process

1. **Automated Checks**
   - All tests must pass
   - Code style checks must pass
   - Coverage must remain >80%

2. **Peer Review**
   - At least one maintainer must approve
   - Clinical contributions reviewed by clinician-maintainers
   - Technical contributions reviewed by developer-maintainers

3. **Merge**
   - Squash and merge for feature branches
   - Clear merge commit messages

---

## 🏥 HIPAA & Privacy Guidelines

**CRITICAL:** This tool handles sensitive health information.

### Required Practices

✅ **DO:**
- Use de-identified data in examples
- Keep patient data processing local
- Follow HIPAA Safe Harbor de-identification
- Document data handling procedures
- Report security vulnerabilities privately

❌ **DON'T:**
- Include PHI in code or comments
- Store patient data in repository
- Use real patient names or identifiers
- Share clinical data without IRB approval
- Post PHI in issues or pull requests

### Security Vulnerability Reporting

**DO NOT** file public issues for security vulnerabilities.

Instead, email: security@nyxdynamics.org

Include:
- Vulnerability description
- Affected versions
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

---

## 📊 Research Data Contributions

We welcome outcome data from real-world implementations:

### Data Submission Format

```python
{
    "implementation": {
        "site_type": "community_health_center",
        "location_region": "northeast",  # Geographic region only
        "start_date": "2025-01",
        "end_date": "2025-06"
    },
    "population": {
        "total_assessed": 150,
        "demographics": {
            "msm": 45,
            "cisgender_women": 60,
            "transgender_women": 25,
            "adolescents": 20
        }
    },
    "outcomes": {
        "baseline_initiation_rate": 0.53,
        "post_intervention_rate": 0.72,
        "interventions_used": [
            "patient_navigation",
            "rna_testing"
        ]
    },
    "barriers_identified": {
        "transportation": 0.40,
        "insurance_delays": 0.25,
        "scheduling": 0.30
    }
}
```

### Data Requirements

- **De-identified:** No PHI
- **IRB Approved:** If research data
- **Structured:** Follow JSON schema
- **Documented:** Include methodology
- **Validated:** Quality checks performed

---

## 🎯 Priority Contributions

We especially need contributions in these areas:

### High Priority
1. **Clinical validation data** from diverse settings
2. **Population-specific insights** (especially PWID, adolescents)
3. **EHR integration modules** (Epic, Cerner, etc.)
4. **Outcome tracking dashboards**
5. **Multi-language support**

### Medium Priority
1. Mobile application development
2. Machine learning enhancements
3. Training video creation
4. Case study documentation
5. Health equity analysis tools

### Community Needs
1. Patient education materials
2. Community organization partnerships
3. Harm reduction program integration
4. Telehealth workflow optimization
5. Payment model guidance

---

## 📞 Getting Help

### Questions?
- **GitHub Discussions:** For general questions
- **Email:** acdemidont@nyxdynamics.org for clinical questions
- **Slack:** [Join our community](link-pending)

### Resources
- [Technical Documentation](TECHNICAL_DOCUMENTATION.md)
- [Implementation Guide](../Clinical%20Implementation%20Guides/NON_TECHNICAL_GUIDE.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

---

## 🙏 Recognition

Contributors are recognized in:
- README.md contributors section
- CHANGELOG.md for specific contributions
- Academic publications (for substantial contributions)
- Project website (coming soon)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🌈 Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code. Please report unacceptable behavior to conduct@nyxdynamics.org.

---

Thank you for helping improve HIV prevention! Every contribution, no matter how small, makes a difference. 🏳️‍🌈❤️

---

*Last updated: October 2025*
