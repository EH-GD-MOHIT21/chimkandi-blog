import json
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import BlogComments, User,BlogRatings
from django.utils import timezone
from .models import Blogs,BlogImages,DescFields
# required for pagination
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import os
from django.conf import settings
from django.http import JsonResponse as Response
from django.views.decorators.csrf import csrf_exempt


def RenderHome(request):
    all_blogs = Blogs.objects.all().order_by('-added_at')
    recent_blogs = all_blogs[:3]
    superuserblogs = []
    show_titlefeature = True
    for blog in all_blogs:
        if blog.author.is_superuser:
            superuserblogs.append(blog)
        if len(superuserblogs)==3:
            break

    if not len(superuserblogs):
        show_titlefeature = False
    return render(request,'home.html',{'rblogs':recent_blogs,'superuserblogs':superuserblogs,'show':show_titlefeature})






def RenderDashboard(request):
    imgavi = True
    is_ref_av = False
    is_reward_av = False
    if not request.user.is_authenticated:
        return redirect('/')
    try:
        obj = User.objects.get(email=request.user.email)
    except:
        return HttpResponse('Looks like you are\'nt authenticated')
    if obj.profile_pic=='' or obj.profile_pic == None:
        imgavi = False
    reward_claimed_at = obj.last_reward_claimed
    nested_balence = round(obj.nested_balance,2)
    referal_by = obj.Referal_by
    if referal_by == '' or referal_by == None:
        is_ref_av = True
    
    if timezone.now().date() != reward_claimed_at:
        is_reward_av = True
    
    blogs = Blogs.objects.filter(author=request.user)[:3]
    if len(blogs):
        blogs_avi = True
    else:
        blogs_avi = False

    data = get_my_referal(request.user.email)
    is_refer = True

    if data is None:
        is_refer = False
    

    return render(request,'dashboard.html',{'imgavi':imgavi,'is_ref_av':is_ref_av,'reward_claimed_at':reward_claimed_at,'nested_balence':nested_balence,'pic':obj.profile_pic,'is_reward_av':is_reward_av,'referal_by':referal_by,'username':request.user.email,'isblogavi':blogs_avi,'blogs':blogs,'is_refer':is_refer,'data':data})






def checkforReferal(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            email = request.POST["authmail"]
            if email == request.user.email:
                return redirect('/')
            try:
                if User.objects.get(email=request.user.email).Referal_by == '' or User.objects.get(email=request.user.email).Referal_by == None:
                    scum = User.objects.get(email=email)
                    scum.nested_balance += 1.0   # shared person gets 1
                    scum.save()
                    scum = User.objects.get(email=request.user.email)
                    scum.nested_balance += 0.5  # filled person gets 0.5
                    scum.Referal_by = email
                    scum.save()
                    return HttpResponse('Successfully claimed referal reward.')
                return HttpResponse('Already earned Referal')
            except:
                return redirect('/dashboard')
        except Exception as e:
            return redirect('/')
    else:
        return redirect('/')






def RenderBlogPage(request):
    return render(request,'blog.html')





# RenderPostBlogPage
def postblog(request):
    if request.user.is_authenticated:
        cat_data = []
        available_cats = Blogs().Blog_categories_available
        for cat in available_cats:
            cat_data.append(cat[0])
        return render(request,'postblog.html',{'data':cat_data})
    return redirect('/')





def acceptblogdata(request):
    if request.user.is_authenticated and request.method == "POST":
        desc_indexes = []
        img_indexes = []
        if User.objects.get(email=request.user.email).nested_balance < 1.5:
            return HttpResponse("Your Nested Coin is less than 1.5 you can't upload a blog now.")
        try:
            title = request.POST["title"]
            fimage = request.FILES["fimage"]
            category = request.POST["category"]
            for i in range(1,10):
                try:
                    file = request.FILES[str(i)]
                    img_indexes.append(i)
                except Exception as e:
                    pass
            for i in range(1,10):
                if i not in img_indexes:
                    try:
                        request.POST[str(i)]
                        desc_indexes.append(i)
                    except:
                        break
            try:
                if len(img_indexes) and len(desc_indexes):
                    maximum = max(max(img_indexes),max(desc_indexes))
                elif len(img_indexes):
                    maximum = len(img_indexes)
                elif len(desc_indexes):
                    maximum = len(desc_indexes)
                else:
                    maximum = 0
            except:
                maximum = 0
            blog_pos_spec = ""
            for i in range(1,maximum+1):
                if i in desc_indexes:
                    blog_pos_spec += "t"
                else:
                    blog_pos_spec += "i"
            blog_model = Blogs()
            blog_model.title = title
            blog_model.feature_img = fimage
            blog_model.Blog_categories = category
            blog_model.author = request.user
            blog_model.created
            blog_model.content_position = blog_pos_spec
            blog_model.slugify_n_set
            blog_model.save()
            for desc in desc_indexes:
                d_obj = DescFields(index=blog_model,descr=request.POST[str(desc)])
                d_obj.save()
            for img in img_indexes:
                i_obj = BlogImages(index=blog_model,image=request.FILES[str(img)])
                i_obj.save()
            cum_ = User.objects.get(email=request.user.email)
            cum_.nested_balance -= 1.5
            cum_.save()

            return redirect('/dashboard')
        except Exception as e:
            # for some reason if some of stuff didn't loaded then delete all the saved info
            try:
                blog_model.delete()
                for desc in desc_indexes:
                    d_obj = DescFields(index=blog_model)
                    d_obj.delete()
                for img in img_indexes:
                    i_obj = BlogImages(index=blog_model)
                    i_obj.delete()
            except:
                pass
            # print(e)
            return redirect('/postblog')
    else:
        return redirect('/')







def RenderUniqueBlogPage(request,blogurl):
    try:
        blog = Blogs.objects.get(blog_url=blogurl)
        title = blog.title
        author = blog.author
        category = blog.Blog_categories
        timestamp = blog.added_at
        blog_rating = blog.blog_rating
        total_rating = blog.total_rate
        images = BlogImages.objects.filter(index=blog)
        desc = DescFields.objects.filter(index=blog)
        render_str = blog.content_position
        render_obj = []
        img_index = 0
        desc_index = 0
        render_string_obj = []
        for word in render_str:
            if word == "t":
                render_obj.append(desc[desc_index])
                desc_index += 1
                render_string_obj.append(word)
            elif word == "i":
                render_obj.append(images[img_index])
                img_index += 1
                render_string_obj.append(word)

        if len(render_obj)!= len(render_string_obj):
            return HttpResponse("There is some error for showing your blog.")

        
        final_render_obj = zip(render_string_obj,render_obj)
        recent_blogs_3 = Blogs.objects.filter(author=author).order_by('added_at')[:3]

        user_rating_exists = False
        user_rating = 0

        if request.user.is_authenticated:
            try:
                user_rating = int(BlogRatings.objects.get(index=blog,user=request.user).rating)
                user_rating_exists = True
            except:
                pass
        comments = BlogComments.objects.filter(index=blog)
        return render(request,'blog.html',{'title':title,'author':author,'timestamp':timestamp,'data':final_render_obj,'recent':recent_blogs_3,'category':category,"user_rating_exists":user_rating_exists,"user_rating":user_rating,"blog_rating":blog_rating,"comments":comments,"total_rating":total_rating,"blog_url":blogurl})
    except Exception as e:
        # print(e)
        return redirect('/')




def get_my_referal(username):
    objects = User.objects.filter(Referal_by=username)
    if len(objects):
        return objects
    return None



def RenderSearchFields(request):
    try:
        filter = request.GET["filter"]
        data = request.GET["data"]
        if data == "" or data is None:
            return redirect('/')

        post_per_page = 9
        page = request.GET.get('page')

        dataset = CollectAppropriateData(filter,data)

        # dataset = Blogs.objects.all()
        if dataset == None:
            return HttpResponse('Sorry No Resourses Found.')
        posts = Paginator(dataset,post_per_page)

        try:
            posts_pp = posts.page(page)
        except PageNotAnInteger:
            posts_pp = posts.page(1)
        except EmptyPage:
            posts_pp = posts.page(posts.num_pages)
    except Exception as e:
        print(e)
        return redirect('/')
    return render(request,'search.html',{'posts':posts_pp,'rest_url':f"filter={filter}&data={data}"})




def CollectAppropriateData(filter,data):
    if filter == 'category':
        dataset = Blogs.objects.filter(Blog_categories__icontains=data)
        if len(dataset):
            return dataset
        return None
    elif filter == 'author':
        try:
            user = User.objects.get(email=data)
        except:
            return None
        blogs = Blogs.objects.filter(author=user)
        if len(blogs):
            return blogs
        return None
    elif filter == "rating":
        try:
            dataset = Blogs.objects.filter(blog_rating__gte=float(data)).order_by("-blog_rating")
            if len(dataset):
                return dataset
            return None
        except:
            return None
    elif filter == 'title':
        dataset = Blogs.objects.filter(title__icontains=data)
        if len(dataset):
            return dataset
        return None
    elif filter == "recent_posts":
        dataset = Blogs.objects.all()
        if len(dataset):
            return dataset
        return None
    elif filter == "featured_posts":
        dataset_list = Blogs.objects.all()
        dataset = []
        for element in dataset_list:
            if element.author.is_superuser:
                dataset.append(element)
        if len(dataset):
            return dataset
        return None
    elif filter == 'timestamp':
        dataset = Blogs.objects.filter(added_at__icontains=data)
        if len(dataset):
            return dataset
        return None
    return None



def changepp(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            ppicupdated = request.FILES["ppicupdated"]
            cumobj = User.objects.get(email=request.user.email)
            try:
                pre_pic = str(cumobj.profile_pic)
                full_path = os.path.join(str(settings.MEDIA_ROOT) + os.sep,pre_pic)
                os.remove(str(full_path))
            except:
                pass
            cumobj.profile_pic = ppicupdated
            cumobj.save()
            return redirect('/dashboard')
        except Exception as e:
            print(e)
            return redirect('/')
    return redirect('/')


@csrf_exempt
def make_rating(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return Response({'status':403,'message':'Please authenticate to rate a blog.'})
    try:
        body = json.loads(request.body)
        blog_url = body.get("blog_url")
        rating = body.get("rating")
        blog_url = str(blog_url).split('/')[-1]
        rating = int(str(rating).split('-')[-1])
        blogmodel = Blogs.objects.get(blog_url=blog_url)
        try:
            BlogRatings.objects.get(index=blogmodel,user=request.user)
            return Response({'status':406,'message':'You have already rated this blog.'})
        except:
            pass
        model = BlogRatings(index=blogmodel)
        model.user = request.user
        model.rating = rating
        model.save()
        rate_model = BlogRatings.objects.filter(index=blogmodel)
        blogmodel.blog_rating = (blogmodel.blog_rating * (len(rate_model)-1) + rating) / (len(rate_model) )
        blogmodel.total_rate += 1
        blogmodel.save()

        return Response({'status':200,'message':'success'})
    except Exception as e:
        print(e)
        return Response({'status':404,'message':'Blog not found.'})


@csrf_exempt
def post_comment(request):
    if not request.user.is_authenticated or request.method != "POST":
        return Response({'status':400,'message':'Invalid Request.'})
    try:
        body = json.loads(request.body)
        blog_url = body.get('blog_url')
        user = request.user
        comment = body.get('comment')
        blog_url = str(blog_url).split('/')[-1]
        blog_model = Blogs.objects.get(blog_url=blog_url)
        obj = BlogComments(index=blog_model,user=user)
        obj.comment = comment
        obj.add_timestamp
        obj.save()
        return Response({'status':200,'message':'success'})
    except:
        return Response({'status':400,'message':'Invalid Request.'})



def removecomment(request):
    if not request.user.is_authenticated or request.method != "POST":
        return redirect('/')
    try:
        timestamp = request.POST["timestamp-comment"]
        current_user_path = str(request.POST["current-user-path"])
        blog = Blogs.objects.get(blog_url=current_user_path)
        usercomment = BlogComments.objects.get(id=timestamp,user=request.user,index=blog)
        usercomment.delete()
        return redirect('/blogs/'+current_user_path)
    except:
        return redirect('/')


@csrf_exempt
def delete_blog(request):
    if not request.user.is_authenticated or request.method != "POST":
        return Response({'status':400,'message':'Looks like you are not authorised.'})
    try:
        body = json.loads(request.body)
        blog = Blogs.objects.get(blog_url=body.get('blog_url'))
        if blog.author.email != request.user.email:
            return Response({'status':403,'message':'You don\'t have permission to delete this Blog.'})
        blog.delete()
        return Response({'status':200,'message':'success'})
    except:
        return Response({'status':404,'message':'Blog Not Found.'})