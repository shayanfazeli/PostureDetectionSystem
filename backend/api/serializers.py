from rest_framework import serializers
from .models import *

class HistogramSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Histogram
		fields = ('start', 'end', 'is_bad_posture')
