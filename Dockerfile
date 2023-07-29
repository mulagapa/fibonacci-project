FROM python
LABEL authors="manidharmulagapaka"
WORKDIR /
COPY requirements.txt /
ADD templates/ /templates/
COPY tests/ /tests/
RUN pip install -r requirements.txt
COPY app.py /
EXPOSE 5000
CMD ["flask" , "--app", "app", "--debug", "run", "--host", "0.0.0.0"]
