FROM python:3.10
WORKDIR /generation
ADD . /generation

RUN pip install -r requirements.txt

CMD ["python", "gen_toast.py"]