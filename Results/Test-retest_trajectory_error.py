import numpy as np
import pandas as pd

# 1. Load data
df_test = pd.read_excel("trajectory_and_safety_errors.xlsx", sheet_name="Trajectory")
df_retest = pd.read_excel("Trajectory_error_retest.xlsx")

# 2. Extract the 10 subjects and skip missing values
original = {}
retest = {}

for i in range(10):
    sub = int(df_test['Subject'][i])
    # Left lead
    if pd.notna(df_test['left'][i]) and pd.notna(df_retest['Left'][i]):
        original[(sub, 'L')] = df_test['left'][i]
        retest[(sub, 'L')] = df_retest['Left'][i]
    # Right lead
    if pd.notna(df_test['right'][i]) and pd.notna(df_retest['Right'][i]):
        original[(sub, 'R')] = df_test['right'][i]
        retest[(sub, 'R')] = df_retest['Right'][i]

keys = sorted(original.keys())
m1 = np.array([original[k] for k in keys])
m2 = np.array([retest[k] for k in keys])
n = len(m1)

# 3. Print paired table
print(f"Number of paired measurements: {n}\n")
print(f"{'Lead':<10} {'Original':>10} {'Retest':>10} {'Diff':>10} {'AbsDiff':>10}")
print("-" * 52)
for k, v1, v2 in zip(keys, m1, m2):
    diff = v2 - v1
    lead_name = f"Sub {k[0]}{k[1]}"
    print(f"{lead_name:<10} {v1:>10.4f} {v2:>10.4f} {diff:>10.4f} {abs(diff):>10.4f}")

# 4. Bland-Altman
diffs = m2 - m1
mean_diff = np.mean(diffs)
sd_diff = np.std(diffs, ddof=1)
abs_diffs = np.abs(diffs)

print("\n--- Bland-Altman ---")
print(f"Mean difference (bias):   {mean_diff:.4f} mm")
print(f"SD of differences:       {sd_diff:.4f} mm")
print(f"95% Limits of agreement: [{mean_diff - 1.96*sd_diff:.4f}, {mean_diff + 1.96*sd_diff:.4f}] mm")
print(f"Mean absolute difference: {np.mean(abs_diffs):.4f} mm")
print(f"Max absolute difference:  {np.max(abs_diffs):.4f} mm")

# 5. ICC (Two-way ANOVA)
grand_mean = np.mean([m1, m2])
sub_means = (m1 + m2) / 2
BMS = 2 * np.sum((sub_means - grand_mean)**2) / (n - 1)
WMS = np.sum((m1 - sub_means)**2 + (m2 - sub_means)**2) / n
rater_means = [np.mean(m1), np.mean(m2)]
JMS = n * np.sum((rater_means - grand_mean)**2)
EMS = (n * WMS - JMS) / (n - 1)

icc_agreement = (BMS - EMS) / (BMS + EMS + 2 * (JMS - EMS) / n)
icc_consistency = (BMS - EMS) / (BMS + EMS)
r = np.corrcoef(m1, m2)[0, 1]

print("\n--- Reliability ---")
print(f"ICC(2,1) agreement:   {icc_agreement:.3f}")
print(f"ICC(3,1) consistency: {icc_consistency:.3f}")
print(f"Pearson r:            {r:.3f}")

print("\n--- Summary ---")
print(f"Original: {np.mean(m1):.4f} ± {np.std(m1, ddof=1):.4f} mm")
print(f"Retest:   {np.mean(m2):.4f} ± {np.std(m2, ddof=1):.4f} mm")