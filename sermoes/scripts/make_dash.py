import json
d=json.load(open('dashboard_data.json'))
keep=['id','titulo','pregador','data','ano','texto','confianca','serie','tipo','youtube','link','refs','livros']
d['sermoes']=[{k:x[k] for k in keep} for x in d['sermoes']]
s=open('dashboard_template.html').read().replace('/*DATA*/null',json.dumps(d,ensure_ascii=False,separators=(',',':')))
open('/home/user/teste/sermoes/dashboard.html','w').write(s)
print(len(s)//1024,'KB')
