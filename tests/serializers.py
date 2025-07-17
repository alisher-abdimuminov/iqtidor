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
)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name", )


class AnswerSerializerer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("value_1", "value_2", "image", "is_correct", )


class TestSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField("get_answers")

    def get_answers(self, obj: Test):
        answers = Answer.objects.filter(test=obj)
        return AnswerSerializerer(answers, many=True).data

    class Meta:
        model = Test
        fields = ("question", "image", "type", "answers", )


class BlockSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    tests = serializers.SerializerMethodField("get_tests")

    def get_tests(self, obj: Block):
        tests = Test.objects.filter(block=obj)
        return TestSerializer(tests, many=True).data
    
    class Meta:
        model = Block
        fields = ("id", "dtm", "name", "subject", "tests", )


class DtmSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField("get_blocks")
    is_open = serializers.SerializerMethodField("get_is_open")

    def get_blocks(self, obj: Dtm):
        blocks = Block.objects.filter(dtm=obj)
        return BlockSerializer(blocks, many=True).data
    
    def get_is_open(self, obj: Dtm):
        request: HttpRequest = self.context.get("request")
        if obj.participants.all().contains(request.user):
            return True
        return False
    
    class Meta:
        model = Dtm
        fields = ("id", "name", "created", "started", "ended", "blocks", "is_open", "is_public", )



class DtmsSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField("get_is_open")

    def get_is_open(self, obj: Dtm):
        request: HttpRequest = self.context.get("request")
        if obj.participants.all().contains(request.user):
            return True
        return False
        
    class Meta:
        model = Dtm
        fields = ("id", "name", "created", "started", "ended", "is_open", "is_public", )

# cefr
class QuestionAnswerSerializerer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ("value_1", "value_2", "image", "is_correct", )


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField("get_answers")

    def get_answers(self, obj: Question):
        answers = QuestionAnswer.objects.filter(question=obj)
        return QuestionAnswerSerializerer(answers, many=True).data

    class Meta:
        model = Question
        fields = ("question", "image", "type", "answers", )


class CefrSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField("get_questions")
    is_open = serializers.SerializerMethodField("get_is_open")

    def get_questions(self, obj: Cefr):
        questions = Question.objects.filter(cefr=obj)
        return QuestionSerializer(questions, many=True).data

    def get_is_open(self, obj: Dtm):
        request: HttpRequest = self.context.get("request")
        if obj.participants.all().contains(request.user):
            return True
        return False
    
    class Meta:
        model = Dtm
        fields = ("id", "name", "created", "started", "ended", "questions", "is_open", "is_public", )


class CefrsSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField("get_is_open")

    def get_is_open(self, obj: Cefr):
        request: HttpRequest = self.context.get("request")
        if obj.participants.all().contains(request.user):
            return True
        return False
        
    class Meta:
        model = Cefr
        fields = ("id", "name", "created", "started", "ended", "is_open", "is_public", )
