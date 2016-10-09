COMMIT="刷新输出信息用互斥锁保护, 从而保解决信息的乱序输出问题..."



github :
	git add -A
	git commit -m $(COMMIT)
	git push origin master

