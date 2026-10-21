import pandas as pd, numpy as np, json, re
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
d=pd.read_csv('spacex.csv'); d.columns=[c.strip() for c in d.columns]
d['Booster_Version']=d.Booster_Version.str.strip()
d['class']=d.Landing_Outcome.str.strip().str.startswith('Success').astype(int)
d['FlightNumber']=np.arange(1,len(d)+1)
def block(b):
    if 'v1.0' in b: return 0
    if 'v1.1' in b: return 1
    if 'FT' in b: return 2
    if 'B4' in b: return 4
    if 'B5' in b: return 5
    return 3
d['Block']=d.Booster_Version.map(block)
X=pd.concat([d[['FlightNumber','PAYLOAD_MASS__KG_','Block']], pd.get_dummies(d.Orbit.str.strip(),prefix='Orbit'), pd.get_dummies(d.Launch_Site.str.strip(),prefix='Site')],axis=1).astype(float)
y=d['class'].values
Xs=StandardScaler().fit_transform(X)
Xtr,Xte,ytr,yte=train_test_split(Xs,y,test_size=0.2,random_state=2)
print(X.shape, len(ytr), len(yte), yte.sum(), len(yte)-yte.sum())
grids={
 'Logistic Regression':(LogisticRegression(max_iter=1000),{'C':[0.01,0.1,1],'penalty':['l2'],'solver':['lbfgs']}),
 'SVM':(SVC(),{'kernel':['linear','rbf','poly','sigmoid'],'C':np.logspace(-3,3,5).tolist(),'gamma':np.logspace(-3,3,5).tolist()}),
 'Decision Tree':(DecisionTreeClassifier(random_state=0),{'criterion':['gini','entropy'],'splitter':['best','random'],'max_depth':[2*n for n in range(1,10)],'max_features':['sqrt'],'min_samples_leaf':[1,2,4],'min_samples_split':[2,5,10]}),
 'KNN':(KNeighborsClassifier(),{'n_neighbors':list(range(1,11)),'algorithm':['auto'],'p':[1,2]})}
out={}
for n,(m,g) in grids.items():
    gs=GridSearchCV(m,g,cv=10).fit(Xtr,ytr)
    acc=gs.score(Xte,yte); cm=confusion_matrix(yte,gs.predict(Xte))
    out[n]={'cv':gs.best_score_,'test':acc,'cm':cm.tolist(),'params':{k:(v if not isinstance(v,(np.floating,np.integer)) else float(v)) for k,v in gs.best_params_.items()}}
    print(n,round(gs.best_score_,4),round(acc,4),cm.tolist(),gs.best_params_)
json.dump(out,open('ml.json','w'),default=str)
