FROM continuumio/anaconda3:4.4.0
COPY . /home/venkat/
EXPOSE 5000
WORKDIR /home/venkat/
RUN pip install -r requirements.txt
CMD python app.py