from uuid import uuid4

from sqlalchemy import text


def create_test_user(db_session, login: str, senha: str):
    db_session.execute(
        text(
            """
            INSERT INTO validade_login (login, senha, loja, business, whatsapp)
            VALUES (:login, :senha, :loja, :business, :whatsapp)
            """
        ),
        {
            "login": login,
            "senha": senha,
            "loja": "TESTE",
            "business": True,
            "whatsapp": None,
        },
    )
    db_session.commit()


def delete_test_user(db_session, login: str):
    db_session.execute(
        text("DELETE FROM validade_login WHERE login = :login"),
        {"login": login},
    )
    db_session.commit()


def test_login_succeeds(client, db_session):
    login = f"teste_{uuid4().hex}@exemplo.com"
    senha = "Senha123"
    create_test_user(db_session, login, senha)

    try:
        response = client.post(
            "/auth/login",
            json={"email": login, "senha": senha},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == login
        assert data["loja"] == "TESTE"
        assert data["business"] is True
        assert "id" in data
        assert "criado_em" in data
        assert "expira_em" in data
    finally:
        delete_test_user(db_session, login)


def test_login_fails_with_wrong_password(client, db_session):
    login = f"teste_{uuid4().hex}@exemplo.com"
    senha = "Senha123"
    create_test_user(db_session, login, senha)

    try:
        response = client.post(
            "/auth/login",
            json={"email": login, "senha": "senha_errada"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Email ou senha inválidos"
    finally:
        delete_test_user(db_session, login)


def test_login_fails_with_unknown_user(client):
    response = client.post(
        "/auth/login",
        json={"email": f"desconhecido_{uuid4().hex}@exemplo.com", "senha": "Senha123"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou senha inválidos"


def test_signup_succeeds(client, db_session):
    email = f"novo_{uuid4().hex}@exemplo.com"
    response = client.post(
        "/auth/signup",
        json={
            "email": email,
            "senha": "Senha123",
            "loja": "TESTE",
            "business": True,
            "whatsapp": None,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["loja"] == "TESTE"
    assert data["business"] is True
    assert data["whatsapp"] is None
    assert "criado_em" in data
    assert "expira_em" in data

    delete_test_user(db_session, email)


def test_signup_fails_when_email_exists(client, db_session):
    email = f"duplicado_{uuid4().hex}@exemplo.com"

    response_one = client.post(
        "/auth/signup",
        json={
            "email": email,
            "senha": "Senha123",
            "loja": "TESTE",
            "business": True,
            "whatsapp": None,
        },
    )
    assert response_one.status_code == 200

    response_two = client.post(
        "/auth/signup",
        json={
            "email": email,
            "senha": "Senha123",
            "loja": "TESTE",
            "business": True,
            "whatsapp": None,
        },
    )

    assert response_two.status_code == 409
    assert response_two.json()["detail"] == "Email already registered"

    delete_test_user(db_session, email)


# --------------------------------------------------
# Testes de cadastro
# --------------------------------------------------
#
# Quando começar o cadastro, os testes devem cobrir pelo menos:
# - cadastro com sucesso
# - cadastro com login já existente
# - cadastro com dados inválidos
#
# A estrutura deve seguir o mesmo padrão do login:
# - criar usuário temporário, se necessário
# - chamar a rota real
# - validar status code e resposta
# - limpar os dados no final
