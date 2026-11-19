from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
class Appointment(models.Model):
    def clean(self):
        super().clean()
        if self.appointment_date is None:
            return
        date_changed = True
        if not self._state.adding:
            old_date = Appointment.objects.filter(
                pk=self.pk
            ).values_list("appointment_date", flat=True).first()
            date_changed = old_date != self.appointment_date
            if date_changed and self.appointment_date <= timezone.now():
                raise ValidationError({
                    "appointment_date": "Le rendez-vous doit être futur."
                })
    class Meta:
        ordering = ["appointment_date"]
        constraints = [
        models.UniqueConstraint(
        fields=["doctor", "appointment_date"],
        name="unique_doctor_appointment_date"
        )
        ]        
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"
    reason = models.TextField()
    appointment_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
    max_length=9, choices=Status.choices,
    default=Status.PENDING
    )
    prescription = models.FileField(
upload_to="prescriptions/", blank=True,
validators=[FileExtensionValidator(["pdf"])]
)
    doctor = models.ForeignKey(
    "AccountApp.Doctor", on_delete=models.CASCADE
    )
    patient = models.ForeignKey(
    "AccountApp.Patient", on_delete=models.CASCADE
    )
