from django.db import models


class Feature(models.Model):
    name = models.TextField()


class Feedback(models.Model):
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name="feedback"
    )
    comment = models.TextField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="feedback"
    )


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#000000")
    feature = models.ManyToManyField(Feature, related_name="tags")
