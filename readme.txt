1. conda create --file env.txt -n urank
2. activate urank
3. pip install -r requirements.txt
4. python urank_app.py


#docker setup
1. Download docker (for Win10)
https://hub.docker.com/editions/community/docker-ce-desktop-windows/

2. Go to Docker settings and in the "Network" tab set DNS Server as fixed

3. navigate to urank/docker_config folder and run following commands in Windows PowerShell
docker build -t elasticsearch-ingest .
docker run -d -p 9200:9200 elasticsearch-ingest

4. Now you can run urank_app.py script
