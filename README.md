# Shopee Phone Scraper API

API para extração de telefones de vendedores da Shopee Brasil

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/sidobill/shopee_crawler.git
cd shopee_crawler
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o .env conforme necessário
```

## 🚀 Execução

Inicie o servidor:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse a documentação interativa em:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## 🔍 Endpoints

### POST /scrape
Endpoint principal para extração de telefones.

**Exemplo de requisição:**
```json
{
  "keywords": ["brinquedos", "eletronicos"],
  "max_per_keyword": 5,
  "delay_ms": 1000,
  "proxy": "http://user:pass@proxy:port"  // opcional
}
```

**Exemplo de resposta:**
```json
{
  "results": [
    {
      "phone": "(11) 98765-4321",
      "normalized": "+55 11 98765 4321",
      "source": "description"
    }
  ],
  "execution_time": 3.45,
  "errors": []
}
```

## ⚙️ Configuração

Edite o arquivo `.env` para configurar:

```ini
SHOPEE_BASE_URL=https://shopee.com.br
DEFAULT_DELAY_MS=800  # Delay entre requisições
DEFAULT_MAX_RESULTS=10 # Máximo de resultados por keyword
COUNTRY_DIAL=+55       # Código do país
PROXY_URL=             # Proxy padrão (opcional)
```

## 🛡️ Proxy

Para evitar bloqueios, configure um proxy:

1. No arquivo `.env`:
```ini
PROXY_URL=http://user:pass@proxy:port
```

2. Ou na requisição:
```json
{
  "proxy": "http://user:pass@proxy:port"
}
```

## 🐳 Docker

Para executar com Docker:

```bash
docker build -t shopee-scraper .
docker run -p 8000:8000 shopee-scraper
```

## 📝 Licença

MIT