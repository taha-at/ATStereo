import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

# one CSV per operator, column "RMSE" in mm
files = {f"Op{i}": f"ATStereo_Phase1_RMSE_op{i}.csv" for i in range(1, 6)}

df = pd.concat(
    [pd.DataFrame({"operator": op, "rmse": pd.read_csv(f)["RMSE"].astype(float)})
     for op, f in files.items()],
    ignore_index=True,
)
print("N =", len(df))
print(df["operator"].value_counts().sort_index())

# random-intercept model: rmse = b0 + u_operator + e
mdf = smf.mixedlm("rmse ~ 1", df, groups=df["operator"]).fit(reml=True)
b0, se = mdf.params["Intercept"], mdf.bse["Intercept"]
var_u, var_e = mdf.cov_re.iloc[0, 0], mdf.scale

# t-based CI, df = operators - 1
dof = df["operator"].nunique() - 1
tc = stats.t.ppf(0.975, dof)
print(f"\nconverged: {mdf.converged}")
print(f"mean {b0:.4f} mm, SE {se:.4f}, 95% CI [{b0 - tc*se:.4f}, {b0 + tc*se:.4f}] (t, df={dof})")
print(f"between-operator SD {np.sqrt(var_u):.2f}, residual SD {np.sqrt(var_e):.2f}")
print(f"between-operator var {var_u:.6f}, residual var {var_e:.6f}, ICC {var_u/(var_u+var_e):.3f}")
print(f"stats.t.ppf(0.975, 4): {stats.t.ppf(0.975, 4)}")

# per-operator table (compare with Table 1)
g = df.groupby("operator")["rmse"]
table = pd.DataFrame({
    "N": g.count(), "mean": g.mean(), "SD": g.std(),
    "median": g.median(), "Q25": g.quantile(0.25), "Q75": g.quantile(0.75),
    "min": g.min(), "max": g.max(),
})
print("\n", table.round(3))

# secondary: pooled mean, SD, median, and mean of operator means
om = g.mean()
se_om = om.std(ddof=1) / np.sqrt(len(om))
tc_om = stats.t.ppf(0.975, len(om) - 1)
print(f"\npooled mean {df['rmse'].mean():.4f} +/- {df['rmse'].std():.4f}")
print(f"pooled median {df['rmse'].median():.4f}")
print(f"pooled range {df['rmse'].min():.2f} -- {df['rmse'].max():.2f}")
print(f"mean of operator means {om.mean():.4f} +/- {om.std(ddof=1):.4f} [{om.mean() - tc_om*se_om:.4f}, {om.mean() + tc_om*se_om:.4f}]")
