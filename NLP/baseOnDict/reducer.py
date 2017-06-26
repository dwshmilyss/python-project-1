# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
id2score = {}
#fin = open("result.txt")
for line in sys.stdin:
	line = line.strip()
	weiboId, score = line.split('\t')
	if id2score.get(weiboId) is None:
		id2score[weiboId] = int(score)
	else:
		id2score[weiboId] = id2score[weiboId] + int(score)

for weiboId, score in id2score.items():
	print '%s\t%s' % (weiboId, score)
