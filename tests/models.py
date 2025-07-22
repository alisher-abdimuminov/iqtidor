from django.db import models

from users.models import User


TEST_TYPE = (
    ("single", "Bitta javob tanlanadigan"),
    ("multiple", "Ko'p javob tanlanadigan"),
    ("matchable", "Moslashtiriladigan"),
    ("writable", "Javob yoziladigan"),
)


class Subject(models.Model):
    name = models.CharField()
    
    def __str__(self):
        return self.name
    
    def count_cefrs(self):
        return Cefr.objects.filter(subject=self).count()
    
    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"

# dtm

class Dtm(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, related_name="dtm_participants", blank=True)
    is_public = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    started = models.DateTimeField()
    ended = models.DateTimeField()  

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "DTM"
        verbose_name_plural = "DTM lar"


class Block(models.Model):
    dtm = models.ForeignKey(Dtm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "DTM blok"
        verbose_name_plural = "DTM bloklar"
    

class Test(models.Model):
    question = models.TextField()
    image = models.ImageField(upload_to="images/tests", null=True, blank=True)
    type = models.CharField(max_length=10, choices=TEST_TYPE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = "DTM test"
        verbose_name_plural = "DTM testlar"


class Answer(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    value_1 = models.TextField()
    value_2 = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/answers", null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.test.question
    
    class Meta:
        verbose_name = "DTM test javob"
        verbose_name_plural = "DTM test javoblari"


# cefr
class Cefr(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="cefr_participants", blank=True)
    is_public = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    started = models.DateTimeField()
    ended = models.DateTimeField()  

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "CEFR"
        verbose_name_plural = "CEFR lar"


class Question(models.Model):
    question = models.TextField()
    image = models.ImageField(upload_to="images/tests", null=True, blank=True)
    type = models.CharField(max_length=10, choices=TEST_TYPE)
    cefr = models.ForeignKey(Cefr, on_delete=models.CASCADE)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = "CEFR savoli"
        verbose_name_plural = "CEFR savollari"


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value_1 = models.TextField()
    value_2 = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/answers", null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question.question
    
    class Meta:
        verbose_name = "CEFR savoli javobi"
        verbose_name_plural = "CEFR savoli javoblari"
