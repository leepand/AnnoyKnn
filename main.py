import annoy
import psutil
import numpy as np
from collections import Counter
class BaseANN(object):
    def use_threads(self):
        return True

    def done(self):
        pass

    def batch_query(self, X, n):
        res = []
        for q in X:
            res.append(self.query(q, n))
        return res

    def get_index_size(self, process):
        """Returns the size of the index in kB or -1 if not implemented."""
        return psutil.Process().memory_info().rss / 1024  # return in kB for backwards compatibility

    def fit(self, X):
        pass

    def query(self, q, n):
        return [] # array of candidate indices
class Annoy(BaseANN):
    def __init__(self, metric, n_trees, search_k):
        self._n_trees = n_trees
        self._search_k = search_k
        self._metric = metric
        self.name = 'Annoy(n_trees=%d, search_k=%d)' % (self._n_trees, self._search_k)

    def fit(self, X,len_X):
        self._annoy = annoy.AnnoyIndex(100, metric=self._metric)
        for i in xrange(len_X):#enumerate(X):
            v = [random.gauss(0, 1) for z in xrange(100)]
            self._annoy.add_item(i, v)
        self._annoy.build(self._n_trees)

    def query(self, v, n):
        return self._annoy.get_nns_by_vector(v, n, self._search_k,include_distances=True)
    def predict(self,X_test, y_train, k,threshold=0.8):
        # create list for distances and targets
        #y_train list的顺序与X_train row_index 一一对应
        distances = []
        targets = []
        cosine_list=[]
        cl=[]
        # sort the list
        item,distances = self.query(x, 10)
        '''return [(item1,cosin1),(item2,cosin2)...]'''
        neighbours_cosine_distances=zip(item, 1 - (np.array(distances) ** 2) / 2)
        '''make a list of the k neighbors' targets'''
        for i in range(k):
            index = item[i]
            cosine_dist=1-(distances[i]**2)/2.0#sqrt(2(1-cos(u,v)))
            if cosine_dist<threshold:
                continue
            targets.append(y_train[index])
            #print cosine_dist
            cosine_list.append(cosine_dist)
            cl.append(neighbours_cosine_distances[i])
        if len(targets)<1:
            return None
        top_item=Counter(targets).most_common(1)
        if  top_item[0][1] <2:
            top1=targets[0]
        else:
            top1=Counter(targets).most_common(1)[0][0]
        # return most common target
        return top1#Counter(targets).most_common(1),targets,'top1:',top1,cosine_list,cl#[0][0]
x = [random.gauss(0, 1) for z in xrange(100)]
l = [ i for i in range(100)]
metric, n_trees, search_k='angular',40,10
uu=Annoy(metric, n_trees, search_k)
print type(v)
uu.fit(10,100)
uu.query(x,10)
print uu.query(x,10),uu.predict(v,l,3,threshold=0.2)