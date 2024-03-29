# -*- coding: utf-8 -*-
"""Minimizing_churn_rate_through_analysis_of financial_habits _through_analysis_of_financial_habits

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11TxyDt7Ce4Ji8HfUf73kLn6zuJRACBoH
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

dataset = pd.read_csv('churn_data.csv') # Users who were 60 days enrolled, churn in the next 30

dataset.head(5) # Viewing the Data
dataset.columns
dataset.describe()

# Removing NaN
dataset.isna().any()
dataset.isna().sum()
dataset = dataset.drop(columns=['credit_score', 'rewards_earned'])

# Cleaning Data
dataset = dataset[dataset['credit_score'] >= 300]

## Histograms
dataset2 = dataset.drop(columns=['user', 'churn'])
fig = plt.figure(figsize=(15, 12))
plt.suptitle('Histograms of Numerical Columns', fontsize=20)
for i in range(1, dataset2.shape[1] + 1):
    plt.subplot(6, 5, i)
    f = plt.gca()
    f.axes.get_yaxis().set_visible(False)
    f.set_title(dataset2.columns.values[i - 1])

    vals = np.size(dataset2.iloc[:, i - 1].unique())

    plt.hist(dataset2.iloc[:, i - 1], bins=vals, color='#3F5D7D')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

## Pie Plots
dataset2 = dataset[['housing', 'is_referred', 'app_downloaded',
                    'web_user', 'app_web_user', 'ios_user',
                    'android_user', 'registered_phones', 'payment_type',
                    'waiting_4_loan', 'cancelled_loan',
                    'received_loan', 'rejected_loan', 'zodiac_sign',
                    'left_for_two_month_plus', 'left_for_one_month', 'is_referred']]
fig = plt.figure(figsize=(15, 12))
plt.suptitle('Pie Chart Distributions', fontsize=20)
for i in range(1, dataset2.shape[1] + 1):
    plt.subplot(6, 3, i)
    f = plt.gca()
    f.axes.get_yaxis().set_visible(False)
    f.set_title(dataset2.columns.values[i - 1])

    values = dataset2.iloc[:, i - 1].value_counts(normalize=True).values
    index = dataset2.iloc[:, i - 1].value_counts(normalize=True).index
    plt.pie(values, labels=index, autopct='%1.1f%%')
    plt.axis('equal')
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

## Exploring Uneven Features
dataset[dataset2.waiting_4_loan == 1].churn.value_counts()
dataset[dataset2.cancelled_loan == 1].churn.value_counts()
dataset[dataset2.received_loan == 1].churn.value_counts()
dataset[dataset2.rejected_loan == 1].churn.value_counts()
dataset[dataset2.left_for_one_month == 1].churn.value_counts()

## Correlation with Response Variable
dataset2.drop(columns=['housing', 'payment_type',
                       'registered_phones', 'zodiac_sign']
    ).corrwith(dataset.churn).plot.bar(figsize=(20,10),
              title='Correlation with Response variable',
              fontsize=15, rot=45,
              grid=True)

## Correlation Matrix
sns.set(style="white")

# Compute the correlation matrix
corr = dataset.drop(columns=['user', 'churn']).corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(18, 15))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

# Removing Correlated Fields
dataset = dataset.drop(columns=['app_web_user'])

dataset.to_csv('new_churn_data.csv', index=False)

import pandas as pd
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt

dataset = pd.read_csv('new_churn_data.csv')

# One-Hot Encoding
dataset = pd.get_dummies(dataset, drop_first=True)

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(dataset.drop(columns='churn'), dataset['churn'],
                                                    test_size=0.2,
                                                    random_state=0)

# Balancing the Training Set
from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=0)
X_train_resampled, y_train_resampled = sm.fit_resample(X_train, y_train)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train_scaled = sc_X.fit_transform(X_train_resampled)
X_test_scaled = sc_X.transform(X_test)

#### Model Building ####

# Fitting Model to the Training Set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state=0)
classifier.fit(X_train_scaled, y_train_resampled)

# Predicting Test Set
y_pred = classifier.predict(X_test_scaled)

# Evaluating Results
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, precision_score, recall_score
cm = confusion_matrix(y_test, y_pred)
accuracy_score(y_test, y_pred)
precision_score(y_test, y_pred)
recall_score(y_test, y_pred)
f1_score(y_test, y_pred)

df_cm = pd.DataFrame(cm, index=(0, 1), columns=(0, 1))
plt.figure(figsize=(10, 7))
sns.set(font_scale=1.4)
sns.heatmap(df_cm, annot=True, fmt='g')
print("Test Data Accuracy: %0.4f" % accuracy_score(y_test, y_pred))

# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=classifier, X=X_train_scaled, y=y_train_resampled, cv=10)
print("Logistic Regression Accuracy: %0.3f (+/-%0.3f)" % (accuracies.mean(), accuracies.std() * 2))

#### Feature Selection ####

## Feature Selection
# Recursive Feature Elimination
from sklearn.feature_selection import RFE

# Model to Test
classifier = LogisticRegression()
# Select Best X Features
rfe = RFE(estimator=classifier, n_features_to_select=20)
rfe = rfe.fit(X_train_scaled, y_train_resampled)
# Summarize the selection of the attributes
print(rfe.support_)
print(rfe.ranking_)
selected_features = X_train.columns[rfe.support_]

# New Correlation Matrix
sns.set(style="white")

# Compute the correlation matrix
corr = X_train[selected_features].corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(18, 15))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

# Fitting Model to the Training Set with selected features
selected_features = X_train.columns[rfe.support_]
classifier.fit(X_train_scaled[:, rfe.support_], y_train_resampled)

# Get the indices of selected features
selected_feature_indices = [X_train.columns.get_loc(col) for col in selected_features]

# Predicting Test Set using selected features
y_pred = classifier.predict(X_test_scaled[:, selected_feature_indices])

# Evaluating Results
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, precision_score, recall_score
cm = confusion_matrix(y_test, y_pred)
accuracy_score(y_test, y_pred)
precision_score(y_test, y_pred)
recall_score(y_test, y_pred)
f1_score(y_test, y_pred)

df_cm = pd.DataFrame(cm, index=(0, 1), columns=(0, 1))
plt.figure(figsize=(10, 7))
sns.set(font_scale=1.4)
sns.heatmap(df_cm, annot=True, fmt='g')
print("Test Data Accuracy: %0.4f" % accuracy_score(y_test, y_pred))

from sklearn.model_selection import cross_val_score

# Get the indices of selected features
selected_feature_indices = [X_train.columns.get_loc(col) for col in selected_features]

# Applying k-Fold Cross Validation
accuracies = cross_val_score(estimator=classifier,
                             X=X_train_scaled[:, selected_feature_indices],
                             y=y_train_resampled, cv=10)
print("Logistic Regression Accuracy: %0.3f (+/- %0.3f)" % (accuracies.mean(), accuracies.std() * 2))

final_results = pd.concat([y_test, dataset['user']], axis=1).dropna()
final_results['predicted_churn'] = y_pred
final_results = final_results[['user', 'churn', 'predicted_churn']].reset_index(drop=True)

