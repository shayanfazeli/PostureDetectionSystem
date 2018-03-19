from multiprocessing import Process, Manager, Value
import time
from .notifier import notification_process, notify
# import posture_classifier.sensor_monitor
from api import posture_classifier
# from posture_classifier import sensor_monitor


#Place holders
def monitor_sensor_process(data_queue):
	pass
def monitor_camera_process():
	pass

class SensorData():
	def __init__(self, data):
		self.data = data
		self.ts = time.time()

class ProcessHandler():
	def __init__(self):
		manager = Manager()

		self.processes = []

		self.sensor_data_queue = manager.Queue(1000)
		self.bad_posture = Value('i', 0)
		self.sitting_too_long = Value('i', 0)
		self.state = Value('i', 0)


	def add_sensor_data(self, data):
		self.sensor_data_queue.put(SensorData(data))

	def notify_bad_posture(self):
		self.bad_posture.value = 1

	def notify_sitting_too_long(self):
		self.sitting_too_long.value = 1


	def init(self):
		self.processes = []
		self.processes.append(Process(target = posture_classifier.sensor_monitor, args = (self.sensor_data_queue, self.state, self.bad_posture)))
		self.processes.append(Process(target = monitor_camera_process))
		self.processes.append(Process(target = notification_process, args = (self.bad_posture, self.sitting_too_long)))

		features = []
		labels = []
		with open('posture_data.csv') as fp:
		   for cnt, line in enumerate(fp):
		       split = line.split(',')
		       label = split.pop(len(split) - 1)
		       for i in range(len(split)):
		           split[i] = int(split[i])
		       features.append(split)
		       labels.append(int(label))

		self.processes[0].start()

		print("main process 1")
		self.state.value = 1
		for i in range(len(features)):
			if(labels[i] != 1):
				break
			self.sensor_data_queue.put(features[i], False)
		while not self.sensor_data_queue.empty():
			print("queue not empty")
			time.sleep(1)
		print("main process 2")
		self.state.value = 2
		for j in range(i, len(features)):
			self.sensor_data_queue.put(features[j], False)
		while not self.sensor_data_queue.empty():
			print("queue not empty")
			time.sleep(1)
		print("main process 3")
		self.state.value = 3
		for i in range(len(features)):
			self.sensor_data_queue.put(features[i], False)
		while not self.sensor_data_queue.empty():
			print("queue not empty")
			time.sleep(1)
		




	def start(self):
		for process in self.processes:
			if not process.is_alive():
				process.daemon = True
				process.start()

	def terminate(self):
		for process in self.processes:
			process.terminate()






