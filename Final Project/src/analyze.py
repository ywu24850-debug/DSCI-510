import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import config
import os
import matplotlib.pyplot as plt

def match_classifier(df_full):
    print("\nTraining Match Result Classifier")
    if df_full is None:
        print("Data loading failed.")
        return
    features = config.FEATURES
    target = config.TARGET

    df_model = df_full.dropna(subset=features + [target])
    print(f"\n{len(df_model)} / {len(df_full)} clean rows ")
    if len(df_model) < 100:
        print("Too few rows after dropna")
        return

    X = df_model[features]
    y = df_model[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False, random_state=42)
    print(f"Training set size: {len(X_train)} matches")
    print(f"Test set size: {len(X_test)} matches")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("\nTraining Classifier...")
    model = XGBClassifier(
        objective='multi:softmax',
        num_class=3,
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42,
        early_stopping_rounds=10
    )
    model.fit(
        X_train_scaled,
        y_train,
        eval_set=[(X_test_scaled, y_test)],
        verbose=False
    )
    print("Model training complete")

    predictions = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, predictions)
    print(f"\nModel Evaluation Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report")
    print(
        classification_report(y_test, predictions, target_names=['Home (0)', 'Draw (1)', 'Away (2)'], zero_division=0))
    print("\nFeature Importance")

    feature_names = model.get_booster().feature_names
    if feature_names is None: feature_names = features
    importance_scores = model.feature_importances_
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importance_scores})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    print(importance_df.head(20).to_string())

    try:
        if not os.path.exists('results'):
            os.makedirs('results')
        fig, ax = plt.subplots()
        importance_df.sort_values(by='Importance', ascending=True).plot(kind='barh', x='Feature', y='Importance', ax=ax,
                                                                        legend=False)
        ax.set_title('Feature Importance')
        plt.tight_layout()
        save_path = os.path.join(config.RESULTS_DIR, 'feature_importance.png')
        plt.savefig(save_path)
        print(f"\nFeature importance plot saved to {save_path}")
    except Exception as e:
        print(f"Warning: Could not save plot. Error: {e}")