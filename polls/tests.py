from django.test import TestCase
import datetime
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice, Voter
from django.contrib.auth.models import User


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text = question_text,pub_date = time)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days = 30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(),False)
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days = 1, seconds = 1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(),False)
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(),True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        question = create_question(question_text = "Past question.",days =-30)
        question.choice_set.create(choice_text = 'choice1', votes = 0)
        question.choice_set.create(choice_text = 'choice2', votes = 0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_future_question(self):
        question = create_question(question_text = "Future question.",days = 30)
        question.choice_set.create(choice_text = 'choice1', votes = 0)
        question.choice_set.create(choice_text = 'choice2', votes = 0)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        question1 = create_question(question_text = "Past question.",days = -30)
        question1.choice_set.create(choice_text = 'choice1.1', votes = 0)
        question1.choice_set.create(choice_text = 'choice1.2', votes = 0)
        question2 = create_question(question_text = "Future question.", days = 30)
        question2.choice_set.create(choice_text = 'choice2.1', votes = 0)
        question2.choice_set.create(choice_text = 'choice2.2', votes = 0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_two_past_questions(self):
        question1 = create_question(question_text = "Past question 1.", days = -30)
        question1.choice_set.create(choice_text = 'choice1.1', votes = 0)
        question1.choice_set.create(choice_text = 'choice1.2', votes = 0)
        question2 = create_question(question_text = "Past question 2.", days = -5)
        question2.choice_set.create(choice_text = 'choice2.1', votes = 0)
        question2.choice_set.create(choice_text = 'choice2.2', votes = 0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question 2.>','<Question: Past question 1.>'])

    def test_question_with_one_choice(self):
        question = create_question(question_text = "question", days = -5)
        question.choice_set.create(choice_text = 'choice', votes = 0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_question_with_no_choice(self):
        create_question(question_text = "question", days = -5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_question_with_multiple_choices(self):
        question = create_question(question_text = "question", days = -5)
        question.choice_set.create(choice_text = 'choice1', votes = 0)
        question.choice_set.create(choice_text = 'choice2', votes = 0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: question>'])

    def test_questions_with_choice_no_choice_and_multiple_choices(self):
        question1 = create_question(question_text = "question 1", days = -5)
        question1.choice_set.create(choice_text = 'choice1', votes = 0)
        question2 = create_question(question_text = 'question 2', days = -3)
        question2.choice_set.create(choice_text = 'choice2.1', votes = 0)
        question2.choice_set.create(choice_text = 'choice2.2', votes = 0)
        create_question(question_text = "question 3", days = -2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: question 2>'])

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        future_question = create_question(question_text = 'Future question.', days = 5)
        future_question.choice_set.create(choice_text = 'choice1', votes = 0)
        future_question.choice_set.create(choice_text = 'choice2', votes = 0)
        url = reverse('polls:detail',args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        past_question = create_question(question_text = 'Past question.', days = -5)
        past_question.choice_set.create(choice_text = 'choice1', votes = 0)
        past_question.choice_set.create(choice_text = 'choice2', votes = 0)
        url = reverse('polls:detail',args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_question_with_one_choice(self):
        question = create_question(question_text = 'question',days = -5)
        question.choice_set.create(choice_text = 'choice',votes = 0)
        url = reverse('polls:detail',args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_question_with_no_choice(self):
        question = create_question(question_text = 'question',days = -5)
        url = reverse('polls:detail',args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_question_with_multiple_choices(self):
        question = create_question(question_text = "question",days = -3)
        question.choice_set.create(choice_text = 'choice1',votes = 0)
        question.choice_set.create(choice_text = 'choice2',votes = 0)
        url = reverse('polls:detail',args = (question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,question.question_text)

class QuestionResultsViewTests(TestCase):

    def test_future_question(self):
        future_question = create_question(question_text = 'Future question.', days = 5)
        future_question.choice_set.create(choice_text = 'choice1', votes = 0)
        future_question.choice_set.create(choice_text = 'choice2', votes = 0)
        url = reverse('polls:results',args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        past_question = create_question(question_text = 'Past question.', days = -5)
        past_question.choice_set.create(choice_text = 'choice1', votes = 0)
        past_question.choice_set.create(choice_text = 'choice2', votes = 0)
        url = reverse('polls:results',args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_question_with_one_choice(self):
        question = create_question(question_text = 'question',days = -5)
        question.choice_set.create(choice_text = 'choice',votes = 0)
        url = reverse('polls:results',args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_question_with_no_choice(self):
        question = create_question(question_text = 'question',days = -5)
        url = reverse('polls:results',args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_question_with_multiple_choices(self):
        question = create_question(question_text = "question",days = -3)
        question.choice_set.create(choice_text = 'choice1',votes = 0)
        question.choice_set.create(choice_text = 'choice2',votes = 0)
        url = reverse('polls:results',args = (question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,question.question_text)

class VoterDetailViewTests(TestCase):

    def test_user_votes_one_time(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        question = create_question(question_text="question", days=-3)
        question.choice_set.create(choice_text='choice1', votes=0)
        question.choice_set.create(choice_text='choice2', votes=0)
        response = self.client.post('/polls/1/vote/', {'choice':'1', })
        self.assertEqual(response.status_code,302)
        choice = Choice.objects.get(pk=1)
        self.assertEqual(choice.votes,1)

    def test_user_cant_double_vote(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        question = create_question(question_text="question", days=-3)
        question.choice_set.create(choice_text='choice1', votes=0)
        question.choice_set.create(choice_text='choice2', votes=0)
        response = self.client.post('/polls/1/vote/', {'choice':'1', })
        self.assertEqual(response.status_code,302)
        choice = Choice.objects.get(pk=1)
        self.assertEqual(choice.votes,1)
        v = Voter(user= User.objects.get(username='testuser'), question=question)
        v.save()
        response = self.client.post('/polls/1/vote/', {'choice': '1', })
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Sorry, but you have already voted.python ')



