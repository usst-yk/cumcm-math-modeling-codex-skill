# Validation Report

This benchmark uses synthetic spectra with a known thickness of `8.000000 um`.

| Item | Evidence | Result | Status |
| --- | --- | --- | --- |
| sic_10deg thickness error | tables/tab_q2_thickness.csv | 0.000050 um <= 0.050000 um | pass |
| sic_15deg thickness error | tables/tab_q2_thickness.csv | 0.000082 um <= 0.050000 um | pass |
| two-angle consistency | tables/tab_q2_reliability.csv | difference=0.000131 um | pass |

Limitations:

- This case checks execution accuracy on a known synthetic spectrum.
- It does not claim to reproduce the official 2025 B hidden attachments.
- The refractive index is fixed to keep the regression test deterministic.
