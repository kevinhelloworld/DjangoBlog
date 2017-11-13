from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect, reverse
from blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.
def post_comment(request, post_pk):
	post = get_object_or_404(Post, pk=post_pk)
	
	if request.method == 'POST':
		form = CommentForm(request.POST)
		
		if form.is_valid():
			# commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
			comment = form.save(commit=False)
			
			# 将评论和被评论的文章关联起来。
			comment.post = post
			
			#数据准备好了，存储入数据库
			comment.save()
			return HttpResponseRedirect(reverse('blog:detail', args=(post.id,)))
			
			
		else:
			comment_list = post.comment_set.all()
			context = {'post': post,
						   'form': form,
						   'comment_list': comment_list
						   }
			return render(request, 'blog/detail.html', context=context)
	return HttpResponseRedirect(reverse('blog:detail', args=(post.id,)))
        
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。    

		
