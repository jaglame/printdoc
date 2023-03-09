# 1. Crear entorno virtual

>git clone git@github.com:jaglame/printdoc.git

>cd printdoc

>virtualenv env -p python3

>. env/bin/active

# 2. Instalar paquete
>python setup.py develop

# 3. config.ini (para modificar)
> cd printdoc

> cp config_copy.ini config.ini

# 4. Levantar servicio
## Devel

> python serve.py

## uwsgi

>chmod +x serve_uwsgi

>./serve_uwsgi

# Verificar.
>http://0.0.0.0:9191

RUNNING
