# This is a Docker file which allows us to set up what our Docker
# container will look like and how it is structured

# Start with the Python 3.7 directory from Docker
FROM python:3.7
# Add all files . into a new dir in the container called /usr/src/app
ADD . /usr/src/app
# Set this dir as our working directory
WORKDIR /usr/src/app
# expose port 4000 to the host OS to interact with the container
EXPOSE 4000
# Run any setup commands we desire to configure the virtual environment in the container
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Start the app from the index.py file
ENTRYPOINT ["python","index.py"]
