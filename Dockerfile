FROM python:3.11

# Crear carpeta de trabajo
WORKDIR /code

# Copiar todos los archivos desde ./calendarios_procesos al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y gnupg curl unixodbc-dev gcc g++ && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Muy importante: añadir /code al PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/code"

# Y ejecutar uvicorn indicando el punto de entrada correcto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]