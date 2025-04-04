# payment-service

## 1. Criar e ativar o ambiente virtual (venv)

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

## 2. Instalar as dependências do projeto

```bash
pip install -r requirements.txt
```

```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

## 3. Executar o projeto com Docker

```bash
sudo systemctl restart docker
```

```bash
docker compose up --build --remove-orphans
```

## 4. Acessar a API

```
http://0.0.0.0:8003/docs
```
