FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

COPY startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh
CMD ["/app/startup.sh"]
