import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Post, Category
from django.core.mail import send_mail, EmailMessage
from submit.models import Profile
from .forms import PostForm, CategoryForm
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from .models import Competition, Submission
from .forms import CompetitionForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


def index(request):
    context = {
        'posts': Post.objects.all(),
        'categories': Category.objects.all(),  

    }
    return render(request, 'core/index.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'core/index.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = 'core/index.html'  
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if 'pk' in self.kwargs:
            category = Category.objects.get(pk=self.kwargs['pk'])
            return Post.objects.filter(category=category).order_by('-date_posted')
        else:
            return Post.objects.all().order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        if 'pk' in self.kwargs:
            context['selected_category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

class UserPostListView(LoginRequiredMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        profile = user.profile
        return redirect('user-posts', username=user.username)



class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object

        all_other_videos = Post.objects.filter(image__isnull=False).exclude(
            pk=post.pk)

        random_suggested_videos = random.sample(list(all_other_videos),
                                                min(6, len(all_other_videos)))

        context['random_suggested_videos'] = random_suggested_videos

        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'  

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category_form'] = CategoryForm()  
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        post_form = self.get_form()
        category_form = CategoryForm(request.POST, request.FILES)

        if 'submit_post' in request.POST:
            return self.handle_post_form(post_form)
        elif 'submit_category' in request.POST:
            return self.handle_category_form(category_form)

        return self.render_to_response(self.get_context_data(form=post_form, category_form=category_form))

    def handle_post_form(self, form):
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def handle_category_form(self, form):
        if form.is_valid():
            category = form.save()
            messages.success(self.request, 'New category has been created!')
            return redirect('post-create') 
        else:
            return self.render_to_response(self.get_context_data(category_form=form))

    def form_valid(self, form):
        user = self.request.user


        form.instance.author = user

        category_id = self.request.POST.get('category')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                form.instance.category = category
            except Category.DoesNotExist:
                messages.warning(self.request, 'Selected category does not exist.')
                return self.form_invalid(form)

        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content' ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def post_list(request):
    posts = Post.objects.all()


    context = {
        'posts': posts,
    }

    return render(request, 'core/index.html', context)


def competition_list(request):
    competitions = Competition.objects.all().order_by('-date_posted')
    form = CompetitionForm() if request.user.is_staff else None
    
    if request.method == 'POST' and request.user.is_staff:
        form = CompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Competition created successfully!')
            return redirect('competition_list')

    return render(request, 'core/competition_list.html', {
        'competitions': competitions,
        'form': form
    })


@login_required
def create_competition(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create competitions.')
        return redirect('competition_list')

    if request.method == 'POST':
        form = CompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Competition created successfully!')
            return redirect('competition_list')
    else:
        form = CompetitionForm()

    return render(request, 'core/create_competition.html', {'form': form})

def submit_entry(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    
    if request.method == 'POST':
        email = request.POST['email']
        content = request.POST['content']
        
        submission = Submission.objects.create(
            competition=competition,
            email=email,
            content=content
        )

        email_subject = f'Competition Submission Received: {competition.title}'
        email_body = f'Thank you for your submission to "{competition.description}":\n\nYour entry is: {submission.content}\n\nThank you for your participation. Winners will be announced soon.'

        email_message = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,  
            to=[email, settings.ADMIN_EMAIL],  
            headers={'Reply-To': email},  
        )
        email_message.send(fail_silently=False)

        
        try:
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,  
                [email], 
                fail_silently=False,
            )
        except Exception as e:
            
            print(f"Error sending email to client: {e}")

        
        messages.success(request, 'Your submission has been received!')
        return redirect('competition_list')
    
    messages.error(request, 'Invalid submission method.')
    return redirect('competition_list')


def subscribe(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.is_paid = True
        profile.save()
        messages.success(request, 'You have successfully subscribed to the paid plan!')
        return redirect('profile')
    return render(request, 'core/subscribe.html')


def subscribed(request):
    return render(request, 'core/subscribed.html')


def terms(request):
    return render(request, 'core/terms.html')


def unsubscribe(request):
    return render(request, 'core/unsubscribe.html')

def unsubscribed(request):
    return render(request, 'core/unsubscribed.html')


def optout(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        email_message = EmailMessage(
            subject='New Subscription from',
            body=f'Email: {email}',
            from_email=settings.ADMIN_EMAIL,  
            to=[settings.ADMIN_EMAIL],
            reply_to=[email],  
        )
        email_message.send(fail_silently=False)

        html_content = render_to_string('emails/welcome.html', {'email': email})

        confirmation_email = EmailMultiAlternatives(
            subject="Subscription Confirmation", 
            body='', 
            from_email=settings.ADMIN_EMAIL,  
            to=[email],  
        )
        confirmation_email.attach_alternative(html_content, "text/html") 


        confirmation_email.send(fail_silently=False)

        messages.success(request, 'Your enquiry has been sent successfully and a confirmation email has been sent!')
        return redirect('subscribe')

    return redirect('index')


def unsub(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        send_mail(
            'User has unsubscribed',
            f'Email: {email}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        messages.success(request, 'Your enquiry has been sent successfully!')
        return redirect('unsubscribe')

    return redirect('index')
