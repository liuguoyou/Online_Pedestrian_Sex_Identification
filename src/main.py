from os import listdir
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.datasets import fetch_lfw_people
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import RandomizedPCA
from sklearn.svm import LinearSVC
from datetime import datetime
import sys
import cv2
from array import array

class Data:
    def __init__(self):
        self.load()

    def load(self):

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        self.males = []
        for file in listdir('data/male'):
            gray = Image.open('data/male/'+file,'r')
            gray=gray.convert('L')
            gray=np.asarray(gray)
            try:
                (x,y,w,h) = face_cascade.detectMultiScale(gray, 1.3, 5)[0]
                face = gray[y:y+h, x:x+w]
                dim=cv2.resize(face, (100, 100), interpolation = cv2.INTER_AREA)
                self.males.append(np.array(dim))
                cv2.imwrite('data/cropped/male/'+file+'.jpg', dim)
            except:
                pass
                print 'male',file

        self.females = []
        for file in listdir('data/female'):
            gray = Image.open('data/female/'+file,'r')
            gray=gray.convert('L')
            gray=np.asarray(gray)
            try:
                (x,y,w,h) = face_cascade.detectMultiScale(gray, 1.3, 5)[0]
                face = gray[y:y+h, x:x+w]
                dim=cv2.resize(face, (100, 100), interpolation = cv2.INTER_AREA)
                self.females.append(np.array(dim))
                cv2.imwrite('data/cropped/female/'+file+'.jpg', dim)
            except:
                pass
                print 'female',file

def plot_gallery(images, titles, h, w, n_row=3, n_col=4):
    """Helper function to plot a gallery of portraits"""
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        plt.title(titles[i], size=12)
        plt.xticks(())
        plt.yticks(())
    plt.show()

class eF:
    def __init__(self,Data):
        self.load(Data)

    def load(self,Data):
        data_set = []
        data_set_labels = []
        for person in Data.males:
            data_set.append(person.flatten())
            data_set_labels.append(1)
        for person in Data.females:
            data_set.append(person.flatten())
            data_set_labels.append(-1)
        h,w=person.shape
        X_train, X_test, y_train, y_test = train_test_split(data_set, data_set_labels, test_size=0.01, random_state=datetime.now().second)

        n_components = 15

        self.pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X_train)
        X_train_pca = self.pca.transform(X_train)
        X_test_pca = self.pca.transform(X_test)
        eigenfaces = self.pca.components_.reshape((n_components, h, w))
        eigenface_titles = ["eigenface %d" % i for i in range(eigenfaces.shape[0])]
        #plot_gallery(eigenfaces, eigenface_titles, h, w)
        self.clf = LinearSVC()
        self.clf.fit(X_train_pca,y_train)
        s=self.clf.score(X_test_pca,y_test)
        print s

a=Data()
b=eF(a)