import numpy as np
from sklearn import svm, datasets
from sklearn.cross_validation import train_test_split
from sklearn.multiclass import OneVsRestClassifier

from sklearn_evaluation import ClassifierEvaluator

# Import some data to play with
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Add noisy features to make the problem harder
random_state = np.random.RandomState(0)
n_samples, n_features = X.shape
X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]

# shuffle and split training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5,
                                                    random_state=0)

# Learn to predict each class against the other
classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True,
                                 random_state=random_state))
classifier = classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
y_score = classifier.decision_function(X_test)

feature_list = range(4)
target_names = ['setosa', 'versicolor', 'virginica']

# Create a trained model instance
ce = ClassifierEvaluator(classifier, y_test, y_pred, y_score,
                         feature_list, target_names,
                         estimator_name='super awesome SVC')

template = '''
           # Report
           {estimator_type}
           {date}
           {confusion_matrix}
           {roc}
           {precision_recall}
           '''

ce.generate_report(template, 'report.html')
