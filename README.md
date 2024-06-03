Tarea 1 | Sistemas Distribuidos | Sección 2

Cristóbal Barra | Ernesto Villa


Primer paso: Clonar github a traves del siguiente comando

--git clone https://github.com/ehnryoo/tarea2_SD


Segundo paso: Segundo paso levantar servicio de docker 

--docker-compose up --build

--docker start tarea2_sd-consumer-1  //Para reiniciar si no funciona el consumer

--docker start tarea2_sd-producer-1  //Para reiniciar si no funciona el producer


Tercer paso: realizar pruebas

--Invoke-WebRequest -Uri http://localhost:4000/solicitud -Method POST -ContentType "application/json" -Body '{"correo": "test@example.com", "data": "some data"}'

--Invoke-WebRequest -Uri http://localhost:4001/solicitud/[id] -Method GET


Paso extra, en la carpeta consumer colocar los datos de un mail para las pruebas

PD: El proyecto de la tarea funciono de buena manera en mi pc, pero al momento de subirlo a github y hacer pruebas de instalacion el producer dejo de funcionar arrojando error de que el script wait-for-kafka no esta en el directorio, siendo que este esta en el directorio, en el video se muestra la implementacion de lo solicitado.
