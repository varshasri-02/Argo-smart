"""
AgroSmart - Crop Recommendation Model Evaluation
Author: Varshasri R V
This script evaluates the ML-based crop recommendation model and generates metrics
"""

# Import required libraries
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)


def evaluate_crop_model(y_test, y_pred, model_name="Crop Recommendation Model"):
    """
    Calculate all metrics for crop recommendation model
    
    Parameters:
    -----------
    y_test : array-like
        True labels
    y_pred : array-like
        Predicted labels
    model_name : str
        Name of the model for display
    
    Returns:
    --------
    dict : Dictionary containing all metrics
    """
    print("="*70)
    print(f"AGROSMART - {model_name.upper()} EVALUATION")
    print("="*70)
    
    # 1. Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy * 100:.2f}%")

    # 2. Precision, Recall, F1-Score (weighted for multi-class)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall: {recall * 100:.2f}%")
    print(f"F1-Score: {f1 * 100:.2f}%")
    
    # 3. Detailed Classification Report
    print("\n" + "="*70)
    print("DETAILED CLASSIFICATION REPORT")
    print("="*70)
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # 4. Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)
    
    # Visualize confusion matrix
    plt.figure(figsize=(12, 10))
    
    # Get unique labels
    labels = sorted(y_test.unique())
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels,
                cbar_kws={'label': 'Count'})
    plt.title(f'{model_name} - Confusion Matrix\nAccuracy: {accuracy*100:.2f}%', 
              fontsize=14, fontweight='bold')
    plt.ylabel('Actual Crop', fontsize=12)
    plt.xlabel('Predicted Crop', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    filename = f'agrosmart_confusion_matrix_{model_name.lower().replace(" ", "_")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\nConfusion matrix saved as '{filename}'")
    plt.close()
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm
    }


def cross_validate_model(model, X, y, cv=5):
    """
    Perform k-fold cross-validation
    
    Parameters:
    -----------
    model : estimator object
        The machine learning model to evaluate
    X : array-like
        Feature matrix
    y : array-like
        Target labels
    cv : int
        Number of folds for cross-validation
    
    Returns:
    --------
    array : Cross-validation scores
    """
    print("\n" + "="*70)
    print(f"CROSS-VALIDATION ({cv}-FOLD)")
    print("="*70)
    
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    
    print(f"\nIndividual fold scores: {[f'{score*100:.2f}%' for score in scores]}")
    print(f"\nMean Accuracy: {scores.mean() * 100:.2f}%")
    print(f"Standard Deviation: ±{scores.std() * 100:.2f}%")
    print(f"Min Accuracy: {scores.min() * 100:.2f}%")
    print(f"Max Accuracy: {scores.max() * 100:.2f}%")
    
    return scores


def compare_models(X_train, X_test, y_train, y_test):
    """
    Compare multiple ML models for crop recommendation
    
    Parameters:
    -----------
    X_train, X_test : array-like
        Training and test features
    y_train, y_test : array-like
        Training and test labels
    
    Returns:
    --------
    dict : Comparison results for all models
    """
    print("\n" + "="*70)
    print("MODEL COMPARISON")
    print("="*70)
    
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Naive Bayes': GaussianNB()
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n{'='*70}")
        print(f"Training {name}...")
        print('='*70)
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Evaluate
        metrics = evaluate_crop_model(y_test, y_pred, name)
        
        results[name] = metrics
    
    # Visualize comparison
    plot_model_comparison(results)
    
    return results


def plot_model_comparison(results):
    """
    Create visualization comparing different models
    
    Parameters:
    -----------
    results : dict
        Dictionary containing metrics for each model
    """
    models = list(results.keys())
    metrics_names = ['accuracy', 'precision', 'recall', 'f1_score']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(models))
    width = 0.2
    
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    
    for i, metric in enumerate(metrics_names):
        values = [results[model][metric] * 100 for model in models]
        ax.bar(x + i * width, values, width, label=metric.capitalize(), color=colors[i])
    
    ax.set_xlabel('Models', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax.set_title('AgroSmart - Model Performance Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim([0, 105])
    
    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f', padding=3)
    
    plt.tight_layout()
    plt.savefig('agrosmart_model_comparison.png', dpi=300, bbox_inches='tight')
    print("\nModel comparison chart saved as 'agrosmart_model_comparison.png'")
    plt.close()


def plot_feature_importance(model, feature_names, model_name="Random Forest"):
    """
    Plot feature importance for tree-based models
    
    Parameters:
    -----------
    model : estimator object
        Trained model with feature_importances_ attribute
    feature_names : list
        List of feature names
    model_name : str
        Name of the model
    """
    if hasattr(model, 'feature_importances_'):
        print("\n" + "="*70)
        print("FEATURE IMPORTANCE ANALYSIS")
        print("="*70)
        
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        print("\nFeature Ranking:")
        for i, idx in enumerate(indices):
            print(f"{i+1}. {feature_names[idx]}: {importances[idx]*100:.2f}%")
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(importances)), importances[indices], color='skyblue', edgecolor='navy')
        plt.xlabel('Features', fontsize=12, fontweight='bold')
        plt.ylabel('Importance', fontsize=12, fontweight='bold')
        plt.title(f'{model_name} - Feature Importance', fontsize=14, fontweight='bold')
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('agrosmart_feature_importance.png', dpi=300, bbox_inches='tight')
        print("\nFeature importance chart saved as 'agrosmart_feature_importance.png'")
        plt.close()


def main():
    """
    Main execution function
    """
    print("\n" + "="*70)
    print("AGROSMART - CROP RECOMMENDATION MODEL EVALUATION")
    print("Author: Varshasri R V")
    print("="*70)
    
    try:
        # ===========================
        # 1. LOAD DATASET
        # ===========================
        print("\n[Step 1/5] Loading dataset...")
        
        # Update this path to your actual dataset location
        df = pd.read_csv('Machine Learning/Crop_recommendation.csv')
        
        print(f"Dataset loaded successfully!")
        print(f"  - Total samples: {len(df)}")
        print(f"  - Features: {df.shape[1] - 1}")
        print(f"  - Target crops: {df.iloc[:, -1].nunique()}")
        
        # Display basic info
        print("\nDataset columns:", df.columns.tolist())
        print("\nFirst few rows:")
        print(df.head())
        
        # ===========================
        # 2. PREPARE DATA
        # ===========================
        print("\n[Step 2/5] Preparing data...")
        
        # Update these column names based on your dataset
        feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        target_column = 'label'  # or 'crop' - update based on your dataset
        
        X = df[feature_columns]
        y = df[target_column]
        
        print(f"Features (X): {X.shape}")
        print(f"Target (y): {y.shape}")
        print(f"\nCrop distribution:")
        print(y.value_counts())
        
        # ===========================
        # 3. SPLIT DATA
        # ===========================
        print("\n[Step 3/5] Splitting data (80% train, 20% test)...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training set: {X_train.shape[0]} samples")
        print(f"Test set: {X_test.shape[0]} samples")
        
        # ===========================
        # 4. TRAIN AND EVALUATE MODEL
        # ===========================
        print("\n[Step 4/5] Training Random Forest model...")
        
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        print("Model trained successfully!")
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Evaluate
        metrics = evaluate_crop_model(y_test, y_pred, "Random Forest")
        
        # Cross-validation
        cv_scores = cross_validate_model(model, X, y, cv=5)
        
        # Feature importance
        plot_feature_importance(model, feature_columns, "Random Forest")
        
        # ===========================
        # 5. COMPARE MODELS (OPTIONAL)
        # ===========================
        print("\n[Step 5/5] Comparing multiple models...")
        comparison_results = compare_models(X_train, X_test, y_train, y_test)
        
        # ===========================
        # FINAL SUMMARY
        # ===========================
        print("\n" + "="*70)
        print("FINAL SUMMARY")
        print("="*70)
        print(f"\nBest Model: Random Forest")
        print(f"Test Accuracy: {metrics['accuracy']*100:.2f}%")
        print(f"Cross-Validation Accuracy: {cv_scores.mean()*100:.2f}% (±{cv_scores.std()*100:.2f}%)")
        print(f"Precision: {metrics['precision']*100:.2f}%")
        print(f"Recall: {metrics['recall']*100:.2f}%")
        print(f"F1-Score: {metrics['f1_score']*100:.2f}%")

        print("\n" + "="*70)
        print("EVALUATION COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nGenerated files:")
        print("  1. agrosmart_confusion_matrix_random_forest.png")
        print("  2. agrosmart_feature_importance.png")
        print("  3. agrosmart_model_comparison.png")
        print("\n")
        
    except FileNotFoundError:
        print("\nERROR: Dataset file not found!")
        print("Please update the file path in the script:")
        print("  df = pd.read_csv('YOUR_DATASET_PATH.csv')")
        
    except KeyError as e:
        print(f"\n❌ ERROR: Column not found: {e}")
        print("Please update feature_columns and target_column in the script")
        print("Current columns in dataset:", df.columns.tolist())
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()