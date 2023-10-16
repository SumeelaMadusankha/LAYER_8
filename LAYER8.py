{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "executionInfo": {
     "elapsed": 2507,
     "status": "ok",
     "timestamp": 1692881109152,
     "user": {
      "displayName": "sumeela madusanka",
      "userId": "12151675989731501762"
     },
     "user_tz": -330
    },
    "id": "m9y1uoML8iPU",
    "ExecuteTime": {
     "end_time": "2023-10-13T05:42:31.478232300Z",
     "start_time": "2023-10-13T05:42:27.371126500Z"
    }
   },
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from sklearn.model_selection import train_test_split,cross_val_score\n",
    "from sklearn.svm import SVC\n",
    "from sklearn.neighbors import KNeighborsClassifier as KNN\n",
    "from sklearn.preprocessing import RobustScaler\n",
    "from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score\n",
    "from sklearn.decomposition import PCA\n",
    "#grid search\n",
    "from sklearn.model_selection import GridSearchCV\n",
    "from sklearn.metrics import f1_score\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "executionInfo": {
     "elapsed": 2244,
     "status": "ok",
     "timestamp": 1692891076822,
     "user": {
      "displayName": "sumeela madusanka",
      "userId": "12151675989731501762"
     },
     "user_tz": -330
    },
    "id": "2yYIos7TAsHt",
    "ExecuteTime": {
     "end_time": "2023-10-13T05:42:51.942901200Z",
     "start_time": "2023-10-13T05:42:47.712200300Z"
    }
   },
   "outputs": [],
   "source": [
    "# Load the data\n",
    "train_data = pd.read_csv('train.csv')\n",
    "valid_data = pd.read_csv('valid.csv')\n",
    "test_data = pd.read_csv('test.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "outputs": [],
   "source": [
    "# Split data into features (X) and target labels (y)\n",
    "X_train = train_data.drop(['label_1', 'label_2', 'label_3', 'label_4'], axis=1)\n",
    "y_label_1_train = train_data['label_1']\n",
    "y_label_2_train = train_data['label_2']\n",
    "y_label_3_train = train_data['label_3']\n",
    "y_label_4_train = train_data['label_4']\n",
    "\n",
    "X_valid = valid_data.drop(['label_1', 'label_2', 'label_3', 'label_4'], axis=1)\n",
    "y_valid_label1 = valid_data['label_1']\n",
    "y_valid_label2 = valid_data['label_2']\n",
    "y_valid_label3 = valid_data['label_3']\n",
    "y_valid_label4 = valid_data['label_4']\n",
    "\n",
    "X_test = test_data.drop(['ID'], axis=1)\n",
    "\n",
    "output = pd.DataFrame(index=range(744))\n",
    "output['ID'] = test_data['ID']\n",
    "\n",
    "validate = pd.DataFrame()\n",
    "\n",
    "\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-10-13T06:55:42.030011Z",
     "start_time": "2023-10-13T06:55:41.941245900Z"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "label_4\n",
      "6     19938\n",
      "2      1449\n",
      "0       955\n",
      "12      954\n",
      "7       938\n",
      "13      482\n",
      "1       481\n",
      "11      480\n",
      "10      480\n",
      "3       479\n",
      "5       478\n",
      "9       472\n",
      "4       469\n",
      "8       465\n",
      "Name: count, dtype: int64\n"
     ]
    }
   ],
   "source": [
    "# count individual unique count of each label category\n",
    "class_distribution =train_data['label_4'].value_counts()\n",
    "print(class_distribution)"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-10-13T06:51:01.693314900Z",
     "start_time": "2023-10-13T06:51:01.677357100Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "# Apply feature engineering techniques"
   ],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "outputs": [],
   "source": [
    "sc = RobustScaler()\n",
    "\n",
    "X_train_scaled = sc.fit_transform(X_train)\n",
    "X_valid_scaled = sc.transform(X_valid)\n",
    "X_test_scaled = sc.transform(X_test)\n",
    "\n",
    "# Calculate the variance threshold\n",
    "desired_variance = 0.97  # Set the desired explained variance\n",
    "pca = PCA(n_components=desired_variance, svd_solver='full')\n",
    "X_train_pca = pca.fit_transform(X_train_scaled)\n",
    "X_valid_pca =pca.transform(X_valid_scaled)\n",
    "X_test_pca = pca.transform(X_test_scaled)\n",
    "\n",
    "# Get the number of components selected based on the variance threshold\n",
    "n_components = pca.n_components_"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-10-13T06:51:08.099689100Z",
     "start_time": "2023-10-13T06:51:03.899724800Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "aFzAUW_SN8Ki",
    "ExecuteTime": {
     "end_time": "2023-09-22T05:53:30.847155200Z",
     "start_time": "2023-09-22T05:53:30.824944700Z"
    }
   },
   "source": [
    "# Cross validation for label 1"
   ],
   "outputs": [],
   "execution_count": 42
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 48675,
     "status": "ok",
     "timestamp": 1692891603793,
     "user": {
      "displayName": "sumeela madusanka",
      "userId": "12151675989731501762"
     },
     "user_tz": -330
    },
    "id": "ypSIK93vCjU6",
    "outputId": "9ea70f0e-6932-4a0d-ceee-0b47c3721bde",
    "ExecuteTime": {
     "end_time": "2023-09-23T11:06:18.441568400Z",
     "start_time": "2023-09-23T11:01:30.170015600Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Cross-validation accuracy for svc label_1: 0.92\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\joblib\\externals\\loky\\backend\\context.py:136: UserWarning: Could not find the number of physical cores for the following reason:\n",
      "[WinError 2] The system cannot find the file specified\n",
      "Returning the number of logical cores instead. You can silence this warning by setting LOKY_MAX_CPU_COUNT to the number of cores you want to use.\n",
      "  warnings.warn(\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\joblib\\externals\\loky\\backend\\context.py\", line 257, in _count_physical_cores\n",
      "    cpu_info = subprocess.run(\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\subprocess.py\", line 501, in run\n",
      "    with Popen(*popenargs, **kwargs) as process:\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\subprocess.py\", line 947, in __init__\n",
      "    self._execute_child(args, executable, preexec_fn, close_fds,\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\subprocess.py\", line 1416, in _execute_child\n",
      "    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Cross-validation accuracy for knn_label_1: 0.83\n"
     ]
    }
   ],
   "source": [
    "cv_score = cross_val_score(SVC(random_state=42, kernel='linear', gamma='auto'), X_train_pca, y_label_1_train, cv=5)\n",
    "\n",
    "print(f\"Cross-validation accuracy for svc label_1: {np.mean(cv_score):.2f}\")\n",
    "\n",
    "cv_score = cross_val_score(KNN(n_neighbors=5), X_train_pca, y_label_1_train, cv=5)\n",
    "\n",
    "print(f\"Cross-validation accuracy for knn_label_1: {np.mean(cv_score):.2f}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "# Grid search for label 1"
   ],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "750\n",
      "Validate accuracy: 0.924\n",
      "Validate precision: 0.924\n",
      "Validate recall: 0.924\n",
      "Validate f1: 0.924\n"
     ]
    }
   ],
   "source": [
    "#grid searchcv\n",
    "param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100],\n",
    "              'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],\n",
    "              'gamma': ['auto', 'scale']}\n",
    "kernal = ['linear', 'poly', 'rbf', 'sigmoid']\n",
    "gamma = ['auto', 'scale']\n",
    "\n",
    "gs_ = GridSearchCV(estimator=SVC(), param_grid=param_grid, scoring='accuracy', cv=5, n_jobs=-1)\n",
    "gs = SVC(C=0.1, gamma='auto', kernel='linear')\n",
    "gs = gs.fit(X_train_pca, y_label_1_train)\n",
    "\n",
    "\n",
    "#evaluate train model\n",
    "pred_label_1 = gs.predict(X_valid_pca)\n",
    "print(len(pred_label_1))\n",
    "#save on to csv file\n",
    "validate['LABEL1']=pred_label_1\n",
    "\n",
    "\n",
    "#save on to csv file\n",
    "validate.to_csv('validate.csv', index=False)\n",
    "\n",
    "\n",
    "print('Validate accuracy: %.3f' % accuracy_score(y_true=y_valid_label1, y_pred=pred_label_1))\n",
    "print('Validate precision: %.3f' % precision_score(y_true=y_valid_label1, y_pred=pred_label_1, average='micro'))\n",
    "print('Validate recall: %.3f' % recall_score(y_true=y_valid_label1, y_pred=pred_label_1,    average='micro'))\n",
    "print('Validate f1: %.3f' % f1_score(y_true=y_valid_label1, y_pred=pred_label_1,    average='micro'))"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-10-13T07:05:45.854935600Z",
     "start_time": "2023-10-13T07:05:21.851779900Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "# Cross validation for label 2\n"
   ],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(28040, 401)\n",
      "(28040,)\n"
     ]
    }
   ],
   "source": [
    "train_data_label_2 = train_data[train_data['label_2'].notna()]\n",
    "X_train_label_2 = train_data_label_2.drop(['label_1', 'label_2', 'label_3', 'label_4'], axis=1)\n",
    "y_label2_train = train_data_label_2['label_2']\n",
    "\n",
    "X_train_label2_scaled = sc.fit_transform(X_train_label_2)\n",
    "\n",
    "valid_data_label_2 = valid_data[valid_data['label_2'].notna()]\n",
    "X_valid_label_2 = valid_data_label_2.drop(['label_1', 'label_2', 'label_3', 'label_4'], axis=1)\n",
    "y_valid_label_2 = valid_data_label_2['label_2']\n",
    "\n",
    "X_test_label_2 = test_data.drop(['ID'], axis=1)\n",
    "\n",
    "X_valid_label2_scaled = sc.transform(X_valid_label_2)\n",
    "X_test_label_2_scaled = sc.transform(X_test_label_2)\n",
    "\n",
    "\n",
    "# Calculate the variance threshold\n",
    "desired_variance = 0.97  # Set the desired explained variance\n",
    "pca_label2 = PCA(n_components=desired_variance, svd_solver='full')\n",
    "X_train_label2_pca = pca_label2.fit_transform(X_train_label2_scaled)\n",
    "X_valid_label2_pca =pca_label2.transform(X_valid_label2_scaled)\n",
    "X_test_label2_pca = pca_label2.transform(X_test_label_2_scaled)\n",
    "\n",
    "\n",
    "# Get the number of components selected based on the variance threshold\n",
    "n_components_label2 = pca.n_components_\n",
    "\n",
    "print(X_train_label2_pca.shape)\n",
    "print(y_label2_train.shape)"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-10-13T07:09:19.693428900Z",
     "start_time": "2023-10-13T07:09:15.635288300Z"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\joblib\\externals\\loky\\backend\\context.py:136: UserWarning: Could not find the number of physical cores for the following reason:\n",
      "[WinError 2] The system cannot find the file specified\n",
      "Returning the number of logical cores instead. You can silence this warning by setting LOKY_MAX_CPU_COUNT to the number of cores you want to use.\n",
      "  warnings.warn(\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\joblib\\externals\\loky\\backend\\context.py\", line 257, in _count_physical_cores\n",
      "    cpu_info = subprocess.run(\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\subprocess.py\", line 501, in run\n",
      "    with Popen(*popenargs, **kwargs) as process:\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\subprocess.py\", line 947, in __init__\n",
      "    self._execute_child(args, executable, preexec_fn, close_fds,\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\subprocess.py\", line 1416, in _execute_child\n",
      "    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Cross-validation accuracy for knn_label_2: 0.52\n",
      "Cross-validation accuracy for svc_label_2: 0.48\n"
     ]
    }
   ],
   "source": [
    "cv_score = cross_val_score(KNN(n_neighbors=5), X_train_label2_pca, y_label2_train, cv=5)\n",
    "print(f\"Cross-validation accuracy for knn_label_2: {np.mean(cv_score):.2f}\")\n",
    "\n",
    "cv_score = cross_val_score(SVC(random_state=42, kernel='linear', gamma='auto'), X_train_label2_pca, y_label2_train, cv=5)\n",
    "print(f\"Cross-validation accuracy for svc_label_2: {np.mean(cv_score):.2f}\")\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-09-23T07:17:38.105067700Z",
     "start_time": "2023-09-23T07:08:27.651029100Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "# Grid search for label 2"
   ],
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Cross-validation accuracy for svc_label_2: 0.47\n"
     ]
    }
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Validate accuracy: 0.861\n",
      "Validate precision: 0.861\n",
      "Validate recall: 0.861\n",
      "Validate f1: 0.861\n"
     ]
    }
   ],
   "source": [
    "#grid searchcv for knn\n",
    "param_grid = {\n",
    "    'n_neighbors': np.arange(1, 25),\n",
    "     'weights': ['uniform', 'distance'],\n",
    "    'p': [1, 2]  # Corresponds to Manhattan and Euclidean distances\n",
    "              }\n",
    "# gs_label_2_ = GridSearchCV(estimator=KNN(), param_grid=param_grid, scoring='accuracy', cv=5, n_jobs=-1)\n",
    "gs_label_2 = KNN(n_neighbors=5, weights='uniform', p=1)\n",
    "gs_label_2 = gs_label_2.fit(X_train_label2_pca, y_label2_train)\n",
    "\n",
    "\n",
    "#evaluate train model\n",
    "pred_label_2 = gs_label_2.predict(X_valid_label2_pca)\n",
    "validate1 = pd.DataFrame()\n",
    "validate1['LABEL2']=pred_label_2\n",
    "validate1.to_csv('validate1.csv', index=False)\n",
    "print('Validate accuracy: %.3f' % accuracy_score(y_true=y_valid_label_2, y_pred=pred_label_2))\n",
    "print('Validate precision: %.3f' % precision_score(y_true=y_valid_label_2, y_pred=pred_label_2, average='micro'))\n",
    "print('Validate recall: %.3f' % recall_score(y_true=y_valid_label_2, y_pred=pred_label_2,    average='micro'))\n",
    "print('Validate f1: %.3f' % f1_score(y_true=y_valid_label_2, y_pred=pred_label_2,    average='micro'))"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-10-13T07:12:46.487891400Z",
     "start_time": "2023-10-13T07:12:43.198326200Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "outputs": [
    {
     "ename": "KeyboardInterrupt",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "\u001B[1;31m---------------------------------------------------------------------------\u001B[0m",
      "\u001B[1;31mKeyboardInterrupt\u001B[0m                         Traceback (most recent call last)",
      "Cell \u001B[1;32mIn[11], line 4\u001B[0m\n\u001B[0;32m      2\u001B[0m param_grid \u001B[38;5;241m=\u001B[39m {\u001B[38;5;124m'\u001B[39m\u001B[38;5;124mC\u001B[39m\u001B[38;5;124m'\u001B[39m: [\u001B[38;5;241m0.001\u001B[39m, \u001B[38;5;241m0.01\u001B[39m, \u001B[38;5;241m0.1\u001B[39m, \u001B[38;5;241m1\u001B[39m, \u001B[38;5;241m10\u001B[39m, \u001B[38;5;241m100\u001B[39m]}\n\u001B[0;32m      3\u001B[0m gs_label_2_svc \u001B[38;5;241m=\u001B[39m GridSearchCV(estimator\u001B[38;5;241m=\u001B[39mSVC(random_state\u001B[38;5;241m=\u001B[39m\u001B[38;5;241m42\u001B[39m, kernel\u001B[38;5;241m=\u001B[39m\u001B[38;5;124m'\u001B[39m\u001B[38;5;124mlinear\u001B[39m\u001B[38;5;124m'\u001B[39m, gamma\u001B[38;5;241m=\u001B[39m\u001B[38;5;124m'\u001B[39m\u001B[38;5;124mauto\u001B[39m\u001B[38;5;124m'\u001B[39m), param_grid\u001B[38;5;241m=\u001B[39mparam_grid, scoring\u001B[38;5;241m=\u001B[39m\u001B[38;5;124m'\u001B[39m\u001B[38;5;124maccuracy\u001B[39m\u001B[38;5;124m'\u001B[39m, cv\u001B[38;5;241m=\u001B[39m\u001B[38;5;241m5\u001B[39m, n_jobs\u001B[38;5;241m=\u001B[39m\u001B[38;5;241m-\u001B[39m\u001B[38;5;241m1\u001B[39m)\n\u001B[1;32m----> 4\u001B[0m gs_label_2_svc \u001B[38;5;241m=\u001B[39m \u001B[43mgs_label_2_svc\u001B[49m\u001B[38;5;241;43m.\u001B[39;49m\u001B[43mfit\u001B[49m\u001B[43m(\u001B[49m\u001B[43mX_train_label2_pca\u001B[49m\u001B[43m,\u001B[49m\u001B[43m \u001B[49m\u001B[43my_label2_train\u001B[49m\u001B[43m)\u001B[49m\n\u001B[0;32m      5\u001B[0m \u001B[38;5;28mprint\u001B[39m(gs_label_2_svc\u001B[38;5;241m.\u001B[39mbest_score_)\n\u001B[0;32m      6\u001B[0m \u001B[38;5;28mprint\u001B[39m(gs_label_2_svc\u001B[38;5;241m.\u001B[39mbest_params_)\n",
      "File \u001B[1;32mc:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\sklearn\\base.py:1151\u001B[0m, in \u001B[0;36m_fit_context.<locals>.decorator.<locals>.wrapper\u001B[1;34m(estimator, *args, **kwargs)\u001B[0m\n\u001B[0;32m   1144\u001B[0m     estimator\u001B[38;5;241m.\u001B[39m_validate_params()\n\u001B[0;32m   1146\u001B[0m \u001B[38;5;28;01mwith\u001B[39;00m config_context(\n\u001B[0;32m   1147\u001B[0m     skip_parameter_validation\u001B[38;5;241m=\u001B[39m(\n\u001B[0;32m   1148\u001B[0m         prefer_skip_nested_validation \u001B[38;5;129;01mor\u001B[39;00m global_skip_validation\n\u001B[0;32m   1149\u001B[0m     )\n\u001B[0;32m   1150\u001B[0m ):\n\u001B[1;32m-> 1151\u001B[0m     \u001B[38;5;28;01mreturn\u001B[39;00m fit_method(estimator, \u001B[38;5;241m*\u001B[39margs, \u001B[38;5;241m*\u001B[39m\u001B[38;5;241m*\u001B[39mkwargs)\n",
      "File \u001B[1;32mc:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\sklearn\\model_selection\\_search.py:898\u001B[0m, in \u001B[0;36mBaseSearchCV.fit\u001B[1;34m(self, X, y, groups, **fit_params)\u001B[0m\n\u001B[0;32m    892\u001B[0m     results \u001B[38;5;241m=\u001B[39m \u001B[38;5;28mself\u001B[39m\u001B[38;5;241m.\u001B[39m_format_results(\n\u001B[0;32m    893\u001B[0m         all_candidate_params, n_splits, all_out, all_more_results\n\u001B[0;32m    894\u001B[0m     )\n\u001B[0;32m    896\u001B[0m     \u001B[38;5;28;01mreturn\u001B[39;00m results\n\u001B[1;32m--> 898\u001B[0m \u001B[38;5;28;43mself\u001B[39;49m\u001B[38;5;241;43m.\u001B[39;49m\u001B[43m_run_search\u001B[49m\u001B[43m(\u001B[49m\u001B[43mevaluate_candidates\u001B[49m\u001B[43m)\u001B[49m\n\u001B[0;32m    900\u001B[0m \u001B[38;5;66;03m# multimetric is determined here because in the case of a callable\u001B[39;00m\n\u001B[0;32m    901\u001B[0m \u001B[38;5;66;03m# self.scoring the return type is only known after calling\u001B[39;00m\n\u001B[0;32m    902\u001B[0m first_test_score \u001B[38;5;241m=\u001B[39m all_out[\u001B[38;5;241m0\u001B[39m][\u001B[38;5;124m\"\u001B[39m\u001B[38;5;124mtest_scores\u001B[39m\u001B[38;5;124m\"\u001B[39m]\n",
      "File \u001B[1;32mc:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\sklearn\\model_selection\\_search.py:1419\u001B[0m, in \u001B[0;36mGridSearchCV._run_search\u001B[1;34m(self, evaluate_candidates)\u001B[0m\n\u001B[0;32m   1417\u001B[0m \u001B[38;5;28;01mdef\u001B[39;00m \u001B[38;5;21m_run_search\u001B[39m(\u001B[38;5;28mself\u001B[39m, evaluate_candidates):\n\u001B[0;32m   1418\u001B[0m \u001B[38;5;250m    \u001B[39m\u001B[38;5;124;03m\"\"\"Search all candidates in param_grid\"\"\"\u001B[39;00m\n\u001B[1;32m-> 1419\u001B[0m     \u001B[43mevaluate_candidates\u001B[49m\u001B[43m(\u001B[49m\u001B[43mParameterGrid\u001B[49m\u001B[43m(\u001B[49m\u001B[38;5;28;43mself\u001B[39;49m\u001B[38;5;241;43m.\u001B[39;49m\u001B[43mparam_grid\u001B[49m\u001B[43m)\u001B[49m\u001B[43m)\u001B[49m\n",
      "File \u001B[1;32mc:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\sklearn\\model_selection\\_search.py:845\u001B[0m, in \u001B[0;36mBaseSearchCV.fit.<locals>.evaluate_candidates\u001B[1;34m(candidate_params, cv, more_results)\u001B[0m\n\u001B[0;32m    837\u001B[0m \u001B[38;5;28;01mif\u001B[39;00m \u001B[38;5;28mself\u001B[39m\u001B[38;5;241m.\u001B[39mverbose \u001B[38;5;241m>\u001B[39m \u001B[38;5;241m0\u001B[39m:\n\u001B[0;32m    838\u001B[0m     \u001B[38;5;28mprint\u001B[39m(\n\u001B[0;32m    839\u001B[0m         \u001B[38;5;124m\"\u001B[39m\u001B[38;5;124mFitting \u001B[39m\u001B[38;5;132;01m{0}\u001B[39;00m\u001B[38;5;124m folds for each of \u001B[39m\u001B[38;5;132;01m{1}\u001B[39;00m\u001B[38;5;124m candidates,\u001B[39m\u001B[38;5;124m\"\u001B[39m\n\u001B[0;32m    840\u001B[0m         \u001B[38;5;124m\"\u001B[39m\u001B[38;5;124m totalling \u001B[39m\u001B[38;5;132;01m{2}\u001B[39;00m\u001B[38;5;124m fits\u001B[39m\u001B[38;5;124m\"\u001B[39m\u001B[38;5;241m.\u001B[39mformat(\n\u001B[0;32m    841\u001B[0m             n_splits, n_candidates, n_candidates \u001B[38;5;241m*\u001B[39m n_splits\n\u001B[0;32m    842\u001B[0m         )\n\u001B[0;32m    843\u001B[0m     )\n\u001B[1;32m--> 845\u001B[0m out \u001B[38;5;241m=\u001B[39m \u001B[43mparallel\u001B[49m\u001B[43m(\u001B[49m\n\u001B[0;32m    846\u001B[0m \u001B[43m    \u001B[49m\u001B[43mdelayed\u001B[49m\u001B[43m(\u001B[49m\u001B[43m_fit_and_score\u001B[49m\u001B[43m)\u001B[49m\u001B[43m(\u001B[49m\n\u001B[0;32m    847\u001B[0m \u001B[43m        \u001B[49m\u001B[43mclone\u001B[49m\u001B[43m(\u001B[49m\u001B[43mbase_estimator\u001B[49m\u001B[43m)\u001B[49m\u001B[43m,\u001B[49m\n\u001B[0;32m    848\u001B[0m \u001B[43m        \u001B[49m\u001B[43mX\u001B[49m\u001B[43m,\u001B[49m\n\u001B[0;32m    849\u001B[0m \u001B[43m        \u001B[49m\u001B[43my\u001B[49m\u001B[43m,\u001B[49m\n\u001B[0;32m    850\u001B[0m \u001B[43m        \u001B[49m\u001B[43mtrain\u001B[49m\u001B[38;5;241;43m=\u001B[39;49m\u001B[43mtrain\u001B[49m\u001B[43m,\u001B[49m\n\u001B[0;32m    851\u001B[0m \u001B[43m        \u001B[49m\u001B[43mtest\u001B[49m\u001B[38;5;241;43m=\u001B[39;49m\u001B[43mtest\u001B[49m\u001B[43m,\u001B[49m\n\u001B[0;32m    852\u001B[0m \u001B[43m        \u001B[49m\u001B[43mparameters\u001B[49m\u001B[38;5;241;43m=\u001B[39;49m\u001B[43mparameters\u001B[49m\u001B[43m,\u001B[49m\n\u001B[0;32m    853\u001B[0m \u001B[43m        \u001B[49m\u001B[43msplit_progress\u001B[49m\u001B[38;5;241;43m=\u001B[39;49m\u001B[43m(\u001B[49m\u001B[43msplit_idx\u001B[49m\u001B[43m,\u001B[49m\u001B[43m \u001B[49m\u001B[43mn_splits\u001B[49m\u001B[43m)\u001B[49m\u001B[43m,\u001B[49m\n\u001B[0;32m    854\u001B[0m \u001B[43m        \u001B[49m\u001B[43mcandidate_progress\u001B[49m\u001B[38;5;241;43m=\u001B[39;49m\u001B[43m(\u001B[49m\u001B[43mcand_idx\u001B[49m\u001B[43m,\u001B[49m\u001B[43m \u001B[49m\u001B[43mn_candidates\u001B[49m\u001B[43m)\u001B[49m\u001B[43m,\u001B[49m\n\u001B[0;32m    855\u001B[0m \u001B[43m        \u001B[49m\u001B[38;5;241;43m*\u001B[39;49m\u001B[38;5;241;43m*\u001B[39;49m\u001B[43mfit_and_score_kwargs\u001B[49m\u001B[43m,\u001B[49m\n\u001B[0;32m    856\u001B[0m \u001B[43m    \u001B[49m\u001B[43m)\u001B[49m\n\u001B[0;32m    857\u001B[0m \u001B[43m    \u001B[49m\u001B[38;5;28;43;01mfor\u001B[39;49;00m\u001B[43m \u001B[49m\u001B[43m(\u001B[49m\u001B[43mcand_idx\u001B[49m\u001B[43m,\u001B[49m\u001B[43m \u001B[49m\u001B[43mparameters\u001B[49m\u001B[43m)\u001B[49m\u001B[43m,\u001B[49m\u001B[43m \u001B[49m\u001B[43m(\u001B[49m\u001B[43msplit_idx\u001B[49m\u001B[43m,\u001B[49m\u001B[43m \u001B[49m\u001B[43m(\u001B[49m\u001B[43mtrain\u001B[49m\u001B[43m,\u001B[49m\u001B[43m \u001B[49m\u001B[43mtest\u001B[49m\u001B[43m)\u001B[49m\u001B[43m)\u001B[49m\u001B[43m \u001B[49m\u001B[38;5;129;43;01min\u001B[39;49;00m\u001B[43m \u001B[49m\u001B[43mproduct\u001B[49m\u001B[43m(\u001B[49m\n\u001B[0;32m    858\u001B[0m \u001B[43m        \u001B[49m\u001B[38;5;28;43menumerate\u001B[39;49m\u001B[43m(\u001B[49m\u001B[43mcandidate_params\u001B[49m\u001B[43m)\u001B[49m\u001B[43m,\u001B[49m\u001B[43m \u001B[49m\u001B[38;5;28;43menumerate\u001B[39;49m\u001B[43m(\u001B[49m\u001B[43mcv\u001B[49m\u001B[38;5;241;43m.\u001B[39;49m\u001B[43msplit\u001B[49m\u001B[43m(\u001B[49m\u001B[43mX\u001B[49m\u001B[43m,\u001B[49m\u001B[43m \u001B[49m\u001B[43my\u001B[49m\u001B[43m,\u001B[49m\u001B[43m \u001B[49m\u001B[43mgroups\u001B[49m\u001B[43m)\u001B[49m\u001B[43m)\u001B[49m\n\u001B[0;32m    859\u001B[0m \u001B[43m    \u001B[49m\u001B[43m)\u001B[49m\n\u001B[0;32m    860\u001B[0m \u001B[43m\u001B[49m\u001B[43m)\u001B[49m\n\u001B[0;32m    862\u001B[0m \u001B[38;5;28;01mif\u001B[39;00m \u001B[38;5;28mlen\u001B[39m(out) \u001B[38;5;241m<\u001B[39m \u001B[38;5;241m1\u001B[39m:\n\u001B[0;32m    863\u001B[0m     \u001B[38;5;28;01mraise\u001B[39;00m \u001B[38;5;167;01mValueError\u001B[39;00m(\n\u001B[0;32m    864\u001B[0m         \u001B[38;5;124m\"\u001B[39m\u001B[38;5;124mNo fits were performed. \u001B[39m\u001B[38;5;124m\"\u001B[39m\n\u001B[0;32m    865\u001B[0m         \u001B[38;5;124m\"\u001B[39m\u001B[38;5;124mWas the CV iterator empty? \u001B[39m\u001B[38;5;124m\"\u001B[39m\n\u001B[0;32m    866\u001B[0m         \u001B[38;5;124m\"\u001B[39m\u001B[38;5;124mWere there no candidates?\u001B[39m\u001B[38;5;124m\"\u001B[39m\n\u001B[0;32m    867\u001B[0m     )\n",
      "File \u001B[1;32mc:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\sklearn\\utils\\parallel.py:65\u001B[0m, in \u001B[0;36mParallel.__call__\u001B[1;34m(self, iterable)\u001B[0m\n\u001B[0;32m     60\u001B[0m config \u001B[38;5;241m=\u001B[39m get_config()\n\u001B[0;32m     61\u001B[0m iterable_with_config \u001B[38;5;241m=\u001B[39m (\n\u001B[0;32m     62\u001B[0m     (_with_config(delayed_func, config), args, kwargs)\n\u001B[0;32m     63\u001B[0m     \u001B[38;5;28;01mfor\u001B[39;00m delayed_func, args, kwargs \u001B[38;5;129;01min\u001B[39;00m iterable\n\u001B[0;32m     64\u001B[0m )\n\u001B[1;32m---> 65\u001B[0m \u001B[38;5;28;01mreturn\u001B[39;00m \u001B[38;5;28;43msuper\u001B[39;49m\u001B[43m(\u001B[49m\u001B[43m)\u001B[49m\u001B[38;5;241;43m.\u001B[39;49m\u001B[38;5;21;43m__call__\u001B[39;49m\u001B[43m(\u001B[49m\u001B[43miterable_with_config\u001B[49m\u001B[43m)\u001B[49m\n",
      "File \u001B[1;32mc:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\joblib\\parallel.py:1952\u001B[0m, in \u001B[0;36mParallel.__call__\u001B[1;34m(self, iterable)\u001B[0m\n\u001B[0;32m   1946\u001B[0m \u001B[38;5;66;03m# The first item from the output is blank, but it makes the interpreter\u001B[39;00m\n\u001B[0;32m   1947\u001B[0m \u001B[38;5;66;03m# progress until it enters the Try/Except block of the generator and\u001B[39;00m\n\u001B[0;32m   1948\u001B[0m \u001B[38;5;66;03m# reach the first `yield` statement. This starts the aynchronous\u001B[39;00m\n\u001B[0;32m   1949\u001B[0m \u001B[38;5;66;03m# dispatch of the tasks to the workers.\u001B[39;00m\n\u001B[0;32m   1950\u001B[0m \u001B[38;5;28mnext\u001B[39m(output)\n\u001B[1;32m-> 1952\u001B[0m \u001B[38;5;28;01mreturn\u001B[39;00m output \u001B[38;5;28;01mif\u001B[39;00m \u001B[38;5;28mself\u001B[39m\u001B[38;5;241m.\u001B[39mreturn_generator \u001B[38;5;28;01melse\u001B[39;00m \u001B[38;5;28;43mlist\u001B[39;49m\u001B[43m(\u001B[49m\u001B[43moutput\u001B[49m\u001B[43m)\u001B[49m\n",
      "File \u001B[1;32mc:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\joblib\\parallel.py:1595\u001B[0m, in \u001B[0;36mParallel._get_outputs\u001B[1;34m(self, iterator, pre_dispatch)\u001B[0m\n\u001B[0;32m   1592\u001B[0m     \u001B[38;5;28;01myield\u001B[39;00m\n\u001B[0;32m   1594\u001B[0m     \u001B[38;5;28;01mwith\u001B[39;00m \u001B[38;5;28mself\u001B[39m\u001B[38;5;241m.\u001B[39m_backend\u001B[38;5;241m.\u001B[39mretrieval_context():\n\u001B[1;32m-> 1595\u001B[0m         \u001B[38;5;28;01myield from\u001B[39;00m \u001B[38;5;28mself\u001B[39m\u001B[38;5;241m.\u001B[39m_retrieve()\n\u001B[0;32m   1597\u001B[0m \u001B[38;5;28;01mexcept\u001B[39;00m \u001B[38;5;167;01mGeneratorExit\u001B[39;00m:\n\u001B[0;32m   1598\u001B[0m     \u001B[38;5;66;03m# The generator has been garbage collected before being fully\u001B[39;00m\n\u001B[0;32m   1599\u001B[0m     \u001B[38;5;66;03m# consumed. This aborts the remaining tasks if possible and warn\u001B[39;00m\n\u001B[0;32m   1600\u001B[0m     \u001B[38;5;66;03m# the user if necessary.\u001B[39;00m\n\u001B[0;32m   1601\u001B[0m     \u001B[38;5;28mself\u001B[39m\u001B[38;5;241m.\u001B[39m_exception \u001B[38;5;241m=\u001B[39m \u001B[38;5;28;01mTrue\u001B[39;00m\n",
      "File \u001B[1;32mc:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\joblib\\parallel.py:1707\u001B[0m, in \u001B[0;36mParallel._retrieve\u001B[1;34m(self)\u001B[0m\n\u001B[0;32m   1702\u001B[0m \u001B[38;5;66;03m# If the next job is not ready for retrieval yet, we just wait for\u001B[39;00m\n\u001B[0;32m   1703\u001B[0m \u001B[38;5;66;03m# async callbacks to progress.\u001B[39;00m\n\u001B[0;32m   1704\u001B[0m \u001B[38;5;28;01mif\u001B[39;00m ((\u001B[38;5;28mlen\u001B[39m(\u001B[38;5;28mself\u001B[39m\u001B[38;5;241m.\u001B[39m_jobs) \u001B[38;5;241m==\u001B[39m \u001B[38;5;241m0\u001B[39m) \u001B[38;5;129;01mor\u001B[39;00m\n\u001B[0;32m   1705\u001B[0m     (\u001B[38;5;28mself\u001B[39m\u001B[38;5;241m.\u001B[39m_jobs[\u001B[38;5;241m0\u001B[39m]\u001B[38;5;241m.\u001B[39mget_status(\n\u001B[0;32m   1706\u001B[0m         timeout\u001B[38;5;241m=\u001B[39m\u001B[38;5;28mself\u001B[39m\u001B[38;5;241m.\u001B[39mtimeout) \u001B[38;5;241m==\u001B[39m TASK_PENDING)):\n\u001B[1;32m-> 1707\u001B[0m     \u001B[43mtime\u001B[49m\u001B[38;5;241;43m.\u001B[39;49m\u001B[43msleep\u001B[49m\u001B[43m(\u001B[49m\u001B[38;5;241;43m0.01\u001B[39;49m\u001B[43m)\u001B[49m\n\u001B[0;32m   1708\u001B[0m     \u001B[38;5;28;01mcontinue\u001B[39;00m\n\u001B[0;32m   1710\u001B[0m \u001B[38;5;66;03m# We need to be careful: the job list can be filling up as\u001B[39;00m\n\u001B[0;32m   1711\u001B[0m \u001B[38;5;66;03m# we empty it and Python list are not thread-safe by\u001B[39;00m\n\u001B[0;32m   1712\u001B[0m \u001B[38;5;66;03m# default hence the use of the lock\u001B[39;00m\n",
      "\u001B[1;31mKeyboardInterrupt\u001B[0m: "
     ]
    }
   ],
   "source": [
    "#svc grid searchcv\n",
    "param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100],\n",
    "              'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],\n",
    "              'gamma': ['auto', 'scale']}\n",
    "gs_label_2_svc = GridSearchCV(estimator=SVC(), param_grid=param_grid, scoring='accuracy', cv=5, n_jobs=-1)\n",
    "gs_label_2_svc = gs_label_2_svc.fit(X_train_label2_pca, y_label2_train)\n",
    "print(gs_label_2_svc.best_score_)\n",
    "print(gs_label_2_svc.best_params_)\n",
    "print(gs_label_2_svc.best_params_['C'])\n",
    "print(gs_label_2_svc.best_params_['kernel'])\n",
    "print(gs_label_2_svc.best_params_['gamma'])\n",
    "#evaluate train model\n",
    "pred_label_2_svc = gs_label_2_svc.predict(X_valid_label2_pca)\n",
    "print('Validate accuracy: %.3f' % accuracy_score(y_true=y_valid_label_2, y_pred=pred_label_2_svc))\n",
    "print('Validate precision: %.3f' % precision_score(y_true=y_valid_label_2, y_pred=pred_label_2_svc, average='micro'))\n",
    "print('Validate recall: %.3f' % recall_score(y_true=y_valid_label_2, y_pred=pred_label_2_svc,    average='micro'))\n",
    "print('Validate f1: %.3f' % f1_score(y_true=y_valid_label_2, y_pred=pred_label_2_svc,    average='micro'))\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-09-23T17:14:45.627208700Z",
     "start_time": "2023-09-23T16:02:14.230929300Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "# Cross validation for label 3"
   ],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\joblib\\externals\\loky\\backend\\context.py:136: UserWarning: Could not find the number of physical cores for the following reason:\n",
      "[WinError 2] The system cannot find the file specified\n",
      "Returning the number of logical cores instead. You can silence this warning by setting LOKY_MAX_CPU_COUNT to the number of cores you want to use.\n",
      "  warnings.warn(\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\joblib\\externals\\loky\\backend\\context.py\", line 257, in _count_physical_cores\n",
      "    cpu_info = subprocess.run(\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\subprocess.py\", line 501, in run\n",
      "    with Popen(*popenargs, **kwargs) as process:\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\subprocess.py\", line 947, in __init__\n",
      "    self._execute_child(args, executable, preexec_fn, close_fds,\n",
      "  File \"c:\\users\\sumeela\\appdata\\local\\programs\\python\\python39\\lib\\subprocess.py\", line 1416, in _execute_child\n",
      "    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Cross-validation accuracy for knn_label_3: 0.90\n",
      "Cross-validation accuracy for svc_label_3: 0.98\n"
     ]
    }
   ],
   "source": [
    "cv_score = cross_val_score(KNN(n_neighbors=5), X_train_pca, y_label_3_train, cv=5)\n",
    "print(f\"Cross-validation accuracy for knn_label_3: {np.mean(cv_score):.2f}\")\n",
    "\n",
    "cv_score = cross_val_score(SVC(random_state=42, kernel='linear', gamma='auto'), X_train_pca, y_label_3_train, cv=5)\n",
    "print(f\"Cross-validation accuracy for svc_label_3: {np.mean(cv_score):.2f}\")\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-09-23T08:37:06.485969700Z",
     "start_time": "2023-09-23T08:36:22.056742100Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "# Grid search for label 3"
   ],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Validate accuracy for label 3: 0.997\n",
      "Validate precision for label 3: 0.997\n",
      "Validate recall for label 3: 0.997\n",
      "Validate f1 for label 3: 0.997\n"
     ]
    }
   ],
   "source": [
    "param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100],\n",
    "              'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],\n",
    "              'gamma': ['auto', 'scale']}\n",
    "gs_label_3_svc_ = GridSearchCV(estimator=SVC(), param_grid=param_grid, scoring='accuracy', cv=5, n_jobs=-1)\n",
    "gs_label_3_svc = SVC(C=0.1, gamma='auto', kernel='linear')\n",
    "gs_label_3_svc = gs_label_3_svc.fit(X_train_pca, y_label_3_train)\n",
    "\n",
    "\n",
    "#evaluate train model\n",
    "pred_label_3_svc = gs_label_3_svc.predict(X_valid_pca)\n",
    "validate3 = pd.DataFrame()\n",
    "\n",
    "validate3['LABEL3']=pred_label_3_svc\n",
    "validate3.to_csv('validate3.csv', index=False)\n",
    "print('Validate accuracy for label 3: %.3f' % accuracy_score(y_true=y_valid_label3, y_pred=pred_label_3_svc))\n",
    "print('Validate precision for label 3: %.3f' % precision_score(y_true=y_valid_label3, y_pred=pred_label_3_svc, average='micro'))\n",
    "print('Validate recall for label 3: %.3f' % recall_score(y_true=y_valid_label3, y_pred=pred_label_3_svc,    average='micro'))\n",
    "print('Validate f1 for label 3: %.3f' % f1_score(y_true=y_valid_label3, y_pred=pred_label_3_svc,    average='micro'))\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-10-13T07:23:18.896223100Z",
     "start_time": "2023-10-13T07:23:12.582114600Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "# Cross validation for label 4"
   ],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Cross-validation accuracy for knn_label_4: 0.86\n",
      "Cross-validation accuracy for svc_label_4: 0.84\n"
     ]
    }
   ],
   "source": [
    "cv_score = cross_val_score(KNN(n_neighbors=5), X_train_pca, y_label_4_train, cv=5)\n",
    "print(f\"Cross-validation accuracy for knn_label_4: {np.mean(cv_score):.2f}\")\n",
    "\n",
    "cv_score = cross_val_score(SVC(random_state=42, kernel='linear', gamma='auto'), X_train_pca, y_label_4_train, cv=5)\n",
    "print(f\"Cross-validation accuracy for svc_label_4: {np.mean(cv_score):.2f}\")"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-09-23T08:48:50.904173300Z",
     "start_time": "2023-09-23T08:43:08.896788700Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [
    "# Grid search for label 4"
   ],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0.8638849929873773\n",
      "{'n_neighbors': 7}\n",
      "Validate accuracy for label 4: 0.907\n",
      "Validate precision for label 4: 0.907\n",
      "Validate recall for label 4: 0.907\n",
      "Validate f1 for label 4: 0.907\n"
     ]
    }
   ],
   "source": [
    "# grid searchcv for knn\n",
    "param_grid = {'n_neighbors': np.arange(1, 25),\n",
    "                'weights': ['uniform', 'distance'],\n",
    "              'p': [1, 2]    }\n",
    "gs_label_4 = GridSearchCV(estimator=KNN(), param_grid=param_grid, scoring='accuracy', cv=5, n_jobs=-1)\n",
    "gs_label_4 = gs_label_4.fit(X_train_pca, y_label_4_train)\n",
    "print(gs_label_4.best_score_)\n",
    "print(gs_label_4.best_params_)\n",
    "#evaluate train model\n",
    "pred_label_4 = gs_label_4.predict(X_valid_pca)\n",
    "print('Validate accuracy for label 4: %.3f' % accuracy_score(y_true=y_valid_label4, y_pred=pred_label_4))\n",
    "print('Validate precision for label 4: %.3f' % precision_score(y_true=y_valid_label4, y_pred=pred_label_4, average='micro'))\n",
    "print('Validate recall for label 4: %.3f' % recall_score(y_true=y_valid_label4, y_pred=pred_label_4,    average='micro'))\n",
    "print('Validate f1 for label 4: %.3f' % f1_score(y_true=y_valid_label4, y_pred=pred_label_4,    average='micro'))\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-09-23T14:59:21.689824500Z",
     "start_time": "2023-09-23T14:55:24.314877100Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Validate accuracy for label 4: 0.924\n",
      "Validate precision for label 4: 0.924\n",
      "Validate recall for label 4: 0.924\n",
      "Validate f1 for label 4: 0.924\n"
     ]
    }
   ],
   "source": [
    "# grid searchcv for svc\n",
    "param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100],\n",
    "              'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],\n",
    "              'gamma': ['auto', 'scale']}\n",
    "gs_label_4_svc_ = GridSearchCV(estimator=SVC(), param_grid=param_grid, scoring='accuracy', cv=5, n_jobs=-1)\n",
    "gs_label_4_svc = SVC(C=0.01, gamma='auto', kernel='linear')\n",
    "gs_label_4_svc = gs_label_4_svc.fit(X_train_pca, y_label_4_train)\n",
    "\n",
    "#evaluate train model\n",
    "pred_label_4_svc = gs_label_4_svc.predict(X_valid_pca)\n",
    "validate4 = pd.DataFrame()\n",
    "validate4['LABEL4']=pred_label_4_svc\n",
    "validate4.to_csv('validate4.csv', index=False)\n",
    "print('Validate accuracy for label 4: %.3f' % accuracy_score(y_true=y_valid_label4, y_pred=pred_label_4_svc))\n",
    "print('Validate precision for label 4: %.3f' % precision_score(y_true=y_valid_label4, y_pred=pred_label_4_svc, average='micro'))\n",
    "print('Validate recall for label 4: %.3f' % recall_score(y_true=y_valid_label4, y_pred=pred_label_4_svc,    average='micro'))\n",
    "print('Validate f1 for label 4: %.3f' % f1_score(y_true=y_valid_label4, y_pred=pred_label_4_svc,    average='micro'))\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-10-13T07:27:06.973324200Z",
     "start_time": "2023-10-13T07:26:08.459283300Z"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "outputs": [],
   "source": [
    "#save on to csv file\n",
    "validate.to_csv('validate.csv', index=False)\n"
   ],
   "metadata": {
    "collapsed": false
   }
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "        feature_1   feature_2   feature_3   feature_4   feature_5   feature_6  \\\n",
      "count  744.000000  744.000000  744.000000  744.000000  744.000000  744.000000   \n",
      "mean     0.005398    0.046413   -0.003152    0.007886   -0.084819   -0.042217   \n",
      "std      0.077064    0.047604    0.060536    0.081165    0.081220    0.056322   \n",
      "min     -0.215194   -0.088241   -0.179731   -0.226406   -0.463127   -0.235149   \n",
      "25%     -0.044833    0.013775   -0.044619   -0.036708   -0.132045   -0.077440   \n",
      "50%     -0.000147    0.048187   -0.006010    0.013099   -0.083526   -0.041958   \n",
      "75%      0.049941    0.080107    0.036146    0.059325   -0.032098   -0.003731   \n",
      "max      0.231716    0.194577    0.232407    0.232575    0.214991    0.143599   \n",
      "\n",
      "        feature_7   feature_8   feature_9  feature_10  ...  feature_759  \\\n",
      "count  744.000000  744.000000  744.000000  744.000000  ...   744.000000   \n",
      "mean     0.115549   -0.060058   -0.014774   -0.020346  ...    -0.004586   \n",
      "std      0.099040    0.067562    0.060351    0.064100  ...     0.074476   \n",
      "min     -0.254034   -0.273333   -0.161935   -0.262905  ...    -0.270497   \n",
      "25%      0.042790   -0.104205   -0.057439   -0.062648  ...    -0.049317   \n",
      "50%      0.117624   -0.057504   -0.019028   -0.021327  ...    -0.000828   \n",
      "75%      0.182336   -0.017095    0.024792    0.021423  ...     0.045909   \n",
      "max      0.445175    0.119893    0.186116    0.181352  ...     0.214002   \n",
      "\n",
      "       feature_760  feature_761  feature_762  feature_763  feature_764  \\\n",
      "count   744.000000   744.000000   744.000000   744.000000   744.000000   \n",
      "mean      0.053022     0.057065    -0.035076    -0.042026     0.011620   \n",
      "std       0.058834     0.072683     0.140571     0.076752     0.063125   \n",
      "min      -0.149944    -0.201129    -0.456167    -0.317826    -0.207807   \n",
      "25%       0.014898     0.013073    -0.128789    -0.094230    -0.027420   \n",
      "50%       0.056800     0.057820    -0.035386    -0.044026     0.015901   \n",
      "75%       0.091388     0.103593     0.059818     0.012584     0.053353   \n",
      "max       0.246139     0.281964     0.412875     0.206010     0.227464   \n",
      "\n",
      "       feature_765  feature_766  feature_767  feature_768  \n",
      "count   744.000000   744.000000   744.000000   744.000000  \n",
      "mean     -0.005678     0.046011     0.038638    -0.041321  \n",
      "std       0.057875     0.071044     0.057567     0.087205  \n",
      "min      -0.242382    -0.137129    -0.128690    -0.302213  \n",
      "25%      -0.042252     0.001658    -0.001763    -0.099365  \n",
      "50%      -0.003575     0.041454     0.036783    -0.038746  \n",
      "75%       0.035534     0.085985     0.076028     0.014671  \n",
      "max       0.152160     0.289267     0.254390     0.217821  \n",
      "\n",
      "[8 rows x 768 columns]\n"
     ]
    }
   ],
   "source": [
    "print(X_test.describe())"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-09-23T17:17:26.948368600Z",
     "start_time": "2023-09-23T17:17:25.769521500Z"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "outputs": [],
   "source": [
    "pred_test_label1= gs.predict(X_test_pca)\n",
    "pred_test_label2= gs_label_2.predict(X_test_label2_pca)\n",
    "pred_test_label3= gs_label_3_svc.predict(X_test_pca)\n",
    "pred_test_label4= gs_label_4_svc.predict(X_test_pca)\n",
    "\n",
    "output['label_1'] = pred_test_label1\n",
    "output['label_2'] = pred_test_label2\n",
    "output['label_3'] = pred_test_label3\n",
    "output['label_4'] = pred_test_label4\n",
    "\n",
    "output.to_csv('label.csv', index=False)\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2023-09-23T17:24:21.777975800Z",
     "start_time": "2023-09-23T17:24:13.538488100Z"
    }
   }
  },
  {
   "cell_type": "markdown",
   "source": [],
   "metadata": {
    "collapsed": false
   }
  }
 ],
 "metadata": {
  "accelerator": "GPU",
  "colab": {
   "authorship_tag": "ABX9TyM9eJCl3RNlGAx/bODx6abF",
   "gpuType": "T4",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
