from django.db import models

class APIRequest(models.Model):
    url = models.CharField(max_length=500)
    method = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} - {self.url}"


class APIResult(models.Model):
    request = models.ForeignKey(APIRequest, on_delete=models.CASCADE)
    response = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    solution = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Result for {self.request.url}"