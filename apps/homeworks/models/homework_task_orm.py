from django.db import models


class HomeworkTaskOrm(models.Model):
    homework = models.ForeignKey(
        "homeworks.HomeworkOrm", on_delete=models.CASCADE, related_name="homework_tasks"
    )
    task = models.ForeignKey(
        "tasks.TaskOrm", on_delete=models.CASCADE, related_name="homework_tasks"
    )

    solution_file = models.FileField(
        upload_to="homework_solutions/",
        blank=True,
        null=True,
        help_text="Przesłane rozwiązanie (skan, zdjęcie, PDF, itd.).",
    )
    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Data przesłania rozwiązania przez ucznia.",
    )
