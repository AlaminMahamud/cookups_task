#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
#from rest_framework.views import APIView
from .models import Choice, Poll
from .serializers import ChoiceSerializer, PollSerializer

#class PollList(APIView):
#    def get(self, request):
#        polls = Poll.objects.all()
#        serializer = PollSerializer(polls, many=True)
#        return Response(serializer.data)
#        
#    def post(self):
#        pass

#class PollDetails(APIView):
#    def get(self, request, id):
#        polls = Poll.objects.all()
#        serializer = PollSerializer(polls, many=True)
#        return Response(serializer.data)
        
#    def post(self):
#        pass

@csrf_exempt
def poll_list(request):
    if (request.method == 'GET'):
            polls = Poll.objects.all()
            serializer = PollSerializer(polls, many=True)
            return JsonResponse(serializer.data, safe=False)

    elif (request.method == 'POST'):
        data = JSONParser().parse(request)
        serializer = PollSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def poll_detail(request, pk):
    """
    Retrieve, update or delete a code poll.
    """
    try:
        poll = Poll.objects.get(pk=pk)
    except Poll.DoesNotExist:
        return HttpResponse(status=404)

    if (request.method == 'GET'):
        serializer = PollSerializer(poll)
        return JsonResponse(serializer.data)

    elif (request.method == 'PUT'):
        data = JSONParser().parse(request)
        serializer = PollSerializer(poll, data=data)
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif (request.method == 'DELETE'):
        poll.delete()
        return HttpResponse(status=204)


#filtering-can't figure out to implement    
class PollList(generics.ListCreateAPIView):
    model = Poll
    serializer_class = PollSerializer
        
    def get_queryset(self):
        queryset = Poll.objects.all()
        
        workspace = self.request.query_params.get('workspace')
        airline = self.request.query_params.get('airline')

        if workspace:
            queryset = queryset.filter(workspace_id=workspace)
        elif airline:
            queryset = queryset.filter(workspace__airline_id=airline)

        return queryset
    
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.all()[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
