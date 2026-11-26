from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, CourseStatus
from enrollments.models import Enrollment, EnrollmentStatus
from students.models import Student


class BaseCourseTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='pass12345',
        )
        cls.course = Course.objects.create(
            name='Python',
            description='Основы Python',
            price=100,
            status=CourseStatus.DRAFT,
            author=cls.admin,
        )

    def setUp(self):
        self.client.force_authenticate(user=self.admin)


class CourseCreateTestCase(BaseCourseTestCase):

    def test_create_draft_course_success(self):
        response = self.client.post('/api/courses/', {
            'name': 'Django',
            'description': 'Веб-разработка',
            'price': 150,
            'status': CourseStatus.DRAFT,
            'author': self.admin.id,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Django')

    def test_cannot_create_published_without_price(self):
        response = self.client.post('/api/courses/', {
            'name': 'Bad',
            'description': 'Описание',
            'status': CourseStatus.PUBLISHED,
            'author': self.admin.id,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_cannot_create_published_without_description(self):
        response = self.client.post('/api/courses/', {
            'name': 'Bad2',
            'description': '',
            'price': 100,
            'status': CourseStatus.PUBLISHED,
            'author': self.admin.id,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)

    def test_can_create_published_with_all_fields(self):
        response = self.client.post('/api/courses/', {
            'name': 'Buba',
            'description': 'Полный курс',
            'price': 200,
            'status': CourseStatus.PUBLISHED,
            'author': self.admin.id,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], CourseStatus.PUBLISHED)

    def test_cannot_create_with_duplicate_name(self):
        response = self.client.post('/api/courses/', {
            'name': 'Python',
            'description': 'Дубль',
            'price': 100,
            'status': CourseStatus.DRAFT,
            'author': self.admin.id,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_cannot_create_published_with_negative_price(self):
        response = self.client.post('/api/courses/', {
            'name': 'Negative',
            'description': 'Описание',
            'price': -100,
            'status': CourseStatus.PUBLISHED,
            'author': self.admin.id,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_cannot_create_with_invalid_price_type(self):
        response = self.client.post('/api/courses/', {
            'name': 'StringPrice',
            'description': 'Описание',
            'price': 'not-a-number',
            'status': CourseStatus.DRAFT,
            'author': self.admin.id,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_anonymous_cannot_create_course(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/courses/', {
            'name': 'Anon',
            'description': 'Описание',
            'price': 100,
            'status': CourseStatus.DRAFT,
            'author': self.admin.id,
        }, format='json')

        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


class CourseRetrieveTestCase(BaseCourseTestCase):

    def test_retrieve_course(self):
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Python')

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get(f'/api/courses/{Course.objects.count()+1}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CourseUpdateTestCase(BaseCourseTestCase):

    def test_patch_change_name(self):
        response = self.client.patch(
            f'/api/courses/{self.course.id}/',
            {'name': 'Python 3'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Python 3')

    def test_cannot_change_price_with_active_enrollments(self):
        student = Student.objects.create_user(
            username='stu', password='pass12345', phone='12345678901'
        )
        Enrollment.objects.create(
            student=student,
            course=self.course,
            status=EnrollmentStatus.ACTIVE,
        )

        response = self.client.patch(
            f'/api/courses/{self.course.id}/',
            {'price': 999},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_change_price_without_enrollments(self):
        response = self.client.patch(
            f'/api/courses/{self.course.id}/',
            {'price': 250},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], 250)

    def test_patch_nonexistent_returns_404(self):
        response = self.client.patch(f'/api/courses/{Course.objects.count()+1}/',{'name': 'Ghost'},format='json',)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_patch_with_duplicate_name(self):
        Course.objects.create(
            name='Duplicated',
            description='d',
            price=10,
            status=CourseStatus.DRAFT,
            author=self.admin,
        )
        response = self.client.patch(
            f'/api/courses/{self.course.id}/',
            {'name': 'Duplicated'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)


class CourseDestroyTestCase(BaseCourseTestCase):

    def test_destroy_archived_not_deleted(self):
        response = self.client.delete(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.course.refresh_from_db()
        self.assertEqual(self.course.status, CourseStatus.ARCHIVED)

    def test_cannot_delete_course_with_active_enrollments(self):
        student = Student.objects.create_user(
            username='stu2', password='pass12345', phone='12345678902'
        )
        Enrollment.objects.create(
            student=student,
            course=self.course,
            status=EnrollmentStatus.ACTIVE,
        )

        response = self.client.delete(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_delete_archived_twice(self):
        self.client.delete(f'/api/courses/{self.course.id}/')
        response = self.client.delete(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_nonexistent_returns_404(self):
        response = self.client.delete(f'/api/courses/{Course.objects.count()+1}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CourseListTestCase(BaseCourseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.published1 = Course.objects.create(
            name='A', description='a', price=100,
            status=CourseStatus.PUBLISHED, author=cls.admin,
        )
        cls.published2 = Course.objects.create(
            name='B', description='b', price=500,
            status=CourseStatus.PUBLISHED, author=cls.admin,
        )
        cls.draft = Course.objects.create(
            name='C', description='c', price=300,
            status=CourseStatus.DRAFT, author=cls.admin,
        )

    def test_filter_by_status(self):
        response = self.client.get(
            f'/api/courses/?status={CourseStatus.PUBLISHED}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [c['name'] for c in response.data['results']]
        self.assertIn('A', names)
        self.assertNotIn('C', names)

    def test_filter_by_price_range(self):
        response = self.client.get('/api/courses/?price_min=100&price_max=400')
        names = [c['name'] for c in response.data['results']]
        self.assertIn('A', names)
        self.assertIn('C', names)
        self.assertNotIn('B', names)

    def test_search_by_name(self):
        response = self.client.get('/api/courses/?search=A')
        names = [c['name'] for c in response.data['results']]
        self.assertEqual(names, ['A'])

    def test_order_by_price_ascending(self):
        response = self.client.get('/api/courses/?ordering=price')
        prices = [c['price'] for c in response.data['results']]
        self.assertEqual(prices, sorted(prices))

    def test_order_by_price_descending(self):
        response = self.client.get('/api/courses/?ordering=-price')
        prices = [c['price'] for c in response.data['results']]
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_anonymous_list_forbidden(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)