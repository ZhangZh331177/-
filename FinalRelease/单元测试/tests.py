from django.test import TestCase
from .models import Student, Teacher, Manager

class ModelTestCase(TestCase):
    def setUp(self):
        # Create sample instances for testing
        self.student = Student.objects.create(
            name='John Doe',
            gender='m',
            grade=1,
            number='123456789012',
            email='john@example.com',
            password='securepwd'
        )

        self.teacher = Teacher.objects.create(
            name='Jane Smith',
            gender='f',
            number='987654321098',
            email='jane@example.com',
            password='anotherpwd'
        )

        self.manager = Manager.objects.create(
            name='Alice Johnson',
            gender='f',
            number='112233445566',
            email='alice@example.com',
            password='managerpwd'
        )

    def test_student_id(self):
        # Test if student ID is correctly returned
        self.assertEqual(self.student.get_id(), '123456789012')

    def test_student_number_length(self):
        # Test student number length validation
        invalid_student = Student(
            name='Invalid Student',
            gender='f',
            grade=1,
            number='12345',  # Invalid length
            email='invalid@example.com',
            password='pwd12345'
        )
        with self.assertRaises(Exception):
            invalid_student.full_clean()  # Ensure the validation error is raised

    def test_teacher_email(self):
        # Test teacher email field
        teacher = Teacher.objects.get(name='Jane Smith')
        self.assertEqual(teacher.email, 'jane@example.com')

    def test_manager_password_length_validation(self):
        # 测试管理员密码长度验证
        # 创建一个长度不合规的管理员对象，预期会引发 ValidationError 异常
        with self.assertRaises(ValidationError):
            invalid_manager = Manager(
                name='Invalid Manager',
                gender='m',
                number='9876543210',  # 无效长度
                email='invalid_manager@example.com',
                password='pwd'  # 无效长度
            )
            invalid_manager.full_clean()  # 确保引发验证错误

    def test_student_string_representation(self):
        # 测试学生模型的字符串表示形式是否符合预期
        self.assertEqual(str(self.student), "123456789012 (John Doe)")

    def test_teacher_number_uniqueness(self):
        # 测试教师的教职工号是否唯一
        # 创建一个已存在教职工号的教师对象，预期会引发 IntegrityError 异常
        with self.assertRaises(IntegrityError):
            duplicate_teacher = Teacher(
                name='Duplicate Teacher',
                gender='m',
                number='123456789012',  # 重复的教职工号
                email='duplicate@example.com',
                password='duplicatepwd'
            )
            duplicate_teacher.save()  # 确保引发完整性错误