# ATStereo — Results & Analysis

This directory contains the experimental datasets, analysis scripts, and notebooks for ATStereo.

## Files

- **`results.ipynb`**: Main Jupyter notebook for statistical analysis (summary statistics, Kruskal–Wallis, Dunn's post-hoc tests, novice learning curve fitting, BrainStereo comparison) and generating publication figures (Figures 5–8 at 300 DPI).
- **`LMM.py` & `LMM_output.txt`**: Linear mixed-effects model (random intercept for operator, REML) reporting the primary registration RMSE estimand ($0.38\text{ mm}$, 95% CI: $0.22$–$0.55\text{ mm}$, $df=4$, $\text{ICC}=0.550$) and per-operator metrics for Table 1.
- **`collision_analysis.ipynb`**: Evaluates bilateral trajectory separation distances against the 5.0 mm collision-warning threshold.
- **`ATStereo_Phase1_RMSE_op[1-5].csv`**: Registration RMSE data (156 trials across 5 operators).
- **`ATStereo_WorkflowTime_op[1-5].csv`**: Surgical workflow durations (108 trials across 5 operators).
- **`trajectory_and_safety_errors.xlsx`**: Clinical DBS trajectory deviation ($\delta_{\text{trajectory}}$) across 17 evaluated leads and anatomical safety clearance.
- **`Trajectory_error_retest.xlsx`**: Blinded re-test measurements across all 17 clinical DBS trajectories collected after a washout period for intra-observer repeatability analysis.
- **`Test-retest_trajectory_error.py`**: Intra-observer agreement and repeatability script computing paired differences, Bland–Altman bias, 95% limits of agreement, and two-way intraclass correlation coefficients ($\text{ICC}(2,1)$ and $\text{ICC}(3,1)$).
- **`trajectorySeparation.csv`**: Bilateral entry and target coordinates across 9 clinical cases.

## Usage

### 1. Frame Registration LMM
```bash
python3 LMM.py > LMM_output.txt
```

### 2. Main Analysis & 300 DPI Figures
```bash
python3 -m nbconvert --execute --inplace results.ipynb
```
Generates `Figure_5_RMSE_Distribution.png`, `Figure_6_Learning_Curve.png`, `Figure_7_Boxplots.png`, and `Figure_8_BrainStereo_Comparison.png`.

### 3. Bilateral Collision Analysis
```bash
python3 -m nbconvert --execute --inplace collision_analysis.ipynb
```

### 4. Trajectory Test–Retest Repeatability Analysis
```bash
python3 Test-retest_trajectory_error.py
```
Computes intra-observer repeatability metrics across all 17 clinical DBS leads:
- Mean difference (bias): $-0.0073\text{ mm}$
- 95% Limits of agreement: $[-0.125, +0.110]\text{ mm}$
- Mean absolute difference: $0.0492\text{ mm}$
- Reliability: $\text{ICC}(2,1) = 0.714$, $\text{ICC}(3,1) = 0.705$, Pearson $r = 0.714$

## Environment
Python 3.12 (`numpy`, `pandas`, `scipy`, `statsmodels`, `scikit-posthocs`, `matplotlib`, `openpyxl`, `nbconvert`)