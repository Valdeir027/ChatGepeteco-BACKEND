# Use a imagem base do Python para Django
FROM python:3.10
# Define o diretório de trabalho dentro do container
WORKDIR /code

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o resto do código para o diretório de trabalho
COPY . .
# Configuração para o servidor Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "django_project.asgi:application"]