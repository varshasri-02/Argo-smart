"""
AgroSmart - Crop Recommendation Model Training Script
Trains and saves the ML model for production use.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style for plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

def load_and_preprocess_data(filepath='Machine Learning/Crop_recommendation.csv'):
    """Load and preprocess the dataset."""
    print("Loading dataset...")
    df = pd.read_csv(filepath)

    # Features and target
    feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    target_column = 'label'

    X = df[feature_columns]
    y = df[target_column]

    print(f"Dataset shape: {X.shape}")
    print(f"Number of crops: {y.nunique()}")
    print(f"Crop distribution:\n{y.value_counts()}")

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, feature_columns, scaler

def train_and_compare_models(X_train, X_test, y_train, y_test):
    """Train and compare different models."""
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(kernel='rbf', random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
    }

    results = {}

    print("\n" + "="*60)
    print("MODEL TRAINING AND COMPARISON")
    print("="*60)

    for name, model in models.items():
        print(f"\nTraining {name}...")

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        print(".2f")

        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        print(".2f")

        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }

    return results

def plot_model_comparison(results):
    """Plot model comparison."""
    models = list(results.keys())
    accuracies = [results[m]['accuracy'] for m in models]
    cv_means = [results[m]['cv_mean'] for m in models]

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, accuracies, width, label='Test Accuracy', alpha=0.8)
    ax.bar(x + width/2, cv_means, width, label='CV Mean Accuracy', alpha=0.8)

    ax.set_xlabel('Models')
    ax.set_ylabel('Accuracy')
    ax.set_title('Model Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    # Add value labels
    for i, v in enumerate(accuracies):
        ax.text(i - width/2, v + 0.01, '.3f', ha='center')
    for i, v in enumerate(cv_means):
        ax.text(i + width/2, v + 0.01, '.3f', ha='center')

    plt.tight_layout()
    plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Model comparison plot saved as 'model_comparison.png'")

def plot_feature_importance(model, feature_names):
    """Plot feature importance for Random Forest."""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]

        print("\n" + "="*60)
        print("FEATURE IMPORTANCE ANALYSIS")
        print("="*60)

        for i, idx in enumerate(indices):
            print("2d")

        plt.figure(figsize=(10, 6))
        plt.bar(range(len(importances)), importances[indices], color='skyblue', edgecolor='navy')
        plt.xlabel('Features')
        plt.ylabel('Importance')
        plt.title('Random Forest - Feature Importance')
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Feature importance plot saved as 'feature_importance.png'")

def save_model_and_scaler(model, scaler, model_path='crop_model.joblib', scaler_path='scaler.joblib'):
    """Save the trained model and scaler."""
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"\nModel saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")

def main():
    """Main training function."""
    print("="*60)
    print("AGROSMART - CROP RECOMMENDATION MODEL TRAINING")
    print("="*60)

    # Load and preprocess data
    X, y, feature_names, scaler = load_and_preprocess_data()

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")

    # Train and compare models
    results = train_and_compare_models(X_train, X_test, y_train, y_test)

    # Plot comparison
    plot_model_comparison(results)

    # Select best model (Random Forest as specified)
    best_model_name = 'Random Forest'
    best_model = results[best_model_name]['model']

    print(f"\nSelected model: {best_model_name}")
    print(".2f")
    print(".2f")

    # Feature importance
    plot_feature_importance(best_model, feature_names)

    # Save model and scaler
    save_model_and_scaler(best_model, scaler)

    print("\n" + "="*60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nGenerated files:")
    print("  - crop_model.joblib")
    print("  - scaler.joblib")
    print("  - model_comparison.png")
    print("  - feature_importance.png")

if __name__ == "__main__":
    main()