# Usa la imagen base de node 18.18.0
FROM node:18.18.0

# Instala curl y otras dependencias necesarias
RUN apt-get update && apt-get install -y curl

# Instala Git
RUN apt-get install -y git
# Clona el repositorio y ejecuta los comandos
RUN git clone -b dev https://github.com/cristian-encalada/Alquivago.git
# Establecer el directorio de trabajo
WORKDIR /Alquivago/vite-project/
# Instalar dependencias y ejecutar vite
CMD npm install && npm run dev
