FROM python:3.10

WORKDIR /kolo_api

COPY . ./

EXPOSE 8000
# Install production dependencies.
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /kolo_api/src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
