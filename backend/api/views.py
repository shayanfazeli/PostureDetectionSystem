from .models import Histogram
from .serializers import HistogramSerializer
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
import time
import logging
import ast
from .process_handler import ProcessHandler
import atexit

logger = logging.getLogger(__name__)
processHandler = ProcessHandler()
processHandler.init()
processHandler.start()
atexit.register(processHandler.terminate)

def index(request):
	return HttpResponse("api index")

class HistogramViewSet(viewsets.ModelViewSet):
	queryset = Histogram.objects.all().order_by('start')
	serializer_class = HistogramSerializer

	@list_route(url_name='in_range', url_path='in_range/(?P<start>.+)/(?P<end>.+)')
	def in_range(self, request, start=None, end=None):
		try:
			qstart = parse_datetime(start)
			qend = parse_datetime(end)
			histograms = Histogram.objects.filter(start__lte=qend, end__gte=qstart).order_by('start')
			serializer = self.get_serializer(histograms, many=True)
			return Response(serializer.data)
		except Exception as e:
			return HttpResponse("unable to parse  {} --- {}</br>error: {}".format(start, end, e))

class FileUploadView(APIView):
	parser_classes = (FileUploadParser,)

	def put(self, request, format=None):
		file_obj = request.data['file']
		with open('/home/armin/Git/FYDP/uploads/{}'.format(file_obj.name), 'wb+') as dest:
			for chunk in file_obj.chunks():
				dest.write(chunk)


		return Response(status=204)

class SensorDataUploadView(APIView):
	def post(self, request, format=None):
		processHandler.add_sensor_data(ast.literal_eval(request.data['sensor_data']))
		return HttpResponse("Sensor data added successfuly.")

class NotifyView(APIView):
	def post(self, request, id, format=None):
		try:
			if int(id) == 0:
				processHandler.notify_bad_posture()
			else:
				processHandler.notify_sitting_too_long()
			return Response(status=200)
		except ValueError:
			return Response(status=400)






