# Security Policy

## Overview

The LAI-PrEP Bridge Period Decision Support Tool handles sensitive healthcare information related to HIV prevention. We take security and patient privacy extremely seriously.

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Principles

### 1. **No PHI Storage**
This tool does NOT store Protected Health Information (PHI). All processing happens locally on the user's system.

### 2. **Local Processing**
Patient assessments are performed entirely on the local machine. No data is transmitted to external servers.

### 3. **Open Source**
All code is open source and auditable for security review.

### 4. **HIPAA-Compliant by Design**
Tool architecture prevents accidental PHI exposure or storage.

## Reporting a Vulnerability

### **DO NOT** Report Security Vulnerabilities Publicly

Security vulnerabilities should **NEVER** be reported through public GitHub issues, discussions, or pull requests.

### How to Report

**Email:** security@nyxdynamics.org

**PGP Key:** [Available on request]

### What to Include

Please provide:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** assessment
4. **Affected versions**
5. **Suggested fix** (if available)
6. **Your contact information** for follow-up

### Example Report

```
Subject: [SECURITY] Potential PHI Exposure in Patient Export

Description:
The patient export function may inadvertently include 
identifiable information in the JSON output under certain 
conditions.

Steps to Reproduce:
1. Create patient profile with specific demographics
2. Export using export_patient() function
3. Check JSON output for identifiable fields

Impact:
Potential HIPAA violation through accidental PHI exposure

Affected Versions:
1.0.0, 1.0.1

Suggested Fix:
Add PHI scrubbing to export function before serialization

Contact: researcher@example.edu
```

## Response Timeline

We take security seriously and will respond promptly:

- **Initial Response:** Within 48 hours
- **Assessment:** Within 7 days
- **Fix Development:** Based on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: Next release cycle
- **Public Disclosure:** After fix is released

## Severity Classification

### Critical
- PHI exposure or leakage
- Remote code execution
- Authentication bypass
- Data corruption affecting patient safety

**Response:** Immediate patch release

### High
- Unauthorized data access
- Security feature bypass
- Significant privacy compromise

**Response:** Urgent patch within 7 days

### Medium
- Limited information disclosure
- Minor security feature weaknesses
- Denial of service vulnerabilities

**Response:** Patch within 14 days

### Low
- Theoretical vulnerabilities
- Minor security improvements
- Best practice violations

**Response:** Include in next scheduled release

## Security Best Practices for Users

### For Healthcare Providers

1. **Environment Security**
   - Use tool only on secure, HIPAA-compliant systems
   - Ensure workstation encryption is enabled
   - Keep system and antivirus software updated
   - Lock workstation when leaving

2. **Access Control**
   - Limit tool access to authorized personnel only
   - Use strong authentication for system access
   - Follow organizational access policies
   - Log and monitor tool usage

3. **Data Handling**
   - Never include PHI in bug reports or issues
   - De-identify any data used for testing
   - Follow organizational data retention policies
   - Securely dispose of any printed materials

4. **Network Security**
   - Use tool on secure, private networks only
   - Avoid public Wi-Fi for patient assessments
   - Use VPN if remote access is required
   - Follow organizational network policies

### For Developers

1. **Code Security**
   - Review all code for potential PHI leakage
   - Never hardcode sensitive information
   - Use parameterized queries (if database added)
   - Validate all inputs
   - Sanitize all outputs

2. **Testing**
   - Use only synthetic/de-identified test data
   - Never use real patient information for testing
   - Include security tests in test suite
   - Test all user input validation

3. **Dependencies**
   - Keep dependencies updated
   - Review security advisories for dependencies
   - Use `pip-audit` or similar tools
   - Pin dependency versions

4. **PHI Protection**
   - Never commit PHI to repository
   - Review all commits before pushing
   - Use `.gitignore` for sensitive directories
   - Enable pre-commit hooks

## HIPAA Compliance

### Privacy Requirements

This tool is designed to support HIPAA-compliant workflows:

**Minimum Necessary:** Tool only requests essential data
**Local Processing:** No PHI transmitted externally
**No Storage:** No PHI persisted to disk
**Audit Trail:** Organizations can log usage per their policies
**Access Controls:** Deployable with organizational controls

### User Responsibilities

Users are responsible for:

- Deploying tool in HIPAA-compliant environment
- Implementing appropriate access controls
- Maintaining audit logs per organizational policy
- Training staff on secure usage
- Ensuring proper device security
- Following data breach notification procedures

### What This Tool Does NOT Do

Does NOT store patient data
Does NOT transmit data to external servers
Does NOT create a covered entity relationship
Does NOT require a Business Associate Agreement
Does NOT include audit logging (user's responsibility)

## Known Limitations

### Current Version (1.1.0)

1. **No Built-in Encryption**
   - User responsible for device encryption
   - No file-level encryption of tool outputs

2. **No Audit Logging**
   - Organizations must implement their own logging
   - Tool does not track who used it or when

3. **No Access Controls**
   - Tool itself has no authentication
   - Relies on system-level access controls

4. **No Data Loss Prevention**
   - Users can export data (by design for flexibility)
   - No automatic PHI detection or blocking

These are intentional design choices to keep the tool lightweight and locally-deployable. Organizations should layer their own security controls as needed.

## Security Checklist for Implementation

Before deploying in your organization:

### Technical
- [ ] Tool installed on HIPAA-compliant workstations
- [ ] Workstation encryption enabled
- [ ] Antivirus/security software active and updated
- [ ] System access controls configured
- [ ] Network security policies enforced
- [ ] Regular security patches applied

### Administrative
- [ ] Security policy review completed
- [ ] Risk assessment conducted
- [ ] Staff training provided
- [ ] Usage logs implemented (if required)
- [ ] Data handling procedures documented
- [ ] Incident response plan includes tool
- [ ] Privacy officer consulted

### Physical
- [ ] Workstations in secure locations
- [ ] Screen privacy filters (if in public areas)
- [ ] Workstation lock policy enforced
- [ ] Printed materials security addressed

## Incident Response

If you suspect a security incident involving this tool:

### Immediate Actions

1. **Stop using the tool** immediately
2. **Document** what happened
3. **Notify** your security/privacy officer
4. **Preserve** evidence (logs, screenshots)
5. **Report** to info@nyxdynamics.org

### Do Not

- Do NOT delete anything
- Do NOT try to "fix" it yourself
- Do NOT discuss publicly
- Do NOT continue using until cleared

### Follow Your Organization's

- Incident response procedures
- Breach notification requirements
- Documentation requirements
- Chain of command

## Updates and Patches

### Security Updates

Security patches are released as soon as safely possible:

- **Critical:** Emergency release (hours to days)
- **High:** Urgent release (days)
- **Medium/Low:** Regular release cycle

### Notification

Security updates are announced via:

1. GitHub Security Advisories
2. Release notes (for non-sensitive issues)
3. Email to registered implementations
4. Project website

### Applying Updates

```bash
# Check current version
python lai_prep_decision_tool.py --version

# Update to latest version
git pull origin main
pip install -r requirements.txt --upgrade

# Verify update
python lai_prep_decision_tool.py --version
```

## Security Audit

This project welcomes security audits:

- Independent security reviews encouraged
- Academic research collaborations welcome
- Responsible disclosure appreciated
- Will acknowledge security researchers (with permission)

## Compliance Certifications

This tool is not certified but is designed to support:

- HIPAA compliance (when properly deployed)
- GDPR principles (data minimization, local processing)
- HITRUST framework compatibility
- SOC 2 control objectives

Organizations are responsible for their own compliance validation.

## Contact

**Security Issues:** security@nyxdynamics.org  
**Privacy Questions:** privacy@nyxdynamics.org  
**General Contact:** acdemidont@nyxdynamics.org

## Acknowledgments

We thank the security research community for helping keep this tool secure. Responsible disclosure researchers will be acknowledged in release notes (with permission) and in our security hall of fame (coming soon).

---

## Additional Resources

- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [HHS Breach Notification](https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html)

---



*Last updated: November 29, 2025*
