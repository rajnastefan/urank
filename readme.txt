1. conda create --file env.txt -n urank
2. activate urank
3. pip install -r requirements.txt
4. python urank_app.py


#docker setup
1. Download docker (for Win10)
https://hub.docker.com/editions/community/docker-ce-desktop-windows/

2.  Docker set up
  - Go to Docker settings and in the "Network" tab set DNS Server as fixed
  - In Advanced tab increase number of CPUs and Memory

3. navigate to urank/docker_config folder and run following commands in Windows PowerShell
#pull last image
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.8.1

#build image from Dockerfile
docker build -t elasticsearch-ingest .

#run elastic search
docker run -d -p 9200:9200 elasticsearch-ingest

#use command below to find and copy Container ID and paste instead of <container_id> in next command
docker ps --filter status=running
docker  run --rm --link <container_id>:elasticsearch --name kibana -p 5601:5601 docker.elastic.co/kibana/kibana:6.8.1

#open browser and type localhost:5601 and check KIBANA UI

4. Now you can run urank_app.py script
