FROM python:3.11.4

ADD main.py .
RUN apt-get update && apt-get -y install poppler-utils && apt-get clean
RUN pip install pdf2image
RUN pip install "git+https://github.com/EelcovanVeldhuizen/rmc.git@Excalidraw"
RUN mkdir -p /app/remarkables
RUN mkdir -p /app/vault
CMD ["python", "./main.py"] 
