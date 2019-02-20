def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from timeit import default_timer as timer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, roc_auc_score
from imblearn import metrics
from collections import OrderedDict
from py_learning_benchmarks import DataLoader



def train_and_predict(classifier, X_train, y_train, X_test, y_test):
    start = timer()
    classifier.fit(X_train, y_train)
    end = timer()
    predictions = classifier.predict(X_test)
    results = OrderedDict()
    results['recall'] = metrics.sensitivity_score(y_test, predictions, pos_label=1, average='binary')
    results['gmean'] = metrics.geometric_mean_score(y_test, predictions, pos_label=1, average='binary')
    results['fmeasure'] = f1_score(y_test, predictions, average=None)[1]
    results['auc'] = roc_auc_score(y_test, predictions, average=None)
    results['time'] = end-start
    return results



data = DataLoader()
query = data(filters=[('dataset_provider', '=', 'keel'), ('IR', '>=', 10), ('name', 'not contains', 'kr'), ('name', 'not contains', 'kdd'), ('name', 'not contains', 'shuttle')],
             sort_by="Instances")
random_state = 1

header = ["Dataset", "IR", "Algorithm","Recall", 'G-Mean', "F-Measure", "AUC", "Time"]
print()

algorithms = [(DecisionTreeClassifier(random_state=random_state, criterion="gini"), "Decision Tree"),
                  (RandomForestClassifier(random_state=random_state), "Random Forest")
                ]
params = None

run_meta_data = []
runs = []
benchmark_count = 0


for metadata, folds in query:
    folds = list(folds) #turn generator into list to allow multiple algorithm runs
    print(benchmark_count, end=', ', flush=True)
    benchmark_count+=1
    run_meta_data += [metadata]


    dataset_run = OrderedDict()
    dataset_run['dataset'] = metadata['name']
    dataset_run['IR'] = metadata['IR']
    dataset_run['results'] = {}
    for classifier, classifier_name in algorithms:
        # try:
        fold_metrics = [] #array of tuples containing metrics on each fold
        for train, test in folds:
            X_train, y_train = train
            X_test, y_test = test
            fold_metrics += [train_and_predict(classifier, X_train.values, y_train.values, X_test.values, y_test.values)]


        averaged_folds = OrderedDict()
        for metric in fold_metrics[0].keys():

            averaged_folds[metric] = 0
            for fold in fold_metrics:
                averaged_folds[metric] += fold[metric]
            averaged_folds[metric] /= len(fold_metrics)

        dataset_run['results'][classifier_name] = averaged_folds

    runs += [dataset_run]
    all_metrics = sorted(list(runs[0]['results']['Decision Tree']))

for metric in all_metrics:
    print(metric+ ",IR," + ",".join(sorted(list(runs[0]['results']))))
    for run in runs:
        print(run['dataset']+","+str(run['IR'])+","+",".join( ["{:0.4f}".format(run['results'][classifier][metric]) for classifier in sorted(list(run['results'])) ] ))
    print()

print("Dataset, Instances, Features") 
for meta_data in run_meta_data:
    print(meta_data['name']+", "+ str(int(meta_data['Instances'])) +", "+ str(int(meta_data['Features'])))
