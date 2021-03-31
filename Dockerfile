COPY . /home/venkat/Google-playstore-app-ratings-prediction
EXPOSE 5000
WORKDIR /home/venkat/Google-playstore-app-ratings-prediction
RUN pip install -r requirements.txt
CMD python app.py
