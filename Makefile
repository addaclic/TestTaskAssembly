
venv:
	python3 -m venv .venv
# 	source .venv/bin/activate
# 	pip freeze > requirements.txt
# 	pip install -r requirements.txt

t1:
	python3 task01.py 

t2:
	python3 task02.py https://github.com/paulbouwer/hello-kubernetes src/app 25.300

t3:
	python3 task03.py 1.2 conf.json

t4:
	bash task04.sh