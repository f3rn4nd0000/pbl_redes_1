docker build -t dispositivo-udp . && docker run -it --rm --name dispositivo-udp -p 19900-20000:19900-20000 --net=host dispositivo-udp

