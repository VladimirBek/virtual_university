from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status, response
from rest_framework.filters import OrderingFilter

from main.models import Course, Lesson, Payment
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from main.servises import checkout_session, create_payment


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet for the Course class. """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListAPI(generics.ListAPIView):
    """ View for getting all lessons. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPI(generics.RetrieveAPIView):
    """ View for getting one lesson. """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPI(generics.CreateAPIView):
    """ View for creating one lesson. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPI(generics.UpdateAPIView):
    """ View for updating one lesson. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPI(generics.DestroyAPIView):
    """ View for deleting one lesson. """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class PaymentListView(generics.ListAPIView):
    """ View for getting all payments. """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson')
    ordering_fields = ['payment_date']


class PaymentCreateView(generics.CreateAPIView):
    """ View for creating one payment. """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = checkout_session(
            course=serializer.validated_data['course'],
            user=self.request.user
        )
        serializer.save()
        create_payment(course=serializer.validated_data['course'],
                       user=self.request.user,
                       session=session)
        return response.Response(session['id'], status=status.HTTP_201_CREATED)
