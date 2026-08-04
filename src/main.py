from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import re
import os
from typing import List, Optional
from dotenv import load_dotenv
import logging
import time

# Configurações iniciais
load_dotenv()
app = FastAPI()

# Headers para simular navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://shopee.com.br/"
}

# Regex para telefones brasileiros
PHONE_REGEX = r"(?:\+?55\s?)?(?:\(?\d{2}\)?[\s-]?)(?:9\s?\d{4}[\s-]?\d{4}|\d{4}[\s-]?\d{4})"

# Modelos Pydantic
class ScrapeRequest(BaseModel):
    keywords: List[str]
    max_per_keyword: int = 10
    delay_ms: int = 800
    proxy: Optional[str] = None

class ShopEntry(BaseModel):
    shop_id: int
    name: str
    url: str
    description: Optional[str] = None

class PhoneResult(BaseModel):
    phone: str
    normalized: str
    source: str  # 'description' ou 'html'

class ScrapeResponse(BaseModel):
    results: List[PhoneResult]
    execution_time: float
    errors: List[str] = []

# Funções auxiliares
def clean_phone(phone: str) -> str:
    """Normaliza número de telefone para formato +55 DDD 9XXXX-XXXX"""
    digits = re.sub(r"[^\d]", "", phone)
    if len(digits) == 11:
        return f"+55 {digits[:2]} {digits[2:7]}-{digits[7:]}"
    return phone

async def search_products(keyword: str, client: httpx.AsyncClient) -> List[int]:
    """Busca produtos por keyword e retorna lista de shop_ids"""
    try:
        url = f"{os.getenv('SHOPEE_BASE_URL')}/api/v4/search/search_items?by=relevancy&keyword={keyword}&limit=50&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return [item['item_basic']['shopid'] for item in data['items']]
    except Exception as e:
        logging.error(f"Erro ao buscar produtos: {e}")
        return []

async def get_shop_info(shop_id: int, client: httpx.AsyncClient) -> Optional[ShopEntry]:
    """Obtém informações básicas da loja"""
    try:
        url = f"{os.getenv('SHOPEE_BASE_URL')}/api/v4/product/get_shop_info?shopid={shop_id}"
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return ShopEntry(
            shop_id=shop_id,
            name=data['data']['name'],
            url=f"{os.getenv('SHOPEE_BASE_URL')}/shop/{shop_id}",
            description=data['data'].get('description')
        )
    except Exception as e:
        logging.error(f"Erro ao obter info da loja {shop_id}: {e}")
        return None

# Endpoints
@app.get("/")
async def root():
    return {"message": "API para extração de telefones de vendedores Shopee Brasil"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/scrape", response_model=ScrapeResponse)
async def scrape_phones(request: ScrapeRequest):
    start_time = time.time()
    results = []
    errors = []
    
    async with httpx.AsyncClient(proxies=request.proxy) as client:
        for keyword in request.keywords:
            try:
                shop_ids = await search_products(keyword, client)
                for shop_id in shop_ids[:request.max_per_keyword]:
                    shop_info = await get_shop_info(shop_id, client)
                    if shop_info:
                        # Implementar lógica de extração de telefones aqui
                        pass
                    time.sleep(request.delay_ms / 1000)
            except Exception as e:
                errors.append(f"Erro ao processar keyword '{keyword}': {str(e)}")
    
    return ScrapeResponse(
        results=results,
        execution_time=time.time() - start_time,
        errors=errors
    )