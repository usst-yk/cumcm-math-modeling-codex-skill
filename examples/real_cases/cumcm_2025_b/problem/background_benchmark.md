# Background Benchmark

## Sources

| Source | Use | Status |
| --- | --- | --- |
| CUMCM official 2025 problem page | Confirms official problem release and attachment package | checked |
| B problem PDF mirror | Confirms title, subquestions, and attachment column meanings | checked |

## Transferable Mechanism

The task is a one-dimensional spectral inverse problem. For a single reflected
beam pair, the reflectance oscillation versus wavenumber has a dominant
frequency

```text
f = 2 n d cos(theta_t)
```

where `theta_t = asin(sin(theta) / n)`. Therefore

```text
d = f / (2 n cos(theta_t))
```

when `d` is measured in centimeters and wavenumber is measured in `cm^-1`.

## Failure Risks

- Treating a best-fit thickness as an official standard answer.
- Estimating peaks without validating angle-to-angle consistency.
- Forgetting unit conversion between centimeter and micrometer.
- Using AI-generated figures as spectral evidence.

## Test Use

This case uses synthetic spectra with a known thickness. The benchmark target is
not to reproduce the official hidden data, but to prove that the code can recover
a known physical thickness from B-question-style input.
