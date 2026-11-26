import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(42)
sample_count = 2000
amount = rng.uniform(100, 10000, sample_count)
volatility = rng.uniform(0, 1, sample_count)
frequency = rng.integers(1, 50, sample_count)
features = np.column_stack([amount, volatility, frequency])

# Label an order as high risk when at least two conditions hold.
score = (
    (amount > 7000).astype(int)
    + (volatility > 0.65).astype(int)
    + (frequency > 35).astype(int)
)
labels = (score >= 2).astype(int)
x_train, x_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.25, random_state=42, stratify=labels
)
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=8,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
)
model.fit(x_train, y_train)
accuracy = float(accuracy_score(y_test, model.predict(x_test)))

joblib.dump(model, ARTIFACTS / "risk_model.joblib")
metrics = {
    "dataset": "synthetic",
    "accuracy": accuracy,
    "training_samples": len(x_train),
    "testing_samples": len(x_test),
    "model": "RandomForestClassifier",
    "random_state": 42,
}
(ARTIFACTS / "metrics.json").write_text(
    json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
)

print(f"Training samples: {len(x_train)}")
print(f"Testing samples: {len(x_test)}")
print(f"Model accuracy: {accuracy:.2%}")
print(f"Model saved to: {ARTIFACTS}")
