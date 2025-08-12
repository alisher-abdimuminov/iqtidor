from django.http import HttpRequest
from rest_framework import serializers


from .models import (
    Answer,
    Block,
    Dtm,
    Subject,
    Test,
    Cefr,
    Question,
    QuestionAnswer,
    Banner,
    DTMResult,
    CEFRResult,
)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "count_cefrs",
        )


class AnswerSerializerer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "value_1",
            "value_2",
            "image",
            "is_correct",
        )


class TestSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField("get_answers")

    def get_answers(self, obj: Test):
        answers = Answer.objects.filter(test=obj)
        return AnswerSerializerer(answers, many=True).data

    class Meta:
        model = Test
        fields = (
            "question",
            "image",
            "type",
            "answers",
        )


class BlockSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    tests = serializers.SerializerMethodField("get_tests")

    def get_tests(self, obj: Block):
        tests = Test.objects.filter(block=obj)
        return TestSerializer(tests, many=True).data

    class Meta:
        model = Block
        fields = (
            "id",
            "dtm",
            "name",
            "subject",
            "tests",
            "ball",
        )


class DtmSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField("get_blocks")
    is_open = serializers.SerializerMethodField("get_is_open")
    is_solved = serializers.SerializerMethodField("get_is_solved")

    def get_blocks(self, obj: Dtm):
        blocks = Block.objects.filter(dtm=obj)
        return BlockSerializer(blocks, many=True).data

    def get_is_open(self, obj: Dtm):
        request: HttpRequest = self.context.get("request")
        if obj.participants.all().contains(request.user):
            return True
        return False

    def get_is_solved(self, obj: Dtm):
        request: HttpRequest = self.context.get("request")
        dtm_result = DTMResult.objects.filter(author=request.user, dtm=obj)

        if dtm_result:
            return True
        return False

    class Meta:
        model = Dtm
        fields = (
            "id",
            "name",
            "price",
            "created",
            "started",
            "ended",
            "blocks",
            "is_open",
            "is_solved",
            "is_public",
        )


class DtmsSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField("get_is_open")
    result = serializers.SerializerMethodField("get_result")

    def get_is_open(self, obj: Dtm):
        request: HttpRequest = self.context.get("request")
        if obj.participants.all().contains(request.user):
            return True
        return False

    def get_result(self, obj: Dtm):
        request = self.context.get("request")
        result = DTMResult.objects.filter(dtm=obj, author=request.user)

        if result:
            result = result.first()
            return DTMResultSerializer(result).data
        return None

    class Meta:
        model = Dtm
        fields = (
            "id",
            "name",
            "price",
            "created",
            "started",
            "ended",
            "is_open",
            "result",
            "is_public",
        )


# cefr
class QuestionAnswerSerializerer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = (
            "value_1",
            "value_2",
            "image",
            "is_correct",
        )


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField("get_answers")

    def get_answers(self, obj: Question):
        answers = QuestionAnswer.objects.filter(question=obj)
        return QuestionAnswerSerializerer(answers, many=True).data

    class Meta:
        model = Question
        fields = (
            "question",
            "image",
            "type",
            "answers",
        )


class CefrSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField("get_questions")
    is_open = serializers.SerializerMethodField("get_is_open")
    result = serializers.SerializerMethodField("get_result")

    def get_questions(self, obj: Cefr):
        questions = Question.objects.filter(cefr=obj)
        return QuestionSerializer(questions, many=True).data

    def get_is_open(self, obj: Dtm):
        request: HttpRequest = self.context.get("request")
        if obj.participants.all().contains(request.user):
            return True
        return False

    def get_result(self, obj: Cefr):
        request: HttpRequest = self.context.get("request")
        result = CEFRResult.objects.filter(cefr=obj, author=request.user)

        if result:
            result = result.first()
            return CEFRResultSerializer(result).data
        return None

    class Meta:
        model = Dtm
        fields = (
            "id",
            "name",
            "price",
            "created",
            "started",
            "ended",
            "questions",
            "is_open",
            "result",
            "is_public",
        )


class BannerSerializer(serializers.ModelSerializer):
    dtm = serializers.SerializerMethodField()
    cefr = serializers.SerializerMethodField()

    def get_dtm(self, obj: Banner):
        request = self.context.get("request")
        dtm = obj.dtm
        if dtm:
            return DtmsSerializer(dtm, context={ "request": request }).data
        return None
    
    def get_cefr(self, obj: Banner):
        request = self.context.get("request")
        cefr = obj.cefr
        if cefr:
            return CefrsSerializer(cefr, context={ "request": request }).data
        return None
    
    class Meta:
        model = Banner
        fields = (
            "id",
            "image",
            "dtm",
            "cefr",
            "is_active",
        )


class CefrsSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField("get_is_open")
    result = serializers.SerializerMethodField("get_result")

    def get_is_open(self, obj: Cefr):
        request: HttpRequest = self.context.get("request")
        if obj.participants.all().contains(request.user):
            return True
        return False

    def get_result(self, obj: Cefr):
        request: HttpRequest = self.context.get("request")
        print("req", request)
        result = CEFRResult.objects.filter(cefr=obj, author=request.user)

        if result:
            result = result.first()
            return CEFRResultSerializer(result).data
        return None

    class Meta:
        model = Cefr
        fields = (
            "id",
            "subject",
            "name",
            "price",
            "created",
            "started",
            "ended",
            "is_open",
            "result",
            "is_public",
        )


class DTMResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DTMResult
        fields = (
            "dtm",
            "points",
            "status",
            "answers_sheet",
        )


class CEFRResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CEFRResult
        fields = (
            "cefr",
            "rash",
            "degree",
            "status",
            "certificate",
        )
