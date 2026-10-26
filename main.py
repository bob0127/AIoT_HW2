# ============================================================
# WINE QUALITY - CRISP-DM MULTIPLE LINEAR REGRESSION
#
# Supports Separate Analysis for Red Wine and White Wine
# 11 Physicochemical Features + Intercept
# Target: Quality (Sensory Score 0-10)
#
# Feature Selection Methods:
# 1. LassoCV
# 2. RFECV
# 3. Sequential Forward Selection (SFS)
# 4. ElasticNetCV
# 5. Exhaustive Feature Selection
#
# Plus: Baseline OLS, VIF, CV, Metrics, Plots, Top 10 Outliers
#
# pip install numpy pandas matplotlib scikit-learn statsmodels
# ============================================================

import os
import sys
import argparse
import itertools
import urllib.request
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for clean file generation
import matplotlib.pyplot as plt

from sklearn.model_selection import (
    train_test_split, KFold, cross_val_score
)
from sklearn.linear_model import (
    LinearRegression, LassoCV, ElasticNetCV
)
from sklearn.feature_selection import (
    RFECV, SequentialFeatureSelector
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score
)
from statsmodels.stats.outliers_influence import (
    variance_inflation_factor
)
import statsmodels.api as sm


RANDOM_STATE = 42
FEATURES = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol"
]
TARGET = "quality"

DATASET_CONFIG = {
    "red": {
        "name": "Red Wine",
        "title": "Red Wine Quality",
        "filename": "winequality-red.csv",
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
        "prefix": "red_wine",
        "output_dir": "results_red_wine",
        "sample_wine": {
            "fixed acidity": 8.3,
            "volatile acidity": 0.53,
            "citric acid": 0.27,
            "residual sugar": 2.5,
            "chlorides": 0.08,
            "free sulfur dioxide": 16.0,
            "total sulfur dioxide": 46.0,
            "density": 0.9967,
            "pH": 3.31,
            "sulphates": 0.65,
            "alcohol": 10.4
        }
    },
    "white": {
        "name": "White Wine",
        "title": "White Wine Quality",
        "filename": "winequality-white.csv",
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv",
        "prefix": "white_wine",
        "output_dir": "results_white_wine",
        "sample_wine": {
            "fixed acidity": 6.85,
            "volatile acidity": 0.28,
            "citric acid": 0.33,
            "residual sugar": 6.39,
            "chlorides": 0.046,
            "free sulfur dioxide": 35.3,
            "total sulfur dioxide": 138.4,
            "density": 0.9940,
            "pH": 3.19,
            "sulphates": 0.49,
            "alcohol": 10.5
        }
    }
}


def load_dataset(wine_type: str) -> pd.DataFrame:
    """Load local wine dataset file, downloading from UCI if not found."""
    cfg = DATASET_CONFIG[wine_type]
    filename = cfg["filename"]

    if not os.path.exists(filename):
        print(f"Local file {filename} not found. Downloading from UCI repository...")
        try:
            urllib.request.urlretrieve(cfg["url"], filename)
            print(f"Downloaded and saved to {filename}")
        except Exception as e:
            print(f"Download failed: {e}. Attempting direct read from URL...")
            return pd.read_csv(cfg["url"], sep=";")

    df = pd.read_csv(filename, sep=";")
    return df


def metrics(y_true, y_pred, p):
    n = len(y_true)
    r2 = r2_score(y_true, y_pred)
    adjusted = (
        1 - (1 - r2) * (n - 1) / (n - p - 1)
        if n > p + 1 else np.nan
    )
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "MSE": mean_squared_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2,
        "Adjusted_R2": adjusted
    }


def run_crisp_dm(wine_type: str = "red", show_plots: bool = False):
    cfg = DATASET_CONFIG[wine_type]
    wine_name = cfg["name"]
    prefix = cfg["prefix"]
    output_dir = cfg["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 65)
    print(f"   CRISP-DM REGRESSION ANALYSIS: {wine_name.upper()}")
    print("=" * 65)

    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    # ============================================================
    # PHASE 1: BUSINESS UNDERSTANDING
    # ============================================================
    print("\n" + "=" * 50)
    print("PHASE 1: BUSINESS UNDERSTANDING")
    print("=" * 50)
    print(f"Goal: Predict sensory quality rating (0-10) for {wine_name}.")
    print("Features: 11 physicochemical laboratory measurements.")
    print("Objective: Compare 5 feature selection methods against Baseline OLS")
    print("           to identify key chemical drivers of wine quality.")

    # ============================================================
    # PHASE 2: DATA UNDERSTANDING
    # ============================================================
    print("\n" + "=" * 50)
    print("PHASE 2: DATA UNDERSTANDING")
    print("=" * 50)
    df = load_dataset(wine_type)
    print("Shape:", df.shape)
    print("\nFirst 5 records:")
    print(df.head())
    print("\nMissing values:")
    print(df.isna().sum())
    print("\nTarget ('quality') distribution:")
    print(df["quality"].value_counts().sort_index())

    # ============================================================
    # PHASE 3: DATA PREPARATION
    # ============================================================
    print("\n" + "=" * 50)
    print("PHASE 3: DATA PREPARATION")
    print("=" * 50)

    X = df[FEATURES].astype(float)
    y = df[TARGET].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=RANDOM_STATE
    )

    print("Features (11):", FEATURES)
    print("Train sample size:", len(X_train))
    print("Test sample size:", len(X_test))

    # ============================================================
    # MODELING HELPERS
    # ============================================================
    def evaluate_subset(name, selected_features):
        selected_features = list(selected_features)
        model = LinearRegression()
        model.fit(X_train[selected_features], y_train)

        predictions = model.predict(X_test[selected_features])

        cv_rmse = -cross_val_score(
            LinearRegression(),
            X_train[selected_features],
            y_train,
            cv=cv,
            scoring="neg_root_mean_squared_error"
        )

        result = metrics(y_test, predictions, len(selected_features))
        result.update({
            "Method": name,
            "N_Features": len(selected_features),
            "Selected_Features": ", ".join(selected_features),
            "CV_RMSE": cv_rmse.mean()
        })
        return result, model, predictions

    results = []
    fitted_models = {}

    def register(name, selected):
        result, model, predictions = evaluate_subset(name, selected)
        results.append(result)
        fitted_models[name] = {
            "model": model,
            "features": list(selected),
            "predictions": predictions
        }
        print(f"\n[{name}]")
        print("  Selected Features ({}): {}".format(len(selected), list(selected)))
        print(f"  CV RMSE: {result['CV_RMSE']:.4f}")
        print(f"  Test R2: {result['R2']:.4f}")
        print(f"  Test RMSE: {result['RMSE']:.4f}")

    # ============================================================
    # PHASE 4: MODELING
    # ============================================================
    print("\n" + "=" * 50)
    print("PHASE 4: MODELING")
    print("=" * 50)

    # ------------------------------------------------------------
    # MODEL 0: BASELINE OLS
    # ------------------------------------------------------------
    register("Baseline OLS", FEATURES)

    # ------------------------------------------------------------
    # MODEL 1: LassoCV Feature Selection
    # ------------------------------------------------------------
    lasso_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("lasso", LassoCV(
            cv=cv,
            max_iter=100000,
            random_state=RANDOM_STATE
        ))
    ])
    lasso_pipe.fit(X_train, y_train)
    lasso_coef = lasso_pipe.named_steps["lasso"].coef_
    lasso_selected = [
        f for f, c in zip(FEATURES, lasso_coef)
        if abs(c) > 1e-8
    ]
    if not lasso_selected:
        lasso_selected = [FEATURES[np.argmax(abs(lasso_coef))]]
    register("LassoCV", lasso_selected)

    # ------------------------------------------------------------
    # MODEL 2: RFECV
    # ------------------------------------------------------------
    rfecv = RFECV(
        estimator=LinearRegression(),
        step=1,
        cv=cv,
        scoring="neg_root_mean_squared_error",
        min_features_to_select=1
    )
    rfecv_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("selector", rfecv)
    ])
    rfecv_pipe.fit(X_train, y_train)
    rfecv_selected = list(
        X_train.columns[rfecv_pipe.named_steps["selector"].support_]
    )
    register("RFECV", rfecv_selected)

    # ------------------------------------------------------------
    # MODEL 3: Sequential Forward Selection (SFS)
    # ------------------------------------------------------------
    best_sfs_score = np.inf
    best_sfs_features = None

    for k in range(1, len(FEATURES) + 1):
        if k == len(FEATURES):
            selected = FEATURES
        else:
            sfs = SequentialFeatureSelector(
                estimator=LinearRegression(),
                n_features_to_select=k,
                direction="forward",
                scoring="neg_root_mean_squared_error",
                cv=cv
            )
            sfs.fit(X_train, y_train)
            selected = list(X_train.columns[sfs.get_support()])

        score = -cross_val_score(
            LinearRegression(),
            X_train[selected],
            y_train,
            cv=cv,
            scoring="neg_root_mean_squared_error"
        ).mean()

        if score < best_sfs_score:
            best_sfs_score = score
            best_sfs_features = selected

    register("Forward SFS", best_sfs_features)

    # ------------------------------------------------------------
    # MODEL 4: ElasticNetCV
    # ------------------------------------------------------------
    elastic_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("elastic", ElasticNetCV(
            l1_ratio=[0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 1.0],
            cv=cv,
            max_iter=100000,
            random_state=RANDOM_STATE
        ))
    ])
    elastic_pipe.fit(X_train, y_train)
    elastic_coef = elastic_pipe.named_steps["elastic"].coef_
    elastic_selected = [
        f for f, c in zip(FEATURES, elastic_coef)
        if abs(c) > 1e-8
    ]
    if not elastic_selected:
        elastic_selected = [FEATURES[np.argmax(abs(elastic_coef))]]
    register("ElasticNetCV", elastic_selected)

    # ------------------------------------------------------------
    # MODEL 5: Exhaustive Feature Selection (Optimized exact CV)
    # ------------------------------------------------------------
    # Precompute fold normal equations for instantaneous exact 5-fold CV
    X_tr_vals = X_train.values
    y_tr_vals = y_train.values
    X_const = np.column_stack([np.ones(len(X_tr_vals)), X_tr_vals])

    cv_folds = []
    for tr_idx, va_idx in cv.split(X_const):
        X_f_tr, y_f_tr = X_const[tr_idx], y_tr_vals[tr_idx]
        X_f_va, y_f_va = X_const[va_idx], y_tr_vals[va_idx]
        XtX = X_f_tr.T @ X_f_tr
        Xty = X_f_tr.T @ y_f_tr
        cv_folds.append((XtX, Xty, X_f_va, y_f_va))

    n_feats = len(FEATURES)
    best_exhaustive_score = np.inf
    best_exhaustive_features = None

    for k in range(1, n_feats + 1):
        for subset in itertools.combinations(range(1, n_feats + 1), k):
            sub_idx = [0] + list(subset)
            rmses = []
            for XtX, Xty, X_va, y_va in cv_folds:
                sub_XtX = XtX[np.ix_(sub_idx, sub_idx)]
                sub_Xty = Xty[sub_idx]
                beta = np.linalg.solve(sub_XtX, sub_Xty)
                pred = X_va[:, sub_idx] @ beta
                rmses.append(np.sqrt(np.mean((y_va - pred) ** 2)))
            cv_rmse = np.mean(rmses)
            if cv_rmse < best_exhaustive_score:
                best_exhaustive_score = cv_rmse
                best_exhaustive_features = [FEATURES[i - 1] for i in subset]

    register("Exhaustive", best_exhaustive_features)

    # ============================================================
    # PHASE 5: EVALUATION
    # ============================================================
    print("\n" + "=" * 50)
    print("PHASE 5: EVALUATION")
    print("=" * 50)

    results_df = pd.DataFrame(results)
    results_df = results_df[[
        "Method",
        "N_Features",
        "Selected_Features",
        "CV_RMSE",
        "MAE",
        "MSE",
        "RMSE",
        "R2",
        "Adjusted_R2"
    ]]
    results_df = results_df.sort_values("CV_RMSE")

    print(f"\n=== MODEL COMPARISON: {wine_name} ===")
    print(results_df.round(4).to_string(index=False))

    # Save comparison CSVs
    csv_paths = [
        f"{output_dir}/feature_selection_comparison.csv",
        f"{prefix}_feature_selection_comparison.csv"
    ]
    for cp in csv_paths:
        results_df.to_csv(cp, index=False)

    best_method = results_df.iloc[0]["Method"]
    best_features = fitted_models[best_method]["features"]
    best_model = fitted_models[best_method]["model"]

    print(f"\nBest method by training CV RMSE ({wine_name}):", best_method)
    print("Selected features:", best_features)

    # ------------------------------------------------------------
    # VIF CHECK
    # ------------------------------------------------------------
    print(f"\n=== VIF: SELECTED FEATURES ({wine_name}) ===")
    X_vif = sm.add_constant(X_train[best_features], has_constant="add")
    vif_vals = np.asarray(X_vif.values, dtype=float)
    vif_table = pd.DataFrame({
        "Feature": X_vif.columns,
        "VIF": [
            variance_inflation_factor(vif_vals, i)
            for i in range(vif_vals.shape[1])
        ]
    })
    print(vif_table.round(3).to_string(index=False))

    # ------------------------------------------------------------
    # PLOT 1: FEATURE SELECTION COMPARISON
    # ------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    plt.barh(results_df["Method"], results_df["CV_RMSE"], color="#3b82f6", edgecolor="#1d4ed8")
    plt.xlabel("Cross-Validated RMSE (Lower is Better)")
    plt.title(f"{wine_name}: Feature Selection Method Comparison")
    plt.gca().invert_yaxis()
    plt.grid(axis="x", alpha=0.3, linestyle="--")
    plt.tight_layout()

    p1_paths = [
        f"{output_dir}/feature_selection_comparison.png",
        f"{prefix}_feature_selection_comparison.png"
    ]
    for p in p1_paths:
        plt.savefig(p, dpi=300)
    if show_plots:
        plt.show()
    plt.close()

    # ------------------------------------------------------------
    # PLOT 2: ACTUAL VS PREDICTED (TEST SET)
    # ------------------------------------------------------------
    test_pred = best_model.predict(X_test[best_features])

    plt.figure(figsize=(8, 7))
    plt.scatter(y_test, test_pred, s=50, alpha=0.6, color="#4f46e5", edgecolors="none")

    lower = min(y_test.min(), test_pred.min()) - 0.2
    upper = max(y_test.max(), test_pred.max()) + 0.2

    plt.plot([lower, upper], [lower, upper], "r--", linewidth=1.5, label="Perfect Prediction (y=x)")
    plt.xlabel("Actual Quality Score")
    plt.ylabel("Predicted Quality Score")
    plt.title(f"{wine_name} - Actual vs Predicted: {best_method}")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()

    p2_paths = [
        f"{output_dir}/actual_vs_predicted.png",
        f"{prefix}_actual_vs_predicted.png"
    ]
    for p in p2_paths:
        plt.savefig(p, dpi=300)
    if show_plots:
        plt.show()
    plt.close()

    # ------------------------------------------------------------
    # TOP 10 OUTLIERS: DESCRIPTIVE FULL-DATA REFIT
    # ------------------------------------------------------------
    full_model = LinearRegression()
    full_model.fit(X[best_features], y)

    outliers = df.copy()
    outliers["Predicted_Quality"] = full_model.predict(X[best_features])
    outliers["Residual"] = outliers[TARGET] - outliers["Predicted_Quality"]
    outliers["Absolute_Residual"] = outliers["Residual"].abs()

    top10 = outliers.nlargest(10, "Absolute_Residual").copy()
    top10.insert(0, "Rank", np.arange(1, len(top10) + 1))
    top10.insert(1, "Original_Index", top10.index)

    print(f"\n=== TOP 10 ABSOLUTE RESIDUALS ({wine_name}) ===")
    display_cols = ["Rank", "Original_Index", "quality", "Predicted_Quality", "Residual", "Absolute_Residual"]
    print(top10[display_cols].round(3).to_string(index=False))

    outlier_paths = [
        f"{output_dir}/top10_outliers.csv",
        f"{prefix}_top10_outliers.csv"
    ]
    for op in outlier_paths:
        top10.to_csv(op, index=False)

    # ------------------------------------------------------------
    # PLOT 3: SCATTER + TOP 10 OUTLIERS
    # ------------------------------------------------------------
    plt.figure(figsize=(10, 8))

    # Color scatter by actual quality score
    distinct_qualities = sorted(outliers[TARGET].unique())
    color_palette = plt.cm.tab10(np.linspace(0, 1, len(distinct_qualities)))

    for q_val, color in zip(distinct_qualities, color_palette):
        sub = outliers[outliers[TARGET] == q_val]
        plt.scatter(
            sub[TARGET],
            sub["Predicted_Quality"],
            label=f"Quality {int(q_val)}",
            color=color,
            alpha=0.6,
            s=45
        )

    min_val = min(outliers[TARGET].min(), outliers["Predicted_Quality"].min()) - 0.2
    max_val = max(outliers[TARGET].max(), outliers["Predicted_Quality"].max()) + 0.2

    # Reference y = x line
    plt.plot([min_val, max_val], [min_val, max_val], "k--", label="y = x", linewidth=1.5)

    # Trend line
    slope, intercept = np.polyfit(outliers[TARGET], outliers["Predicted_Quality"], 1)
    line_x = np.linspace(min_val, max_val, 200)
    plt.plot(line_x, slope * line_x + intercept, color="#ea580c", linewidth=2, label="Scatter Trend Line")

    # Highlight Top 10 largest residuals with red circle rings
    for _, row in top10.iterrows():
        xx = row[TARGET]
        yy = row["Predicted_Quality"]
        plt.scatter(xx, yy, s=200, facecolors="none", edgecolors="red", linewidths=2)
        plt.annotate(
            str(int(row["Rank"])),
            (xx, yy),
            xytext=(6, 7),
            textcoords="offset points",
            fontweight="bold",
            color="red"
        )

    plt.xlabel("Actual Quality Score")
    plt.ylabel("Predicted Quality Score")
    plt.title(f"{wine_name}: {best_method}\nTop 10 Largest Absolute Residuals")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.grid(alpha=0.25)
    plt.tight_layout()

    p3_paths = [
        f"{output_dir}/top10_outliers_plot.png",
        f"{prefix}_top10_outliers_plot.png"
    ]
    for p in p3_paths:
        plt.savefig(p, dpi=300)
    if show_plots:
        plt.show()
    plt.close()

    # ============================================================
    # PHASE 6: DEPLOYMENT
    # ============================================================
    print("\n" + "=" * 50)
    print("PHASE 6: DEPLOYMENT")
    print("=" * 50)

    sample_wine = pd.DataFrame([cfg["sample_wine"]])
    predicted_quality = full_model.predict(sample_wine[best_features])[0]

    print(f"Sample {wine_name} physicochemical properties:")
    for k, v in cfg["sample_wine"].items():
        print(f"  {k}: {v}")
    print(f"\nPredicted {wine_name} quality score: {predicted_quality:.2f} / 10")

    print(f"\nFiles saved for {wine_name}:")
    for cp in csv_paths:
        print(" ", cp)
    for p in p1_paths:
        print(" ", p)
    for p in p2_paths:
        print(" ", p)
    for op in outlier_paths:
        print(" ", op)
    for p in p3_paths:
        print(" ", p)

    return results_df, best_method, best_features


def main():
    parser = argparse.ArgumentParser(
        description="CRISP-DM Regression Analysis on Wine Quality (Red & White)"
    )
    parser.add_argument(
        "--wine",
        type=str,
        choices=["red", "white", "both"],
        default="both",
        help="Wine type to analyze: 'red', 'white', or 'both' (default: 'both')"
    )
    parser.add_argument(
        "--show-plots",
        action="store_true",
        help="Display matplotlib interactive plots"
    )
    args = parser.parse_args()

    if args.wine in ["red", "both"]:
        run_crisp_dm("red", show_plots=args.show_plots)

    if args.wine in ["white", "both"]:
        run_crisp_dm("white", show_plots=args.show_plots)

    print("\n" + "=" * 65)
    print("ALL ANALYSES COMPLETED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    main()