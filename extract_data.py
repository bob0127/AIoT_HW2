import json
import itertools
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def process_wine(wine_type):
    fname = f"winequality-{wine_type}.csv"
    df = pd.read_csv(fname, sep=";")
    features = [c for c in df.columns if c != "quality"]
    X = df[features].astype(float)
    y = df["quality"].astype(float)
    
    # Main model split (random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    cv = KFold(5, shuffle=True, random_state=42)
    
    comp_df = pd.read_csv(f"results_{wine_type}_wine/feature_selection_comparison.csv")
    
    models = []
    for _, row in comp_df.iterrows():
        sub_feats = [f.strip() for f in row["Selected_Features"].split(",")]
        m = LinearRegression().fit(X_tr[sub_feats], y_tr)
        coef_dict = {f: float(c) for f, c in zip(sub_feats, m.coef_)}
        is_best = bool(row["Method"] == comp_df.iloc[0]["Method"])
        models.append({
            "id": row["Method"].replace(" ", "_"),
            "name": row["Method"],
            "features": sub_feats,
            "nFeat": int(row["N_Features"]),
            "cvRmse": float(row["CV_RMSE"]),
            "mae": float(row["MAE"]),
            "rmse": float(row["RMSE"]),
            "r2": float(row["R2"]),
            "adjR2": float(row["Adjusted_R2"]),
            "intercept": float(m.intercept_),
            "coefs": coef_dict,
            "isBest": is_best,
            "tag": "BEST CV RMSE" if is_best else f"{row['N_Features']} FEAT"
        })
    
    # Outliers
    out_df = pd.read_csv(f"results_{wine_type}_wine/top10_outliers.csv")
    outliers = []
    for _, r in out_df.iterrows():
        outliers.append({
            "rank": int(r["Rank"]),
            "id": int(r["Original_Index"]),
            "actual": float(r["quality"]),
            "pred": float(r["Predicted_Quality"]),
            "res": float(r["Residual"]),
            "abs_res": float(r["Absolute_Residual"]),
            "alcohol": float(r["alcohol"]),
            "volatile_acidity": float(r["volatile acidity"]),
            "density": float(r["density"])
        })
        
    # Progression data from CSVs
    algo_keys = [
        ("LassoCV", "lasso_l1_ranking"),
        ("Forward_SFS", "forward_sfs"),
        ("RFECV", "rfe"),
        ("ElasticNetCV", "elasticnet_ranking"),
        ("Exhaustive", "exhaustive_search")
    ]
    prog_data = {}
    
    X_tr_prog, X_te_prog, y_tr_prog, y_te_prog = train_test_split(X, y, test_size=0.2, random_state=0)
    
    for algo_id, fname_key in algo_keys:
        p_csv = pd.read_csv(f"progression_{wine_type}_wine/{fname_key}_progression.csv")
        items = []
        min_rmse = p_csv["RMSE"].min()
        for _, pr in p_csv.iterrows():
            k_val = int(pr["Number of Features"])
            sub_feats = eval(pr["Selected Features"])
            m_sub = LinearRegression().fit(X_tr_prog[sub_feats], y_tr_prog)
            is_sweet = bool(abs(pr["RMSE"] - min_rmse) < 1e-6)
            is_cliff = bool(k_val == 11 and pr["RMSE"] > min_rmse)
            items.append({
                "k": k_val,
                "features": sub_feats,
                "rmse": float(pr["RMSE"]),
                "r2": float(pr["R-squared"]),
                "intercept": float(m_sub.intercept_),
                "coefs": {f: float(c) for f, c in zip(sub_feats, m_sub.coef_)},
                "isSweetSpot": is_sweet,
                "isOverfitCliff": is_cliff
            })
        prog_data[algo_id] = items
        
    # Test samples for scatter plot (distributed samples)
    step = max(1, len(X_te) // 40)
    best_feats = models[0]["features"]
    m_best = LinearRegression().fit(X_tr[best_feats], y_tr)
    preds = m_best.predict(X_te[best_feats])
    test_samples = []
    for i in range(0, len(X_te), step):
        idx = X_te.index[i]
        test_samples.append({
            "id": int(idx),
            "actual": float(y_te.iloc[i]),
            "pred": float(preds[i]),
            "res": float(y_te.iloc[i] - preds[i]),
            "features": {f: float(X_te.iloc[i][f]) for f in features}
        })
        
    feat_stats = {}
    for f in features:
        feat_stats[f] = {
            "min": round(float(df[f].min()), 3),
            "max": round(float(df[f].max()), 3),
            "mean": round(float(df[f].mean()), 3),
            "median": round(float(df[f].median()), 3)
        }
        
    return {
        "name": "Red Wine" if wine_type == "red" else "White Wine",
        "sample_count": len(df),
        "features": features,
        "models": models,
        "outliers": outliers,
        "progressions": prog_data,
        "test_samples": test_samples,
        "feature_stats": feat_stats
    }

data = {
    "red": process_wine("red"),
    "white": process_wine("white")
}

with open("wine_web_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Generated wine_web_data.json successfully! Size:", len(json.dumps(data)))
