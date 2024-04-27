from decimal import Decimal
from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    DecimalField,
    DurationField,
    SET_NULL,
)
import pgtrigger
from base.models import BaseModel
from user.models import User


class Course(BaseModel):
    title = CharField(max_length=255, db_index=True, null=True, blank=True)
    description = TextField(null=True, blank=True)
    instructor = ForeignKey(
        User, on_delete=SET_NULL, null=True, related_name="instructed_course"
    )
    duration = DurationField(null=True, blank=True)
    price = DecimalField(
        max_digits=19, decimal_places=4, default=Decimal("0.00"), null=True, blank=True
    )

    class Meta:
        db_table = "course"
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        triggers = [
            pgtrigger.Protect(
                name="is_instructor",
                condition=pgtrigger.Q(instructor__is_instructor=True),
                operation=[pgtrigger.Update, pgtrigger.Insert],
            )
        ]

    def __str__(self):
        return self.name
