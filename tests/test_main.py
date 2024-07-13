import pytest
from httpx import AsyncClient
from app.schemas import AtletaCreate, Atleta

@pytest.mark.asyncio
async def test_create_atleta(client: AsyncClient):
    atleta = {"nome": "João", "cpf": "12345678900", "centro_treinamento": "Centro A", "categoria": "Categoria 1"}
    response = await client.post("/atletas/", json=atleta)
    assert response.status_code == 200
    assert response.json()["nome"] == atleta["nome"]
    assert response.json()["cpf"] == atleta["cpf"]

@pytest.mark.asyncio
async def test_get_atletas(client: AsyncClient):
    response = await client.get("/atletas/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "items" in response.json()

@pytest.mark.asyncio
async def test_get_atleta(client: AsyncClient):
    atleta_id = 1
    response = await client.get(f"/atletas/{atleta_id}")
    if response.status_code == 200:
        assert response.json()["id"] == atleta_id
    else:
        assert response.status_code == 404
