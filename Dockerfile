COPY . /home/venkat/
EXPOSE 5000
WORKDIR /home/venkat/
RUN pip install -r requirements.txt
CMD python app.py
