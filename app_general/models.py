from django.db import models

class Slide(models.Model):
    image = models.ImageField(upload_to='slides/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Slide {self.id}"




