import math
import numpy as np
import pandas as pd
from io import BytesIO
from uuid import uuid4
from django.db import models
from django.core.files.base import ContentFile


from utils.generate_certificate import generate_certificate

from users.models import User


TEST_TYPE = (
    ("single", "Bitta javob tanlanadigan"),
    ("multiple", "Ko'p javob tanlanadigan"),
    ("matchable", "Moslashtiriladigan"),
    ("writable", "Javob yoziladigan"),
)
RESULT_TYPE = (
    ("calculating", "Hisoblanmoqda"),
    ("failed", "Yiqilgan"),
    ("passed", "O'tgan"),
)
CEFR_DEGREE_TYPE = (
    ("A", "A"),
    ("A+", "A+"),
    ("B", "B"),
    ("B+", "B+"),
    ("C", "C"),
    ("C+", "C+"),
    ("D", "D"),
    ("D+", "D+"),
    ("F", "F"),
    ("F+", "F+"),
    ("nc", "Hisoblanmagan"),
)
RASH_STATUS = (
    ("done", "Hisoblangan"),
    ("waiting", "Hisoblanmoqda"),
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(
        User, related_name="dtm_participants", blank=True
    )
    price = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    passing_score = models.DecimalField(max_digits=10, decimal_places=2)

    created = models.DateTimeField(auto_now_add=True)
    started = models.DateTimeField()
    ended = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DTM"
        verbose_name_plural = "DTM lar"


class Block(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dtm = models.ForeignKey(Dtm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ball = models.DecimalField(decimal_places=2, max_digits=10, default=1.1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DTM blok"
        verbose_name_plural = "DTM bloklar"


class Test(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    participants = models.ManyToManyField(
        User, related_name="cefr_participants", blank=True
    )
    is_public = models.BooleanField(default=False)
    passing_score = models.DecimalField(max_digits=10, decimal_places=2)
    is_calculated = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    started = models.DateTimeField()
    ended = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CEFR"
        verbose_name_plural = "CEFR lar"


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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


class Banner(models.Model):
    description = models.TextField(null=True, blank=True)
    dtm = models.ForeignKey(
        Dtm, on_delete=models.SET_NULL, default=None, null=True, blank=True
    )
    cefr = models.ForeignKey(
        Cefr, on_delete=models.SET_NULL, default=None, null=True, blank=True
    )
    image = models.ImageField(upload_to="images/banners", null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.description)

    class Meta:
        verbose_name = "E'lon"
        verbose_name_plural = "E'lonlar"


class DTMResult(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="dtm_result_teacher"
    )
    dtm = models.ForeignKey(Dtm, on_delete=models.CASCADE)
    cases = models.JSONField(default=dict)
    points = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=RESULT_TYPE)
    answers_sheet = models.FileField(upload_to="answers_sheets", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.status)

    class Meta:
        verbose_name = "DTM natija"
        verbose_name_plural = "DTM natijalar"


class CEFRResult(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cefr_result_teacher"
    )
    cefr = models.ForeignKey(Cefr, on_delete=models.CASCADE)
    cases = models.JSONField(default=dict)
    correct_answers = models.IntegerField(default=0)
    ratio_of_total_questions = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    according_to_the_answers_found = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    deviation = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    by_difficulty_level = models.DecimalField(
        max_digits=10, decimal_places=5, default=0
    )
    rash = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    percentage = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    degree = models.CharField(max_length=5, choices=CEFR_DEGREE_TYPE, default="nc")
    status = models.CharField(max_length=20, choices=RESULT_TYPE, null=True, blank=True)
    certificate = models.FileField(upload_to="certificates", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.status)

    class Meta:
        verbose_name = "CEFR natija"
        verbose_name_plural = "CEFR natijalar"


class Rash(models.Model):
    cefr = models.ForeignKey(Cefr, on_delete=models.CASCADE)
    file = models.FileField(upload_to="rash/results", null=True, blank=True)
    status = models.CharField(max_length=10, choices=RASH_STATUS, default="waiting")

    def __str__(self):
        return self.cefr.name

    def save(self, *args, **kwargs):
        if self.status != "done":
            results = CEFRResult.objects.filter(cefr=self.cefr)
            raw = {}
            for result in results:
                raw[
                    f"{result.author.first_name} {result.author.last_name} {result.author.phone}"
                ] = result.cases

            df = pd.DataFrame(raw).T
            df.columns = df.columns.astype(int)
            df = df.reindex(sorted(df.columns), axis=1)

            question_cols = [c for c in df.columns if isinstance(c, int)]

            df["correct_answers"] = df[question_cols].sum(axis=1).astype(int)
            df["ratio_of_total_questions"] = (df["correct_answers"] / 43) * 100
            df["according_to_the_answers_found"] = (df["correct_answers"] / 42) * 100

            mean_val = df["correct_answers"].mean()
            std_val = df["correct_answers"].std(ddof=1)
            df["deviation"] = (
                0 if std_val == 0 else (df["correct_answers"] - mean_val) / std_val
            )

            avg_per_q = df.loc[:, question_cols].mean(axis=0)

            def difficulty_fn(x):
                if x < 0.5:
                    return 3
                elif x <= 0.75:
                    return 2
                else:
                    return 1

            difficulty_row = pd.Series(np.nan, index=df.columns)
            difficulty_row.loc[question_cols] = (
                avg_per_q.apply(difficulty_fn).astype("Int64").values
            )

            df.loc["difficulty"] = difficulty_row

            difficulty_vals = df.loc["difficulty", question_cols]

            df["by_difficulty_level"] = df[question_cols].apply(
                lambda row: ((row == 1) * difficulty_vals).sum(), axis=1
            )

            df["rash"] = (df["by_difficulty_level"] / 65) * 100

            def degree_fn(rash):
                if rash > 70:
                    return "A+"
                elif rash >= 65:
                    return "A"
                elif rash >= 60:
                    return "B+"
                elif rash >= 55:
                    return "B"
                elif rash >= 50:
                    return "C+"
                elif rash >= 46:
                    return "C"
                else:
                    return "F"

            df["degree"] = df["rash"].apply(
                lambda x: degree_fn(x) if pd.notnull(x) else np.nan
            )

            df.loc["difficulty", ["by_difficulty_level", "rash", "degree"]] = np.nan

            df = df.sort_values(by="correct_answers", ascending=False)

            correct_answers = df["correct_answers"].to_dict()
            ratio_of_total_questions = df["ratio_of_total_questions"].to_dict()
            according_to_the_answers_founds = df[
                "according_to_the_answers_found"
            ].to_dict()
            deviations = df["deviation"].to_dict()
            by_difficulty_levels = df["by_difficulty_level"].to_dict()
            rashs = df["rash"].to_dict()
            degrees = df["degree"].to_dict()

            for (
                correct_answer,
                ratio_of_total_question,
                according_to_the_answers_found,
                deviation,
                by_difficulty_level,
                rash,
                degree,
            ) in zip(
                correct_answers,
                ratio_of_total_questions,
                according_to_the_answers_founds,
                deviations,
                by_difficulty_levels,
                rashs,
                degrees,
            ):
                phone = correct_answer.split(" ")[-1]
                student = User.objects.filter(phone=phone)

                if student:
                    student = student.first()
                    cefr_result = CEFRResult.objects.filter(
                        cefr=self.cefr, author=student
                    )

                    if cefr_result:
                        cefr_result = cefr_result.first()

                        percentage = ((rashs[rash] if not math.isnan(rashs[rash]) else 1) / 65) * 100 if (rashs[rash] if not math.isnan(rashs[rash]) else 0) < 65 else 100 

                        cefr_result.correct_answers = correct_answers[correct_answer]
                        cefr_result.ratio_of_total_questions = (
                            ratio_of_total_questions[ratio_of_total_question]
                            if not math.isnan(
                                ratio_of_total_questions[ratio_of_total_question]
                            )
                            else 0
                        )
                        cefr_result.according_to_the_answers_found = (
                            according_to_the_answers_founds[
                                according_to_the_answers_found
                            ]
                            if not math.isnan(
                                according_to_the_answers_founds[
                                    according_to_the_answers_found
                                ]
                            )
                            else 0
                        )
                        cefr_result.deviation = (
                            deviations[deviation]
                            if not math.isnan(deviations[deviation])
                            else 0
                        )
                        cefr_result.by_difficulty_level = (
                            by_difficulty_levels[by_difficulty_level]
                            if not math.isnan(by_difficulty_levels[by_difficulty_level])
                            else 0
                        )
                        cefr_result.rash = (
                            rashs[rash] if not math.isnan(rashs[rash]) else 0
                        )
                        cefr_result.degree = degrees[degree]

                        cefr_result.percentage = percentage

                        cefr_result.certificate.save(
                            f"{cefr_result.author.first_name} {cefr_result.author.last_name}.pdf",
                            ContentFile(
                                generate_certificate(
                                    logo="bgless.png",
                                    first_name=cefr_result.author.first_name,
                                    last_name=cefr_result.author.last_name,
                                    middle_name=cefr_result.author.middle_name,
                                    phone=cefr_result.author.phone,
                                    photo="bgless.png",
                                    id=str(cefr_result.cefr.uuid),
                                    subject=cefr_result.cefr.subject.name,
                                    points="%.2f" % cefr_result.rash,
                                    percentage="%.2f"
                                    % cefr_result.percentage,
                                    degree=cefr_result.degree,
                                    date=cefr_result.created.strftime("%d/%m/%Y"),
                                    director="Sanjar Sultonov",
                                ),
                                f"{cefr_result.author.first_name} {cefr_result.author.last_name}.pdf",
                            ),
                            save=False,
                        )

                        cefr_result.save()

            excel_buffer = BytesIO()
            df.to_excel(excel_buffer)
            excel_buffer.seek(0)

            self.file.save("results.xlsx", ContentFile(excel_buffer.read()), save=False)
            self.status = "done"

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "RASH"
        verbose_name_plural = "RASH"
