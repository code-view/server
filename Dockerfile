FROM python:3.5

ENV version 0.1.1
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
RUN useradd -r code_view
VOLUME /src/code_view/settings/local/
EXPOSE 8080
USER code_view
CMD ["gunicorn", "code_view.main:app", "--bind", "0.0.0.0:8080", "--worker-class", "aiohttp.worker.GunicornWebWorker"]
