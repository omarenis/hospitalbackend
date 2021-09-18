import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
file = pd.read_csv('dataset1.csv')  # read dataset
#
# # structuring the dataset into classes using data varaible, each key of data is a dictionary that contains the class
# # each value for class in data is a dictionary that contains the signification of the questions
# data = {
#     'BEHAVIOR_TROUBLE_PARENTS': {
#         'insolent_with_grown_ups': 0,
#         'feels_attacked_defensive': 0,
#         'destructive': 0,
#         'deny_mistakes_blame_others': 0,
#         'quarrelsome_get_involved_fight': 0,
#         'bully_intimidate_comrades': 0,
#         'constantly_fight': 0,
#         'unhappy': 0,
#     },
#     'LEARNING_TROUBLE_PARENTS': {
#         'has_learning_difficulties': 0,
#         'trouble_finishing_things': 0,
#         'easily_being_distracted': 0,
#         'enability_finish_when_do_effort': 0,
#     },
#     'SOMATISATION_TORUBLE_PARENTS': {
#         'headaches': 0,
#         'upset_stomach': 0,
#         'physical_aches': 0,
#         'vomiting_nausea': 0
#     },
#     'IMPULSIVITY_TROUBLE_PARENTS': {
#         'excitable_impulsive': 0,
#         'want_dominate': 0,
#         'squirms': 0,
#         'restless_needs_do_something': 0
#     },
#     'ANXITY_TROUBLE_PARENTS': {
#         'afraid_new_things': 0,
#         'shy': 0,
#         'worry_much': 0,
#         'being_crashed_manipulated': 0
#     },
#     'HYPERACTIVITY_TROUBLE_PARENTS': {
#         'excitable_impulsive': 0,
#         'cry_often_easily': 0,
#         'squirms': 0,
#         'restless_needs_do_something': 0,
#         'destructive': 0,
#         'trouble_finishing_things': 0,
#         'easily_being_distracted': 0,
#         'moody': 0,
#         'enability_finish_when_do_effort': 0,
#         'disturb_other_children': 0
#     }
# }
# scores = []
# for patient in range(47):
#     diagnostic = 0
#     for i in data:
#         score = 0
#         print(f"patient {patient + 1}")
#         for j in data[i]:
#             score += file[j][patient]
#         if score / len(list(data[i].keys())) >= 2:
#             diagnostic = 1
#             score = 0
#             break
#     scores.append(diagnostic)
#
# file.insert(27, 'diagnostic', scores, True)
# file.to_csv('dataset1.csv')


X = file.iloc[:, :-1]
Y = file['diagnostic']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
classifier = SVC(kernel='rbf', random_state=0)
classifier.fit(X_train, Y_train)
Y_pred = classifier.predict(X_test)
cm = confusion_matrix(Y_test, Y_pred)
