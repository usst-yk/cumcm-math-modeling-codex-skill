# Method comparison

This note records why the least-squares main-frequency estimate is selected as the final thickness estimate.

| Method | Main advantage | Main limitation | Role |
|---|---|---|---|
| Peak spacing | Transparent and easy to check from adjacent extrema. | Sensitive to local peak picking and smoothing thresholds. | Order-of-magnitude reference. |
| FFT | Quickly locates the dominant spectral band. | Limited by frequency resolution and windowing leakage. | Frequency-range check. |
| Least-squares main-frequency fit | Uses the whole curve and suppresses single-peak perturbations. | Requires a sensible search interval. | Final estimate. |

The selected method gives a mean thickness of 8.000016 um, with maximum absolute error 0.000082 um.
