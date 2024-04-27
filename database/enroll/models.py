from django.db.models import ForeignKey, CASCADE
import pgtrigger

from base.models import BaseModel
from course.models import Course
from user.models import User


class Enrollment(BaseModel):
    course = ForeignKey(Course, on_delete=CASCADE, related_name="enrolled_users")
    student = ForeignKey(User, on_delete=CASCADE, related_name="enrolled_courses")

    class Meta:
        db_table = "enrollment"
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"
        # triggers = [
        #     pgtrigger.Protect(
        #         name="unique_enrollment",
        #         condition=pgtrigger.Condition(
        #             """
        #             BEGIN
        #                 SELECT is_student
        #                 FROM student
        #                 WHERE id = NEW.student_id
        #                 AND is_student = TRUE;

        #                 IF NOT FOUND THEN
        #                     RAISE EXCEPTION 'enrollment already exists';
        #                 END IF;

        #                 RETURN NEW;
        #             END;
        #             """
        #         ),
        #         operation=[pgtrigger.Update, pgtrigger.Insert],
        #     )
        # ]

    def __str__(self):
        return self.user
