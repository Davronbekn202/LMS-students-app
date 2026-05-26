from django.db import models

from accounts.models import CustomUser


class Course(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='courses/')
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Davomiyligi (oylarda)")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups')
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, related_name='groups')
    students = models.ManyToManyField('Student', related_name='groups', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.course.name})"


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='student', blank=True, null=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    # courses = models.ManyToManyField(Course, related_name='students', blank=True)

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='teacher', blank=True, null=True)
    phone = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Tajriba (yillarda)")
    courses = models.ManyToManyField(Course, related_name='teachers', blank=True)

    def __str__(self):
        return self.full_name


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='module')
    title = models.CharField(max_length=150)
    description = models.TextField()


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=300)
    description = models.TextField()


class Normative(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='normatives')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='lessons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ManyToManyField(Teacher, related_name='normatives', blank=True)

    def __str__(self):
        return f"{self.title}"


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Normative, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="assign_student")
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    is_checked = models.BooleanField(default=False)
    grade = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="assignment_submission", blank=True,
                                null=True)

    def __str__(self):
        return f"{self.text}"
