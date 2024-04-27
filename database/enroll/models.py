from django.db.models import Q, ForeignKey, CASCADE, UniqueConstraint
import pgtrigger

from base.models import BaseModel
from course.models import Course
from user.models import User


class Enrollment(BaseModel):
    course = ForeignKey(
        Course, on_delete=CASCADE, related_name="enrolled_users"
    )
    student = ForeignKey(
        User, on_delete=CASCADE, related_name="enrolled_courses"
    )

    class Meta:
        db_table = "enrollment"
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"
        triggers = [
            pgtrigger.Protect(
                name="unique_enrollment",
                condition=pgtrigger.Q(student__is_student=True),
                operation=[pgtrigger.Update, pgtrigger.Insert],
            )
        ]

    def __str__(self):
        return self.user
