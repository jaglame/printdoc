# 1. Crear entorno virtual
>virtualenv env -p python3

>. env/bin/active

# 2. Instalar paquete
>python setup.py develop

# 3. config.ini (para modificar)
>Copiar config_copy.ini y renombrar como config.ini

# 4. Levantar servicio
## Devel
>cd printdoc

> python serve.py

## uwsgi
>cd printdoc

>chmod +x serve_uwsgi

>./serve_uwsgi

# Verificar.
>http://0.0.0.0:9191

RUNNING
