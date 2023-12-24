from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status, response
from rest_framework.filters import OrderingFilter

from main.models import Course, Lesson, Payment, Subscription
from main.pagination import PaginationsCourse
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer, \
    SubscriptionCreateSerializer
from main.servises import checkout_session, create_payment
from users.permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet for the Course class. """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModerator]
    pagination_class = PaginationsCourse

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)


class LessonListAPI(generics.ListAPIView):
    """ View for getting all lessons. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator]
    pagination_class = PaginationsCourse

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
    permission_classes = [IsModerator]


class LessonCreateAPI(generics.CreateAPIView):
    """ View for creating one lesson. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator]


class LessonUpdateAPI(generics.UpdateAPIView):
    """ View for updating one lesson. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator]


class LessonDestroyAPI(generics.DestroyAPIView):
    """ View for deleting one lesson. """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]


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


class SubscriptionList(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionCreate(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionCreateSerializer


class SubscriptionDelete(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
