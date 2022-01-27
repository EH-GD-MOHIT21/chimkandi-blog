from statistics import mode
from django.db import models
from usermanager.models import User
from django.utils import timezone
# Create your models here.


class Blogs(models.Model):


    Blog_categories_available = (
        ("General","General"),
        ("Cricket","Cricket"),
        ("Youtuber","Youtuber"),
        ("Actor","Actor"),
        ("SportPerson","SportPerson"),
        ("TechPerson","TechPerson"),
        ("Teacher","Teacher"),
        ("Health","Health"),
        ("God","God"),
        ("Safety","Safety"),
        ("Exam","Exam"),
        ("other","other"),
    )


    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150,default="Admin Provided Blog")
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    added_at = models.DateTimeField()
    content_position = models.CharField(null=True,blank=True,max_length=10)
    blog_url = models.SlugField(unique=True,null=True,blank=True)
    feature_img = models.ImageField(upload_to='imgs',null=True,blank=True)
    Blog_categories = models.CharField(max_length=15,choices=Blog_categories_available,default="General")
    blog_rating = models.FloatField(default=0)
    total_rate = models.IntegerField(default=0)
    

    @property
    def created(self):
        self.added_at = timezone.now()

    @property
    def slugify_n_set(self):
        title = self.title
        garbages = ["!","@","#","$","%",'"',"'","^","&","*","(",")","{","+","=","}","[","]",":",";","?","/",">",".","<",",","`","~","|","\\"," "]
        for word in title:
            if word in garbages:
                title = title.replace(word,'-')
        try:
            Blogs.objects.get(blog_url=title)
            title = title + f"-{len(Blogs.objects.all())}"
            self.blog_url = title
        except:
            self.blog_url = title

    @property
    def return_categories(self):
        return self.Blog_categories_available



class BlogRatings(models.Model):
    index = models.ForeignKey(Blogs,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.FloatField(default=0)


class BlogImages(models.Model):
    index = models.ForeignKey(Blogs,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='imgs')


class DescFields(models.Model):
    index = models.ForeignKey(Blogs,on_delete=models.CASCADE)
    descr = models.TextField()


class BlogComments(models.Model):
    index = models.ForeignKey(Blogs,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(null=True,blank=True)

    @property
    def add_timestamp(self):
        self.timestamp = timezone.now()