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
