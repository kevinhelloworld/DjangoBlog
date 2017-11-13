from ..models import Post, Category
from django import template#导入模板用以注册这个函数为模板标签
from django.db.models.aggregates import Count
from blog.models import Tag

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
	"""获取最新文章标签"""
	return Post.objects.all().order_by('-created_time')[:num]
	
@register.simple_tag	
def achives():
	"""归档模板标签"""
	return Post.objects.dates('created_time', 'month', order='DESC')
	""" 
	dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，且是 
	Python 的 date 对象（！！！），精确到月份，降序排列。接受的三个参数值表明了这些含义，一个是
	created_time (对象名)，即 Post 的创建时间，month 是精度，order='DESC' 表明降序排列.
	"""
	
	
@register.simple_tag	
def get_categories():
#	return Category.objects.all()
	return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
	
# Count 计算标签分类下的文章数，其接受的参数为需要计数的模型的名称
tag_list = Tag.objects.annotate(num_posts=Count('post'))

@register.simple_tag
def get_tags():
	return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

