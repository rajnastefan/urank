#Urank documentation for Windows
#Prerquisites:
    python

#docker setup
Download docker (for Win10)
https://hub.docker.com/editions/community/docker-ce-desktop-windows/

##Docker set up
  - Go to Docker settings and in the "Network" tab set DNS Server as fixed
  - In Advanced tab increase number of CPUs and Memory

#navigate to urank/docker_config folder and run following commands in Windows PowerShell
#pull last image
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.8.1

#build image from Dockerfile
docker build -t elasticsearch-ingest .

#run elastic search
docker run -d -p 9200:9200 elasticsearch-ingest

#use command below to find and copy Container ID and paste instead of <container_id> in next command
docker ps --filter status=running

#use id and paste into following command
docker  run --rm --link <container_id>:elasticsearch --name kibana -p 5601:5601 docker.elastic.co/kibana/kibana:6.8.1

#open browser and type localhost:5601 and check KIBANA UI

#install pip requirements
#We used Pycharm editor functionality to automatically install requirements
pip install -r requirements.txt


#Now you can run urank_frontend_app.py script
python urank_frontend_app.py
