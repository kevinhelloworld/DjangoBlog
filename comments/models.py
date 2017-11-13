from django.db import models

# Create your models here.

class Comment(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=255)
	url = models.URLField(blank=True)
	text = models.TextField()
	created_time = models.DateTimeField(auto_now_add=True)
	"""我们肯定不希望用户在发表评论时还得自己手动填写评论发表时间，这个时间应该自动生成。"""
	
	post = models.ForeignKey('blog.Post')
	#评论关联文章
	
	def __str__(self):
		return self.text[:20]
	
