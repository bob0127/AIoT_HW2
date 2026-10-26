import os
import sys
import argparse
import itertools
import urllib.request
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LassoCV, ElasticNetCV
from sklearn.feature_selection import SequentialFeatureSelector, RFE
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score


DATASETS = {
    "red": {
        "name": "Red Wine",
        "filename": "winequality-red.csv",
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
        "prefix": "red_wine",
        "output_dir": "progression_red_wine"
    },
    "white": {
        "name": "White Wine",
        "filename": "winequality-white.csv",
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv",
        "prefix": "white_wine",
        "output_dir": "progression_white_wine"
    }
}


def load_dataset(wine_type: str) -> pd.DataFrame:
    cfg = DATASETS[wine_type]
    filename = cfg["filename"]
    if not os.path.exists(filename):
        print(f"Downloading {filename} from UCI...")
        urllib.request.urlretrieve(cfg["url"], filename)
    return pd.read_csv(filename, sep=";")


def run_progression_analysis(wine_type: str = "red"):
    cfg = DATASETS[wine_type]
    wine_name = cfg["name"]
    prefix = cfg["prefix"]
    output_dir = cfg["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 65)
    print(f" FEATURE PROGRESSION ANALYSIS: {wine_name.upper()}")
    print("=" * 65)

    # 1. Load Data
    df = load_dataset(wine_type)
    features = [c for c in df.columns if c != "quality"]
    n_features = len(features)

    X = df[features].astype(float)
    y = df["quality"].astype(float)

    # Split matching benchmark: random_state=0, test_size=0.20
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=0
    )

    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=features)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=features)

    def evaluate_subset(features_subset):
        sub = list(features_subset)
        model = LinearRegression()
        model.fit(X_train[sub], y_train)
        y_pred = model.predict(X_test[sub])
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        return rmse, r2

    algorithms = {}

    # 1. Lasso Ranking (by standardized coefficient magnitude)
    print(f"\n[1/5] Running Lasso (L1 Ranking) for {wine_name}...")
    lasso_cv = LassoCV(cv=5, random_state=0, max_iter=100000).fit(X_train_scaled, y_train)
    lasso_rank = [f for _, f in sorted(zip(abs(lasso_cv.coef_), features), reverse=True)]
    algorithms["Lasso (L1 Ranking)"] = [lasso_rank[:k] for k in range(1, n_features + 1)]

    # 2. Forward SFS
    print(f"[2/5] Running Forward SFS for {wine_name}...")
    sfs_subsets = []
    for k in range(1, n_features + 1):
        if k == n_features:
            sfs_subsets.append(features)
        else:
            sfs = SequentialFeatureSelector(
                LinearRegression(),
                n_features_to_select=k,
                direction="forward"
            )
            sfs.fit(X_train, y_train)
            sfs_subsets.append(list(X_train.columns[sfs.get_support()]))
    algorithms["Forward SFS"] = sfs_subsets

    # 3. Recursive Feature Elimination (RFE)
    print(f"[3/5] Running Recursive Feature Elimination (RFE) for {wine_name}...")
    rfe_subsets = []
    for k in range(1, n_features + 1):
        if k == n_features:
            rfe_subsets.append(features)
        else:
            rfe = RFE(LinearRegression(), n_features_to_select=k)
            rfe.fit(X_train_scaled, y_train)
            rfe_subsets.append(list(X_train.columns[rfe.get_support()]))
    algorithms["RFE"] = rfe_subsets

    # 4. ElasticNet Ranking
    print(f"[4/5] Running ElasticNet Ranking for {wine_name}...")
    enet_cv = ElasticNetCV(cv=5, random_state=0, max_iter=100000).fit(X_train_scaled, y_train)
    enet_rank = [f for _, f in sorted(zip(abs(enet_cv.coef_), features), reverse=True)]
    algorithms["ElasticNet Ranking"] = [enet_rank[:k] for k in range(1, n_features + 1)]

    # 5. Exhaustive Search (Best Subset Selection per k via fast OLS normal equations)
    print(f"[5/5] Running Exhaustive Search for {wine_name}...")
    X_tr_mat = np.column_stack([np.ones(len(X_train)), X_train.values])
    y_tr_vec = y_train.values
    X_te_mat = np.column_stack([np.ones(len(X_test)), X_test.values])
    y_te_vec = y_test.values

    XtX = X_tr_mat.T @ X_tr_mat
    Xty = X_tr_mat.T @ y_tr_vec

    exhaustive_subsets = []
    for k in range(1, n_features + 1):
        best_rmse = float("inf")
        best_sub = None
        for sub in itertools.combinations(range(1, n_features + 1), k):
            sub_idx = [0] + list(sub)
            beta = np.linalg.solve(XtX[np.ix_(sub_idx, sub_idx)], Xty[sub_idx])
            pred = X_te_mat[:, sub_idx] @ beta
            rmse = np.sqrt(np.mean((y_te_vec - pred) ** 2))
            if rmse < best_rmse:
                best_rmse = rmse
                best_sub = [features[i - 1] for i in sub]
        exhaustive_subsets.append(best_sub)
    algorithms["Exhaustive Search"] = exhaustive_subsets

    # Evaluate and compile results
    all_dfs = {}
    for name, subsets in algorithms.items():
        records = []
        for k, sub in enumerate(subsets, start=1):
            rmse, r2 = evaluate_subset(sub)
            records.append({
                "Number of Features": k,
                "Selected Features": str(sub),
                "RMSE": rmse,
                "R-squared": r2
            })
        df_res = pd.DataFrame(records)
        all_dfs[name] = df_res

        clean_name = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        csv_name = f"{clean_name}_progression.csv"

        # Save to both dedicated folder and workspace root with prefix
        df_res.to_csv(f"{output_dir}/{csv_name}", index=False)
        df_res.to_csv(f"{prefix}_{csv_name}", index=False)

        print(f"\n===== {wine_name}: {name} =====")
        print(df_res[["Number of Features", "RMSE", "R-squared"]].round(4).to_string(index=False))

        # Plot individual 2-panel chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Left: RMSE
        ax1.plot(df_res["Number of Features"], df_res["RMSE"], marker="o", linewidth=2, color="#1f77b4")
        ax1.set_title(f"{wine_name}: RMSE by Number of Features", fontsize=12, pad=10)
        ax1.set_xlabel("Number of Features", fontsize=11)
        ax1.set_ylabel("RMSE", fontsize=11)
        ax1.set_xticks(range(1, n_features + 1))
        ax1.grid(True, linestyle=":", alpha=0.6)

        # Right: R-squared
        ax2.plot(df_res["Number of Features"], df_res["R-squared"], marker="o", linewidth=2, color="#1f77b4")
        ax2.set_title(f"{wine_name}: R-squared by Number of Features", fontsize=12, pad=10)
        ax2.set_xlabel("Number of Features", fontsize=11)
        ax2.set_ylabel("R-squared", fontsize=11)
        ax2.set_xticks(range(1, n_features + 1))
        ax2.grid(True, linestyle=":", alpha=0.6)

        plt.suptitle(f"{wine_name} - {name}", fontsize=14, fontweight="bold", y=1.02)
        plt.tight_layout()

        plot_name = f"{clean_name}_plot.png"
        plt.savefig(f"{output_dir}/{plot_name}", dpi=300, bbox_inches="tight")
        plt.savefig(f"{prefix}_{plot_name}", dpi=300, bbox_inches="tight")
        plt.close()

    # Combined Comparison Plot across all 5 algorithms
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    markers = ["o", "s", "^", "D", "v"]

    for (name, df_res), color, marker in zip(all_dfs.items(), colors, markers):
        ax1.plot(df_res["Number of Features"], df_res["RMSE"], marker=marker, linewidth=1.8, label=name, color=color)
        ax2.plot(df_res["Number of Features"], df_res["R-squared"], marker=marker, linewidth=1.8, label=name, color=color)

    ax1.set_title(f"{wine_name}: RMSE Comparison across 5 Methods", fontsize=12, pad=10)
    ax1.set_xlabel("Number of Features", fontsize=11)
    ax1.set_ylabel("RMSE (Lower is Better)", fontsize=11)
    ax1.set_xticks(range(1, n_features + 1))
    ax1.legend()
    ax1.grid(True, linestyle=":", alpha=0.6)

    ax2.set_title(f"{wine_name}: R-squared Comparison across 5 Methods", fontsize=12, pad=10)
    ax2.set_xlabel("Number of Features", fontsize=11)
    ax2.set_ylabel("R-squared (Higher is Better)", fontsize=11)
    ax2.set_xticks(range(1, n_features + 1))
    ax2.legend()
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.suptitle(f"{wine_name} - Feature Progression Benchmark", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()

    comb_plot = "all_5_algorithms_comparison_plot.png"
    plt.savefig(f"{output_dir}/{comb_plot}", dpi=300, bbox_inches="tight")
    plt.savefig(f"{prefix}_{comb_plot}", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nAll progression plots and CSVs for {wine_name} successfully generated in '{output_dir}/' and root directory!")


def main():
    parser = argparse.ArgumentParser(
        description="Feature Progression Analysis across k=1..11 for Wine Quality (Red & White)"
    )
    parser.add_argument(
        "--wine",
        type=str,
        choices=["red", "white", "both"],
        default="both",
        help="Wine type to analyze: 'red', 'white', or 'both' (default: 'both')"
    )
    args = parser.parse_args()

    if args.wine in ["red", "both"]:
        run_progression_analysis("red")

    if args.wine in ["white", "both"]:
        run_progression_analysis("white")

    print("\n" + "=" * 65)
    print("ALL FEATURE PROGRESSION ANALYSES COMPLETED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    main()
