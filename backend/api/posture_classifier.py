from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from scipy.spatial import distance
import heapq
import time


class KNNClassifier():
    def __init__(self):
        pass

    def fit(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def predict(self, x_test, k):
        if (k <= 0 or k is None):
            k = 1
        predictions = []
        for row in x_test:
            prediction = self.closest(row, k)
            predictions.append(prediction)
        return predictions

    def closest(self, row, k):
        # Use a max heap to store k closest points.
        max_heap = []
        for i in range(len(self.x_train)):
            dist = distance.euclidean(row, self.x_train[i])
            if (len(max_heap) < k):
                heapq.heappush(max_heap, (dist * -1, i))
                continue
            cmp_dist = max_heap[0][0] * -1
            if (dist < cmp_dist):
                heapq.heappop(max_heap)
                heapq.heappush(max_heap, (dist * -1, i))

        # take majority vote from k closest points
        tally, most_popular, count = {}, None, 0
        for dist, index in max_heap:
            label = self.y_train[index]
            tally[label] = tally.get(label, 0) + 1
            if (tally[label] > count):
                count = tally[label]
                most_popular = label

        return most_popular


def sensor_monitor(queue, state, bad_posture):
    features = []
    labels = []
    KNN_classifier = KNNClassifier()
    classifier_created = False
    started_sitting = time.time()
    cur_bad_posture = False
    bad_posture_start = None
    good_posture_start = None

    print("process started")

    while True:
        # callibrate good posture
        if state.value == 1:
            features.append(queue.get(block=True))
            labels.append(1)
        # callibrate bad posture
        elif state.value == 2:
            features.append(queue.get(block=True))
            labels.append(0)
        # predict
        elif state.value == 3:
            if (not classifier_created):
                print("classifier created")
                KNN_classifier.fit(features, labels)
                classifier_created = True

            item = queue.get(block=True)
            prediction = KNN_classifier.predict([item], k=4)
            # if predict bad posture
            if (prediction[0] == 0):
                if (cur_bad_posture):
                    if(bad_posture_start == None):
                        bad_posture_start = time.time()
                    elapsed = time.time() - bad_posture_start
                    if elapsed >= 3:
                        print("bad posture detected")
                        bad_posture.value = True
                else:
                    bad_posture_start = time.time()
                    cur_bad_posture = True
            else:
                if (cur_bad_posture):
                    good_posture_start = time.time()
                    cur_bad_posture = False
                else:
                    if (good_posture_start == None):
                        good_posture_start = time.time()
                    elapsed = time.time() - good_posture_start
                    if elapsed >= 3:
                        print("good posture detected")
                        bad_posture.value = False

        time.sleep(0.05)

