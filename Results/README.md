# ATStereo registration RMSE analysis

`LMM.py` reproduces the analysis of frame-registration RMSE (156 trials, 5 operators)
reported in Results Section 3.1 and Table 1.

## What it does
- Reads one CSV per operator (column `RMSE`, in mm).
- Fits a linear mixed-effects model with a random intercept for operator (REML):
  RMSE_ij = beta_0 + u_j + e_ij.
- Reports the model-based mean with a t-based 95% CI (df = number of operators - 1),
  the between-operator and residual variances, and the ICC.
- Prints per-operator descriptive statistics (compare with Table 1), the pooled
  trial-level mean, and the mean of operator means with its CI.

## Run
Place the five CSVs (`ATStereo_Phase1_RMSE_op1.csv` ... `op5.csv`) in the same
folder as the script, then:

```
python3 LMM.py > LMM_output.txt
```

Operators are identified only as Op1-Op5.

## Environment
Python 3.12.0, scipy 1.16.2, statsmodels 0.14.6, scikit-posthocs 0.16.1

## Notes
- With five operators the CI uses 4 degrees of freedom, an approximation to
  Satterthwaite/Kenward-Roger for unbalanced data.
- Operators are confounded with experience level, so between-operator variance
  is not purely random.