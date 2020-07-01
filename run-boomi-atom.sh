sudo docker run -p 9090:9090 --privileged -h datadog1 \
  --network ddnetwork \
 -e INSTALLATION_DIRECTORY=/var/boomi \
 -e BOOMI_USERNAME=carolmak@optonline.net \
 -e BOOMI_PASSWORD=Boomi123! \
 -e BOOMI_ATOMNAME=atom1 \
 -e BOOMI_CONTAINERNAME=atom1 \
 -e BOOMI_ACCOUNTID=trainingcarolmackin-TIFUB8 \
 -e ATOM_LOCALHOSTID=datadog1 \
 -e ATOM_VMOPTIONS_OVERRIDES=-javaagent:/var/boomi/javaagent/dd-java-agent-0.55.1.jar\|-Ddd.agent.host=docker-dd-agent\|-Ddd.agent.port=8126 \
 --name atom1 \
 -v /var/boomi:/var/boomi:rw \
 -d -t boomi/atom:release


