import numpy as np
import pandas as pd
import time
#import pylab as pl
import random
import multiprocessing
from sklearn.neighbors import KNeighborsClassifier
from scipy.misc import comb
from multiprocessing import Process, Manager, Lock
from itertools import combinations

stime = int(time.time())

variables = ['no_tms_ai_srvcnum','ave_cst','sp_dist','fodder_pur_mont','crop_res_mont','concentrate_mont', 
             'M_lab_mt_wg','lt_sld','freq_num','fnd_prf_mthd_num','kp_rcrds_num','brd_mthd_clvdnum',
             'totalLlabour','no_ai_bull','Factor1']
variables = ['no_tms_ai_srvcnum','ave_cst','sp_dist','fodder_pur_mont', 
             'M_lab_mt_wg','fnd_prf_mthd_num','kp_rcrds_num','brd_mthd_clvdnum',
             'totalLlabour','no_ai_bull']
variable3s = ['trans_cost', 'tms_vist', 'total_landsize', 'total_livestock_number', 'kp_rcrds_num']

variables1 = ['fnd_prf_mthd_num','kp_rcrds_num' ,'no_tms_ai_srvcnum','brd_mthd_clvdnum','ave_cst', 'sp_dist', 'no_ai_bull' , 'dew_tms_num','sys_rn_num','peak_bst','lt_sld' ,'status_num', 'fodder_pur_mont' ]

f = open('Kenya1.csv', 'r')
kmodelling = pd.read_csv(f)
cats = kmodelling

random_sampling = False
targetAccuracy=0.89

if random_sampling:
    # Create training and test sets fo data
    numitems = len(cats)
    percenttest = 0.3
    test = cats.sample(frac=percenttest, replace=True)
    test_ids = []
    for rec in test.iterrows():
        test_ids.append(rec[0])

    train = cats[~cats.id.isin(test_ids)]

else:
    numitems = len(kmodelling)
    percenttrain = 0.7
    numtrain = int(numitems*percenttrain)
    numtest = numitems - numtrain
    train = kmodelling[0:numtrain]
    test = kmodelling[numtrain:numitems]
    
#### ----------- End of preps ------------


def total_combinations(l,h):
    total = 0
    for i in range(l,h):
        total += int(comb(len(variables), i))

    return total

def analyse(feats, k=3):
    neighbors = k
    classifier = KNeighborsClassifier(neighbors)
    classifier.fit(train[feats], train['pref_brd_mthd_num'])
    predictions = classifier.predict(test[feats])
    # Calculate accuracy
    numtest = len(test)
    correct = 0
    i = 0
    for index, row in test.iterrows():
        if predictions[i] == row['pref_brd_mthd_num']: correct += 1
        i += 1
    return float(correct) / float(numtest)

def k_value(feats, target='pref_brd_mthd_num'):
    largest = 0
    start_k = 3
    end_k = 4
    no_k = 1
    for n in range(start_k, end_k):
        clf = KNeighborsClassifier(n_neighbors=n)
        clf.fit(train[feats], train[target])
        preds = clf.predict(test[feats])
        accuracy = np.where(preds == test[target], 1, 0).sum() / float(len(test))
        if accuracy > largest:
            largest = accuracy
            no_k = n
    return no_k

def execute_analysis(l, vfrequency, params,feats):
    k = k_value(feats)
    anlys = analyse(feats, k)

    l.acquire()
    try:
        if anlys > params['max_accuracy']:
            params['max_accuracy'] = anlys
            params['significant_list'] = feats
            params['sig_k'] = k
        if anlys > targetAccuracy:
            for f in feats:
                vfrequency[f] += 1
    finally:
        l.release()

if __name__ == '__main__':
    significant_list = []
    max_accuracy = 0
    sig_k = 0

    variable_frequency = {}
    for a in variables:
        variable_frequency.update({a: 0})

    procs = []
    totalProcesses = multiprocessing.cpu_count()
    print(totalProcesses)
    init_process = True
    lock = Lock()

    with Manager() as manager:
        fts = manager.dict(variable_frequency)
        params = manager.dict({'max_accuracy': max_accuracy, 'significant_list':significant_list, 'sig_k':sig_k})
        
        maxrange=len(variables)
        for i in range(3, maxrange):
            combs = list(combinations(variables,i))
            totalcombinations = len(combs)
            if init_process:
                init_process = False
                for t in range(totalProcesses): 
                    totalcombinations -= 1
                    current_features = list(combs[totalcombinations])
                    print(current_features)             
                    proc = Process(target=execute_analysis, args=(lock, fts, params,current_features))
                    procs.append(proc)
                    proc.start()

            while totalcombinations > 0:
                for p in procs:
                    if not p.is_alive():
                        totalcombinations -= 1
                        current_features = list(combs[totalcombinations])
                        indx = procs.index(p)
                        procs[indx] = Process(target=execute_analysis, args=(lock,fts, params, current_features))
                        procs[indx].start()
                       
                       
            #For each number of features print out statics
            
            print("------------------------------------------------")
            print("Number of features ",str(i))
            print('Maximum Accuracy:', params['max_accuracy'])
            print('Significant List', params['significant_list'])
            print('Significant K', params['sig_k'])
            print(fts)
            print("------------------------------------------------")
            print("n/***********************************************")
            
        
        max_accuracy = params['max_accuracy']
        significant_list = params['significant_list']
        sig_k = params['sig_k']
        variable_frequency = fts

        for p in procs:
            if p.is_alive():
                p.join()

        etime = int(time.time())
        #print("|||||||||||||||||||||| Overall Stats |||||||||||||")
        print('Time Taken: ', etime - stime)
        print('Accuracy:', max_accuracy)
        print('Significant List', significant_list)
        print('Significant K', sig_k)
        print("-----------------------------------------------------")
        print(variable_frequency)
        #for x in variable_frequency:
            #print(x, "=>", str(variable_frequency[x]))