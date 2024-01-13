from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status, response
from rest_framework.filters import OrderingFilter

from main.models import Course, Lesson, Payment, Subscription
from main.pagination import PaginationsCourse
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer, \
    SubscriptionCreateSerializer
from main.servises import checkout_session, create_payment
from users.permissions import IsModerator, IsOwner
from main.tasks import check_change_course

class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet for the Course class. """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwner, IsModerator]
    pagination_class = PaginationsCourse

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        updated_inctance = serializer.save(owner=self.request.user)
        updated_inctance.owner = self.request.user

        check_change_course.delay(instance.id, instance.updated_at, updated_inctance.updated_at)
        updated_inctance.save()




class LessonListAPI(generics.ListAPIView):
    """ View for getting all lessons. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator, IsOwner]
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
    permission_classes = [IsModerator, IsOwner]


class LessonCreateAPI(generics.CreateAPIView):
    """ View for creating one lesson. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator, IsOwner]


class LessonUpdateAPI(generics.UpdateAPIView):
    """ View for updating one lesson. """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class LessonDestroyAPI(generics.DestroyAPIView):
    """ View for deleting one lesson. """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


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
