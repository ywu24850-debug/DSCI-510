import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import config
import os
import matplotlib.pyplot as plt

def run_final_xg_regressor(df_full):
    print("\nTraining Regressor")
    features = config.features
    target = config.target
    df_model = df_full.dropna(subset=features + [target])
    X = df_model[features]
    y = df_model[target]
    y_true_class = df_model['target_1x2']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    _, _, _, y_test_class = train_test_split(X, y_true_class, test_size=0.2, shuffle=False, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    print(f"\nEvaluation")
    print(f"RMSE: {rmse:.4f} ")
    print(f"R2 Score: {r2:.4f}")

    draw_threshold = 0.3
    preds = []
    for p in predictions:
        if p > draw_threshold:
            preds.append(0)
        elif p < -draw_threshold:
            preds.append(2)
        else:
            preds.append(1)
    acc = accuracy_score(y_test_class, preds)
    print(f"Accuracy: {acc * 100:.2f}% ")

    if not os.path.exists(config.results_dir): os.makedirs(config.results_dir)
    feature_names = features
    importance_df = pd.DataFrame({
         'Feature': feature_names,
         'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    importance_df.plot(kind='barh', x='Feature', y='Importance', ax=ax, legend=False)
    ax.set_title('Feature Importance')
    plt.tight_layout()
    save_path = os.path.join(config.results_dir, 'feature_importance.png')
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")
    print("\nTop 5 Important Features:")
    print(importance_df.tail(5)[::-1].to_string(index=False))