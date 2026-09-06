from cryptography.hazmat.primitives.asymmetric import rsa

from app.core.models import AppSnapshot
from app.integrations.state.memory_provider import MemoryStateRepository

from .conftest import HttpTestClient, access_token


def test_catalogue_and_recipe_search(client: HttpTestClient) -> None:
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["catalog"] == "sample"
    all_recipes = client.get("/api/recipes")
    assert all_recipes.status_code == 200
    assert all_recipes.json()["total"] == 8
    filtered = client.get(
        "/api/recipes", params={"selectedFoodIds": ["tomato", "egg"], "match": "all"}
    )
    assert filtered.status_code == 200
    assert filtered.json()["total"] == 1
    assert filtered.json()["items"][0]["id"] == "tomato-egg"
    assert client.get("/api/recipes/tomato-egg").status_code == 200
    assert client.get("/api/recipes/no-such-recipe").status_code == 404
    assert client.get("/api/foods", params={"q": "トマト"}).json()["total"] == 1


def test_filter_boundaries_and_no_portions_in_search(client: HttpTestClient) -> None:
    response = client.get("/api/recipes", params={"maxMinutes": "10"})
    assert response.status_code == 200
    assert all(item["minutes"] <= 10 for item in response.json()["items"])
    assert client.get("/api/recipes", params={"maxMinutes": "-1"}).status_code == 422
    assert client.get("/api/recipes", params={"servings": "2"}).status_code == 422
    excluded = client.get("/api/recipes", params={"excludedFoodIds": "egg"})
    assert all(
        "egg" not in [ingredient["foodId"] for ingredient in recipe["ingredients"]]
        for recipe in excluded.json()["items"]
    )


def test_state_requires_real_bearer_and_ignores_user_header(client: HttpTestClient) -> None:
    response = client.get("/api/state", headers={"X-User-Id": "user-a"})
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers


def test_conditional_write_conflict_and_user_isolation(
    client: HttpTestClient,
    private_key: rsa.RSAPrivateKey,
    snapshot: AppSnapshot,
    repository: MemoryStateRepository,
) -> None:
    headers = {"Authorization": "Bearer " + access_token(private_key)}
    body = {"expectedVersion": 0, "snapshot": snapshot.model_dump(by_alias=True)}
    response = client.put("/api/state", headers=headers, json=body)
    assert response.status_code == 200
    assert response.json()["version"] == 1
    assert response.json()["snapshot"]["version"] == 3
    assert client.put("/api/state", headers=headers, json=body).status_code == 409
    assert repository.get("user-a").version == 1
    other = {
        "Authorization": "Bearer " + access_token(private_key, "user-b"),
        "X-User-Id": "user-a",
    }
    assert client.get("/api/state", headers=other).json() == {"version": 0, "snapshot": None}
    assert client.get("/api/state", headers=headers).json()["version"] == 1


def test_state_rejects_unknown_private_fields_without_echo(
    client: HttpTestClient, private_key: rsa.RSAPrivateKey, snapshot: AppSnapshot
) -> None:
    body = snapshot.model_dump(by_alias=True)
    body["rawOcr"] = "private receipt customer phone 090"
    headers = {"Authorization": "Bearer " + access_token(private_key)}
    response = client.put(
        "/api/state", headers=headers, json={"expectedVersion": 0, "snapshot": body}
    )
    assert response.status_code == 422
    assert "private receipt" not in response.text


def test_body_limit_precedes_validation(
    client: HttpTestClient, private_key: rsa.RSAPrivateKey
) -> None:
    response = client.put(
        "/api/state",
        content=b"x" * (1048576 + 1),
        headers={"Authorization": "Bearer " + access_token(private_key)},
    )
    assert response.status_code == 413
