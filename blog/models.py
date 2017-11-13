from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name
	"""
    Django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    Django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """


class Tag(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name
	
	
class Post(models.Model):
	title = models.CharField(max_length=70)
	"""
	存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
	"""
	body = models.TextField()
	
	""" 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。"""
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()
	
	"""
	文章摘要excerpt，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
	指定 CharField 的 blank=True 参数值后就可以允许空值了。
	"""
	excerpt = models.CharField(max_length=200, blank=True)
	
	"""我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系"""
	category = models.ForeignKey(Category)
	"""而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。"""
	tags = models.ManyToManyField(Tag, blank=True)
	
	"""
	文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    这里我们通过 ForeignKey 把文章和 User 关联了起来。
    因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
	"""
	author = models.ForeignKey(User)
	
	#该类型的值只允许为正整数或 0，因为阅读量不可能为负值。初始化时 views 的值为 0。
	views = models.PositiveIntegerField(default=0)
	
	def __str__(self):
		return self.title
		
	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])
		#注意这里使用了 update_fields 参数来告诉 Django 只更新数据库中 views 字段的值，以提高效率。
	
	class Meta:
		ordering = ['-created_time']
		"""该内部类定义了post排序方式"""
	
	def save(self, *args, **kwargs):
		if not self.excerpt:
			md = markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
			])
			self.excerpt = strip_tags(md.convert(self.body))[:54]
			
		super(Post, self).save(*args, **kwargs)
	
		
"""		
	def detail(request, pk):
		post = get_object_or_404(Post, pk=pk)
		return render(request, 'blog/detail.html', context={'post':post})
"""
		
	# 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数

