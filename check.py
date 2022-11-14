import os
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

sentence = "Cybersecurity is also one of the significant challenges in the contemporary world, due to the complexity of information systems, both in terms of political usage and technology. Its primary goal is to ensure the system's dependability, integrity, and data privacy."

def load_data():
    X = list()
    y = list()
    ind = [ord(c) for c in sentence]
    ind_x = ind[:-1]
    ind_y = ind[1:]
    for file in os.listdir("db"):
        if file.endswith(".npy"):
            filepath = os.path.join("db", file)
            x = np.load(filepath)
            X.append(x[ind_x, ind_y])
            y.append(file)
    X = pd.DataFrame(X)
    y = pd.Series(y)
    return X, y

def select_file(y):
    for i, name in enumerate(y):
        print("%2d: %s" % (i, name))
    print()
    target = input("Select: ")
    while True:
        if target.isdigit() and 0 <= int(target) and int(target) < len(y):
            return int(target)
        elif target in y:
            return y[y == target].index[0]
        target = input("Select: ")

def train_test_split(X, y, ind):
    X_train = X.drop(ind)
    y_train = y.drop(ind)
    X_test = X.iloc[ind:ind + 1, :]
    return X_train, y_train, X_test

def predict(X_train, y_train, X_test, knn=KNeighborsClassifier(n_neighbors=1)):
    knn.fit(X_train, y_train)
    return knn.predict(X_test)

def main():
    X, y = load_data()
    cont = True
    while cont:
        print("Please select an identity file to find the nearest identification.")
        target_ind = select_file(y)
        X_train, y_train, X_test = train_test_split(X, y, target_ind)
        out = predict(X_train, y_train, X_test)
        print("Identified as:", out)
        inp = input("Continue? (y/n): ")
        while inp != 'y' and inp != 'n':
            inp = input("Continue? (y/n): ")
        cont = (inp == 'y')

if __name__ == "__main__":
    main()