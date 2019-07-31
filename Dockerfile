FROM python:3.6.5-slim
COPY . .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 80
CMD ["python", "src/app.py"]