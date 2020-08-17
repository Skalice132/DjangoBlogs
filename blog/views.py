from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from .models import Post, Tag
import random
from .scrapping import jobs
from django.contrib import messages

quotes = [  "Эффект обычно длится недолго, поскольку люди снова становятся теми, кем были прежде, то есть возвращаются к старому состоянию своего бытия. В данном случае каждый из пациентов с болезнью Паркинсона вернулся домой и увидел свою сиделку и свою супругу, уснул в той же самой кровати, съел ту же самую пищу и, может быть, сыграл в шахматы с теми же самыми друзьями, которые жаловались на свои болячки, – поэтому все это прежнее окружение напомнило ему прежнюю личность и прежнее состояние бытия.",
            "Если ты помнишь, наступил момент, когда ты, вероятно, сказал самому себе: «Мне наплевать, как я себя чувствую [тело]! Не важно, что там происходит в моей жизни [внешнее окружение]! Мне все равно, сколько времени это займет [время]! Я доведу это до конца!",
            "И тут твоя кожа вмиг покрылась мурашками. А все потому, что ты перешел в измененное состояние бытия. В тот момент, когда ты почувствовал эту энергию, ты посылал своему телу новую информацию.",
            "Вера – это попросту расширенное состояние бытия. По существу, убеждения – это мысли и чувства (установка), которые ты снова и снова продолжаешь думать и чувствовать, пока жестко не свяжешь их в своем мозге и эмоционально не обусловишь рефлексами своего тела. Можно сказать, что ты попадаешь в зависимость от них, из-за чего их так трудно изменить. Кроме того, тебе не нравится, когда их кто-нибудь оспаривает. Поскольку опыт впечатан в твой мозг и химически воплощен в эмоциях, большая часть твоих убеждений основана на прошлом опыте.",
            "Что такое медитация? Подобно гипнозу, медитация – это еще один способ обойти критикующий ум и войти в подсознательную систему программ. Медитация призвана вывести осознание за пределы аналитического ума – переключить внимание человека с внешнего мира и времени на мир внутренний.Понятие «медитация» окружено множеством мифов.",
            "Если, обладая ясным намерением, ты сумел ощутить принятие будущего и благодарность, значит, ты уже начинаешь осуществлять это событие эмоционально. Ты изменяешь свой мозг и тело. Можно сказать, что ты пребываешь в новом будущем прямо сейчас.",
            "Ты борешься изо всех сил, норовя любой ценой добиться результата, не понимая, что на самом деле отдаляешь его. Все это вышибает тебя из равновесия, совсем как эмоции выживания и потребления, и чем больше твое отчаяние и сильней раздражение, тем дальше ты отходишь от равновесия."
]

toposts = Post.objects.all()[:3]

class ShowPostView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'post'
    ordering = ['-date']
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(ShowPostView, self).get_context_data(**kwargs)
        ctx['title'] = 'Главная страница блога'
        ctx['titlepage'] = 'Страница c постами'
        ctx['toposts'] = toposts
        ctx['date'] = timezone.now
        ctx['a'] = random.choice(quotes)
        ctx['b'] = random.choice(quotes)

        return ctx


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/news_delete.html'
    success_url = '/'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False


class UserAllPostView(ListView):
    model = Post
    template_name = 'blog/user_news.html'
    context_object_name = 'post'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('date')

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(UserAllPostView, self).get_context_data(**kwargs)
        ctx['title'] = f'Все статьи польователя{ self.kwargs.get("username") }'
        ctx['titlepage'] = f'Статьи автора: { self.kwargs.get("username") }'
        ctx['toposts'] = toposts
        ctx['date'] = timezone.now
        ctx['a'] = random.choice(quotes)
        ctx['b'] = random.choice(quotes)
        return ctx


class TagAllPostView(ListView):
    model = Post
    template_name = 'blog/tag_news.html'
    paginate_by = 4

    def get_queryset(self):
        tags = get_object_or_404(Post, tags=self.kwargs.get('tags'))
        return Post.objects.filter(tags=tags)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(TagAllPostView, self).get_context_data(**kwargs)
        ctx['title'] = f'Все статьи по тегу{ self.kwargs.get("name") }'
        ctx['titlepage'] = f'Страница c тегом { self.kwargs.get("name") }'
        ctx['toposts'] = toposts
        ctx['date'] = timezone.now
        ctx['a'] = random.choice(quotes)
        ctx['b'] = random.choice(quotes)
        return ctx


class DetailPostView(DetailView):
    model = Post
    template_name = 'blog/news_detail.html'
   #context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(DetailPostView, self).get_context_data(**kwargs)
        ctx['title'] = Post.objects.filter(pk=self.kwargs['pk']).first()
        # ctx['titlepage'] = f'Выбрана {str(ctx["title"]).lower()}'
        ctx['toposts'] = toposts
        ctx['date'] = timezone.now
        ctx['a'] = random.choice(quotes)
        ctx['b'] = random.choice(quotes)
        return ctx


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/news_form.html'
   #context_object_name = 'post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(UpdatePostView, self).get_context_data(**kwargs)
        ctx['title'] = Post.objects.filter(pk=self.kwargs['pk']).first()
        # ctx['titlepage'] = f'Выбрана {str(ctx["title"]).lower()}'
        ctx['toposts'] = toposts
        ctx['date'] = timezone.now
        ctx['a'] = random.choice(quotes)
        ctx['b'] = random.choice(quotes)
        return ctx

class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'text','tags']
    template_name = 'blog/news_form.html'
   #context_object_name = 'post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CreatePostView, self).get_context_data(**kwargs)
        ctx['title'] = 'Создать новою новость'
        ctx['titlepage'] = 'Страница нового поста'
        ctx['toposts'] = toposts
        ctx['date'] = timezone.now
        ctx['a'] = random.choice(quotes)
        ctx['b'] = random.choice(quotes)
        return ctx

def progress(request):
    return render(request,'blog/progress.html', {
        'title': 'Обучение',
        'titlepage': 'Страница прогресса обучения',
        'toposts': toposts,
        'a': random.choice(quotes),
        'b': random.choice(quotes),
        'date': timezone.now
    })

def feedback(request):
    form = (request.POST or None)
    feedback_respond = ''
    if request.method == 'POST':
        print(request.POST)
        if form["feedback_text"] != '':
            send_mail(f'Обратная связь с сайта от {request.user}',
                  f'{form["feedback_text"]}\n\t\nС уважением, {request.user}. '
                  f'\n{feedback_respond}Email: {form["feedback_email"]}',
                  'mojetmax@gmail.com', ['cheferock132@gmail.com'],
                  fail_silently=False)
            messages.warning(request, f'Спасибо за отзыв, {request.user}.')
        #     feedback_respond = 'Нужно ответить на '
        else:
             messages.warning(request, f'Поля остались пустые. {request.user}, введите, пожалуйста, текст отзыва.')
        #     feedback_respond = 'Пользователь отказался от обратной связи. '



    return render(request,'blog/feedback.html', {
        'title': 'Обратная связь',
        'titlepage': 'Страница с обратной связью',
        'toposts': toposts,
        'a': random.choice(quotes),
        'b': random.choice(quotes),
        'date': timezone.now
        # 'post': post,
        # 'form': form,
        # 'sent': sent
    })

def vacancies(request):
    return render(request,'blog/vacancies.html', {
        'title': 'Доска объявлений',
        'titlepage': f'Страница с объявлениями({len(jobs)})',
        'toposts': toposts,
        'a': random.choice(quotes),
        'b': random.choice(quotes),
        'date': timezone.now,
        'vac': jobs
    })
