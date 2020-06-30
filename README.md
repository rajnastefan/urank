#Urank documentation for Windows
#Prerquisites:
    python3
    docker 

###Docker Download
Download docker (for Win10)
https://hub.docker.com/editions/community/docker-ce-desktop-windows/

###Docker setup
  * Go to Docker settings and in the "Network" tab set DNS Server as fixed
  * In Advanced tab increase number of CPUs and Memory
  * Navigate to urank/docker_config folder and run following commands in Windows PowerShell(pull last image)
   
    ```docker pull docker.elastic.co/elasticsearch/elasticsearch:6.8.1```
    
  * Build image from Dockerfile
  
    ```docker build -t elasticsearch-ingest .```

  * Run elastic search
  
    ```docker run -d -p 9200:9200 elasticsearch-ingest```

 * Use command below to find and copy Container ID and paste instead of <container_id> in next command
docker ps --filter status=running, use id and paste into following command

    ```docker  run --rm --link <container_id>:elasticsearch --name kibana -p 5601:5601 docker.elastic.co/kibana/kibana:6.8.1```

* Open browser and type ```localhost:5601``` and check KIBANA UI

### Install pip requirements
We used Pycharm editor functionality to automatically install requirements, you can also use anaconda and execute:

    pip install -r requirements.txt

### Run
Now you can run urank_frontend_app.py script

    python urank_frontend_app.py
