"""
Python script to analyse key financial ratios using the DBSCAN algorithm
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import seaborn as sns

ratio_1 = 'Net Profit Margin'
ratio_2 = 'ROA'
industry = 'Energy'

def target_industry(industry):
    #returns all data for the chosen industry

    return  data[data['Sector'] == industry].iloc[:,2:]

def preprocessing(data):
    #scale the data in each column
    for col in range(len(data.columns)):
        data.iloc[:,col] = StandardScaler().fit_transform(data.iloc[:,col].values.reshape(len(data),1))

    return data

def model(X, eps = 0.5, min_samples = 5):
    #compute the DBSAN model
    #print the number of clusters and noicse points
    db = DBSCAN(eps = eps, min_samples = min_samples).fit(X)
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)

    #reformatting and return results - ratio columns and cluster number (-1 for noise)
    labels = pd.DataFrame(labels, columns = ['Labels'])
    X = X.reset_index()
    X.drop("index",axis=1,inplace=True)
    results = pd.concat([X, labels], axis =1)

    return results

def plot(data, ratio_1, ratio_2):
    #plot the results
    figure = sns.lmplot(data = data, x = ratio_1, y = ratio_2, hue = 'Labels',
                        fit_reg = False, legend = True, legend_out = True)
    plt.show()


if __name__ == '__main__':

    data = pd.read_csv('Book1.csv')
    sub = target_industry(industry)
    X = preprocessing(sub)
    results = model(X[[ratio_1, ratio_2]])
    plot(results, ratio_1, ratio_2)
