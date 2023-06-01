import numpy as np
import sklearn.datasets as sk
import scipy.optimize as opt

def fromRowToColumn(v):
    return v.reshape((v.size, 1))

def calc_accuracy(labels, predicted):
    #Needs two lists
    confronted = (labels == predicted)
    TP = 0
    for i in confronted:
        if(i == True):
            TP = TP + 1
    
    return TP/len(predicted)

def load_iris_without_setosa():
    D, L = sk.load_iris()['data'].T, sk.load_iris()['target']
    D = D[:, L != 0] # We remove setosa from D
    L = L[L!=0] # We remove setosa from L
    L[L==2] = 0 
    return D, L

def split_db_2to1(D, L, seed=0):#versicolor=1, virginica=0
    # 2/3 dei dati per il training----->100 per training, 50 per test
    nTrain = int(D.shape[1]*2.0/3.0)
    np.random.seed(seed)
    idx = np.random.permutation(D.shape[1])
    idxTrain = idx[0:nTrain]
    idxTest = idx[nTrain:]
    DTR = D[:, idxTrain]
    DTE = D[:, idxTest]
    LTR = L[idxTrain]
    LTE = L[idxTest]
    return (DTR, LTR), (DTE, LTE)  # DTR= data training, LTR= Label training
    # DTE= Data test, LTE= label testing

def transform(DTE, w, b):
    posteriors = np.dot(w.T,DTE)+b
    posteriors[posteriors>0] = 1
    posteriors[posteriors<=0] = 0
    return posteriors

class logReg():
    def __init__(self,D,L,l):
        self.DTR=D
        self.ZTR=L*2.0-1.0
        self.l=l
        self.dim=D.shape[0]

    def logreg_obj(self,v):
        phi = features_expansion(DTR)
        w= fromRowToColumn(v[0:phi.shape[0]])
        b=v[-1]
        scores=np.dot(w.T,phi)+b
        loss_per_sample=np.logaddexp(0,-self.ZTR*scores)
        loss=loss_per_sample.mean()+0.5*self.l*np.linalg.norm(w)**2
        return loss
    
    def train(self):
        x_stacked = features_expansion(DTR)
        x0=np.zeros(x_stacked.shape[0]+1)
        xOpt,fOpt,d=opt.fmin_l_bfgs_b(self.logreg_obj,x0=x0,approx_grad=True)
        return xOpt
    

def features_expansion(Dataset):#restituisce phi
    expansion = []
    for i in range(Dataset.shape[1]):
        vec = np.reshape(np.dot(fromRowToColumn(Dataset[:, i]), fromRowToColumn(Dataset[:, i]).T), (-1, 1), order='F')
        expansion.append(vec)
    return np.vstack((np.hstack(expansion), Dataset))

if __name__ == '__main__':
    D, L = load_iris_without_setosa()
    (DTR, LTR), (DTE, LTE) = split_db_2to1(D, L)
    print(DTR.shape[0])
    
    """logreg = logReg(DTR, LTR, 0.000001)
    w,b = logreg.train()
    labels = transform(DTE, w, b)
    labels = list(map(int,labels.flatten()))
    print(1-calc_accuracy(LTE, labels)) """

    """ test_x2 = phi_x(DTE.T) """
    regressor=logReg(DTR,LTR,0.001)
    x=regressor.train()
    print(x[0:4])
    test = transform(DTE, x[0:4], x[-1])
    print(test)
    print(1-calc_accuracy(test,LTE))