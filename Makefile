COMMIT="修改了正则表达式, 使得能够匹配出带[置顶]标识的博客标题, 之前此类博客标题显示不正常..."

github :
	git add -A
	git commit -m $(COMMIT)
	git push origin master

