import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class ActivityPredictionService:
    """
    Service for predicting user activity
    """

    def train_model(self, user_activities):
        X = [[activity.visits, activity.actions, activity.session_duration] for activity in user_activities]
        y = [activity.next_month_activity for activity in user_activities]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}")
        return model

    def predict_activity_probability(self, model, user_data):
        X_user = np.array([user_data['visits'], user_data['actions'], user_data['session_duration']]).reshape(1, -1)
        probability = model.predict_proba(X_user)[:, 1][0]
        return probability
