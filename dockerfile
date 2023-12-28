FROM alpine:3.19

WORKDIR $APP_HOME

COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn --host=0.0.0.0 --port 8000 main:app
