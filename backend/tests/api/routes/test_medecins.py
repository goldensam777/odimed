from fastapi.testclient import TestClient

from app.core.config import settings


def test_create_and_get_medecin_profil(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    # 1. Créer profil médecin
    profil_data = {
        "numero_ordre": "MED-123456",
        "specialite": "Médecine Générale",
        "pays_exercice": "Bénin",
        "bio": "Médecin généraliste d'expérience",
    }
    response = client.post(
        f"{settings.API_V1_STR}/medecins/me",
        headers=normal_user_token_headers,
        json=profil_data,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["numero_ordre"] == "MED-123456"
    assert data["specialite"] == "Médecine Générale"

    # 2. Récupérer le profil créé
    get_response = client.get(
        f"{settings.API_V1_STR}/medecins/me",
        headers=normal_user_token_headers,
    )
    assert get_response.status_code == 200
    assert get_response.json()["id"] == data["id"]
