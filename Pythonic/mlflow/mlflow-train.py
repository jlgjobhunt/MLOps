import mlflow

import mlflow.sklearn

import mlflow.pytorch

from sklearn.linear_model import LinearRegression

from sklearn.model_selection import train_test_split

from sklearn.datasets import make_regression


X, y = make_regression(n_samples=100, n_features=2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

with mlflow.start_run():
    mlflow.log_param("n_samples", 100)
    mlflow.log_param("n_features", 2)

    model = LinearRegression()
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(model, "my_model")

print("Run complete. Run 'mlflow ui' to view the results.")

    