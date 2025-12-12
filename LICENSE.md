MIT License

Copyright (c) 2025 Adrian C. Demidont, Nyx Dynamics LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Attribution

When using this software, please provide attribution as follows:

**Citation (BibTeX):**
```bibtex
@software{demidont2025laiprep,
  author    = {Demidont, Adrian C.},
  title     = {LAI-PrEP Bridge Period Decision Support Tool},
  subtitle  = {Computational Validation at UNAIDS Global Scale},
  version   = {4.1.0},
  year      = 2025,
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.17873201},
  url       = {https://doi.org/10.5281/zenodo.17873201},
  repository = {https://github.com/Nyx-Dynamics/lai-prep-bridge-tool-pub}
}
```

**Citation (Text):**
Demidont, A.C. (2025). LAI-PrEP Bridge Period Decision Support Tool: Computational validation at UNAIDS global target scale (v4.1.0). Zenodo. https://doi.org/10.5281/zenodo.17873201

---

## Software Components

This software includes:

1. **Main algorithm** (`lai_prep_decision_tool_v2_1.py`)
   - Core decision support implementation
   - Population-specific risk stratification
   - Barrier identification and quantification
   - Evidence-based intervention recommendation

2. **Configuration system** (`lai_prep_config.json`)
   - Externalized parameters
   - Evidence tier documentation
   - Population and intervention definitions
   - Barrier impact weights

3. **Testing suite** (multiple test files)
   - Edge case validation (18 scenarios)
   - Unit tests for core functionality
   - Population-specific tests
   - Mechanism diversity scoring tests

4. **Utilities**
   - Configuration validation
   - Test runner
   - Documentation generation scripts

All components are released under the MIT License.

---

## Third-Party Dependencies

The software requires:
- **NumPy** (≥1.21.0): BSD License
  - Available at: https://numpy.org/doc/stable/license.html

No other external dependencies are required.

---

## Version and Release History

- **Current Version:** 4.1.0 (December 12, 2025)
- **Zenodo DOI:** 10.5281/zenodo.17873201
- **GitHub:** https://github.com/Nyx-Dynamics/lai-prep-bridge-tool-pub

---

## Disclaimer

This software is provided "as is" for research and educational purposes. It is intended to support clinical decision-making, not replace clinical judgment. Users should:

1. **Review all documentation** before deployment
2. **Conduct prospective validation** with real patient data
3. **Assess equity implications** for their specific population
4. **Ensure institutional review** and approval
5. **Monitor implementation outcomes** continuously
6. **Update parameters** as new evidence emerges

The author disclaims liability for any clinical decisions made based on this tool or any adverse outcomes resulting from its use.

---

## Contributing

Contributions are welcome under the MIT License. By submitting contributions, you agree to license them under the same MIT License.

See CONTRIBUTING.md for guidelines.

---

## Questions

For questions about licensing or usage, contact:
- Adrian C. Demidont, DO
- Nyx Dynamics LLC
- acdemidont@nyxdynamics.org
