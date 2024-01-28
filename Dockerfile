FROM python:3.10.12

# Print output immediately
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
