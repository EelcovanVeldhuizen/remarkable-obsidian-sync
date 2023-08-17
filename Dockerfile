FROM python:3.11.4
# Or any preferred Python version.
ADD main.py .
RUN pip install "git+https://github.com/EelcovanVeldhuizen/rmc.git@Excalidraw"
RUN mkdir -p /app/remarkables
RUN mkdir - /app/vault
CMD ["python", "./main.py"] 