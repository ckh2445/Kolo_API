FROM python:3.8

WORKDIR /kolo_api

COPY . ./

EXPOSE 9999
# Install production dependencies.
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /kolo_api/src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9999"]