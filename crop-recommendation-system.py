import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler

# Wczytanie i podział danych
print("Wczytywanie danych")
df = pd.read_csv('Crop_recommendation.csv')

X = df.drop('label', axis=1)
y = df['label']

# Podział na zbiór treningowy (80%) i testowy (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Preprocessing (Standaryzacja)
print("Trwa standaryzacja danych")
scaler = StandardScaler()

# Skalowanie
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Trenowanie z GridSearch (Random Forest)
print("Uruchamianie GridSearch dla Random Forest")

# Definiowanie parametrów do przetestowania
parametry_rf = {
    'n_estimators': [50, 100, 200], # Ile drzew w lesie
    'max_depth': [None, 10, 20]     # Jak głębokie mogą być drzewa
}

podstawowy_rf = RandomForestClassifier(random_state=42)
# Automat poszukujący najlepszych parametrów (Walidacja krzyżowa cv=5)
grid_search = GridSearchCV(estimator=podstawowy_rf, param_grid=parametry_rf, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Zapisanie wygranego model
najlepszy_model_rf = grid_search.best_estimator_

# Sprawdzanie go na danych testowych
rf_predictions = najlepszy_model_rf.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_predictions)

# Trenownaie k-NN (Model porównawczy)
print("Trenowanie modelu k-NN")
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train_scaled, y_train) # Dane po skalowaniu
knn_predictions = knn_model.predict(X_test_scaled)
knn_accuracy = accuracy_score(y_test, knn_predictions)

# Wyświetlenie wyników
print("\nWYNIKI KOŃCOWE\n")
print(f"Najlepsze parametry dla Lasu Losowego: {grid_search.best_params_}")
print(f"Skuteczność Random Forest (po optymalizacji): {rf_accuracy * 100:.2f}%")
print(f"Skuteczność k-NN (po preprocessingu):         {knn_accuracy * 100:.2f}%")

print("\nSzczegółowy Raport Klasyfikacji (dla Random Forest):")
print(classification_report(y_test, rf_predictions))

# Wizualizacje
print("Generowanie wykresów")

# Wykres ważności cech (Feature Importance)
waznosc = pd.Series(najlepszy_model_rf.feature_importances_, index=X.columns).sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=waznosc.values, y=waznosc.index, hue=waznosc.index, palette='viridis', legend=False)
plt.title('Ważność warunków dla wyboru uprawy (Feature Importance)')
plt.xlabel('Poziom ważności')
plt.ylabel('Cechy (Warunki)')
plt.tight_layout()
plt.show()

# Wykres macierzy błędów (Confusion Matrix)
plt.figure(figsize=(12, 10))
macierz = confusion_matrix(y_test, rf_predictions)

sns.heatmap(macierz, annot=True, fmt='d', cmap='Blues',
            xticklabels=najlepszy_model_rf.classes_,
            yticklabels=najlepszy_model_rf.classes_)
plt.title('Macierz błędów (Confusion Matrix) dla Random Forest')
plt.xlabel('Gatunek przewidziany przez model')
plt.ylabel('Rzeczywisty gatunek rośliny')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Najlepsze parametry dla Lasu Losowego: {'max_depth': None, 'n_estimators': 100}
# Skuteczność Random Forest (po optymalizacji): 99.55%
# Skuteczność k-NN (po preprocessingu):         97.95%
