$ kubectl exec -it mypod -- bash

root@mypod:/# curl http://rest-service.prod.svc:9100/ping;echo
PONG!

root@mypod:/# curl http://rest-service.prod.svc:9100/info;echo
Host Name: rest-7478b84459-dd8jx
Host IP: 10.244.0.69
Client IP : 10.244.0.31

root@mypod:/# curl http://rest-service.prod.svc:9100/person/1/
{"first_name":"sazae","id":1,"last_name":"fuguta"}

root@mypod:/# curl http://rest-service.prod.svc:9100/person/2/
{"first_name":"masuo","id":2,"last_name":"fuguta"}

root@mypod:/# curl http://rest-service.prod.svc:9100/person/3/
{"first_name":"namihei","id":3,"last_name":"isono"}

root@mypod:/# root@mypod:/# curl -X POST -H "Content-Type: application/json" -d '{"fname" : "fune" , "lname" : "isono"}' http://rest-service.prod.svc:9100/person/

root@mypod:/# curl http://rest-service.prod.svc:9100/person/4/
{"first_name":"fune","id":4,"last_name":"isono"}

root@mypod:/# curl http://rest-service.prod.svc:9100/persons  
[{"first_name":"sazae","id":1,"last_name":"fuguta"},{"first_name":"masuo","id":2,"last_name":"fuguta"},{"first_name":"namihei","id":3,"last_name":"isono"}]

kubectl exec -it db-0 -n prod -- bash
mariadb --user user1 --password=secret1 mydb
 
CREATE TABLE Persons (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC));

INSERT INTO Persons VALUES (1, "sazae","fuguta");
INSERT INTO Persons VALUES (2, "masuo","fuguta");
INSERT INTO Persons VALUES (3, "namihei","isono");
select * from Persons;

