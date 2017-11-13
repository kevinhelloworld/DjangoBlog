from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Post, Category, Tag
# Create your views here.


"""
调用 Django 提供的 render 函数。这个函数根据我们传入的参数来构造 HttpResponse。
最终，我们的 HTML 模板中的内容字符串被传递给 HttpResponse 对象并返回给浏览器
（Django 在 render 函数里隐式地帮我们完成了这个过程）
"""

"""
def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})
"""
#index视图函数修改为类视图
class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 5
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		pagination_data = self.pagination_data(paginator, page, is_paginated)
		context.update(pagination_data)
		return context
		
	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:
			return {}
		left = []
		right = []
		left_has_more = False
		right_has_more = False
		first = False
		last = False
		page_number = page.number
		total_pages = paginator.num_pages
		page_range = paginator.page_range
		
		if page_number == 1:
			right = page_range[page_number:page_number + 2]
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True
		elif page_number == total_pages:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		else:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		data = {
			'left': left,
			'right': right,
			'left_has_more': left_has_more,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
		}
		return data

	
	
    
"""    
def detail(request, pk):
	
	# 记得在顶部引入 markdown 模块
	post = get_object_or_404(Post,
	 pk=pk)
	
	阅读量+1
	post.increase_views()
	
	post.body = markdown.markdown(post.body,
								  extensions=[
									'markdown.extensions.extra',
									'markdown.extensions.codehilite',
									'markdown.extensions.toc',
								  ])
	form = CommentForm()
	comment_list = post.comment_set.all()
	context = {'post': post,
			   'form': form,
			   'comment_list': comment_list
			   }
	return render(request, 'blog/detail.html', context=context)
"""
#detail的类视图
class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'
	
	def get(self, request, *args, **kwargs):
		response = super(PostDetailView, self).get(request, *args, **kwargs)
		self.object.increase_views() #统计数量
		# 注意 self.object 的值就是被访问的文章 post
		
		# (get方法)视图必须返回一个 HttpResponse 对象
		return response
		
	def get_object(self, queryset=None):
		# 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
		post = super(PostDetailView, self).get_object(queryset=None)
		post.body = markdown.markdown(post.body,
									  extensions=[
										'markdown.extensions.extra',
										'markdown.extensions.codehilite',
										'markdown.extensions.toc',
									  ])
		return post
		
	def get_context_data(self, **kwargs):
		# 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
		# 还要把评论表单、post 下的评论列表传递给模板。
		context = super(PostDetailView, self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({
			'form': form,
			'comment_list': comment_list
		})
		return context
"""	
def achives(request, year, month):
	post_list = Post.objects.filter(created_time__year=year,
									created_time__month=month
									)
	return render(request, 'blog/index.html', context={'post_list':post_list})
"""
#achives的类视图
class AchivesView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	
	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs['month']  #kwargs是一个字典
		return super(AchivesView, self).get_queryset().filter(created_time__year=year,
															  created_time__month=month)
	"""
	注意这里 created_time 是 Python 的 date 对象，其有一个 year 和 month 属性
	python中类实例调用属性的方法通常是 created_time.year，但是由于这里作为函数的
	参数列表，所以 Django 要求我们把点替换成了两个下划线，即 created_time__year
	"""

"""
def category(request, pk):
	cate = get_object_or_404(Category, pk=pk)
	post_list = Post.objects.filter(category=cate)
	return render(request, 'blog/index.html', context={'post_list': post_list})
"""
#category的类视图
class CategoryView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	#由于类中指定的属性值和IndexView是一样的，所以也可以直接继承IndexView
	
	def get_queryset(self):
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
		
		#覆写了父类的 get_queryset 方法。该方法默认获取指定模型的全部列表数据
		
		return super(CategoryView, self).get_queryset().filter(category=cate)
		"""在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）
		里，非命名组参数值保存在实例的 args 属性（是一个列表）里。所以我们使了 self.kwargs.get('pk') 
		来获取从 URL 捕获的分类 id 值。
		调用父类的 get_queryset 方法获得全部文章列表，紧接着就对返回的结果调用了
		 filter 方法来筛选该分类下的全部文章并返回。
		"""
	
#标签视图函数
class TagView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	
	def get_queryset(self):
		tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(tags=tag)
		

def search(request):
	q = request.GET.get('q')
	error_msg = ''
	
	if not q:
		error_msg = "请输入关键词"
		return render(request, 'blog/index.html', {'error_msg': error_msg})
		
	post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
	return render(request, 'blog/index.html', {'error_msg': error_msg,
												   'post_list': post_list})
												   

def about(request):
	return render(request, 'blog/about.html')
	
	
def contact(request):
	return render(request, 'blog/contact.html')
	
	

