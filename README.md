# Start the project without Docker
##### Start new environment & launch it
```
virtualenv env
source env/bin/activate
```
##### Install the dependencies
```
pip install -r requirements.txt
```

##### Launch the solution
```
python3 main.py
```

# Dockerized Solution
##### Build the Docker image
```
docker build . -t [# TAG_NAME ]
```
##### Run the Docker image 
```
docker run -d [# TAG_NAME ]
``` 
##### List running containers
```
docker ps
```
##### Print out container's logs 
```
docker logs -f [# CONTAINER ID #]
```