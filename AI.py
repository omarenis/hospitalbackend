import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from backend.settings import BASE_DIR
FILE = pd.read_csv(BASE_DIR / 'dataset1.csv')


X = FILE.iloc[:, :-1]
Y = FILE['diagnostic']
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
classifier = SVC(kernel='rbf', random_state=0)


def train():
    classifier.fit(x_train, y_train)


def evaluate(data_to_predict):
    return classifier.predict(data_to_predict)
