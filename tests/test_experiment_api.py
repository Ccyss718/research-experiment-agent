# 测试创建实验
def test_create_experiment_api(client):
    response = client.post(
        "/experiments/",
        json={
            "name": "API test experiment",
            "description": "Created through TestClient",
            "hypothesis": "The API should create an experiment",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "API test experiment"
    assert body["status"] == "planned"
    assert isinstance(body["id"], int)

# 不存在的实验返回404
def test_get_missing_experiment_returns_404(client):
    response = client.get("/experiments/99999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Experiment not found"
    }

# 创建后查询详细
def test_get_experiment_by_id(client):
    create_response = client.post(
        "/experiments/",
        json={
            "name": "Detail API test",
            "description": "Used for detail query"
        }
    )

    assert create_response.status_code == 201

    created = create_response.json()
    experiment_id = created["id"]

    response = client.get(f"/experiments/{experiment_id}")

    assert response.status_code == 200
    assert response.json()["id"] == experiment_id
    assert response.json()["name"] == "Detail API test"

# 测试实验列表接口
def test_list_experiments(client):
    client.post(
        "/experiments/",
        json={
            "name": "List experiment A"
        }
    )
    client.post(
        "/experiments/",
        json={
            "name": "List experiment B"
        }
    )

    response = client.get("/experiments")

    assert response.status_code == 200

    items = response.json()

    assert len(items) == 2
    assert items[0]["name"] == "List experiment A"
    assert items[1]["name"] == "List experiment B"

# 测试update
def test_update_experiment_api(client):
    create_response = client.post(
        "/experiments/",
        json={
            "name": "Original API experiment",
            "description": "Origin"
        }
    )

    experiment_id = create_response.json()["id"]

    response = client.patch(
        f"/experiments/{experiment_id}",
        json={
            "name": "Updated API experiment",
            "status": "running"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == experiment_id
    assert body["name"] == "Updated API experiment"
    assert body["status"] == "running"
    assert body["description"] == "Origin"

# 测试delete
def test_delete_experiment_api(client):
    create_response = client.post(
        "/experiments/",
        json={
            "name": "Delete API experiment"
        }
    )

    experiment_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/experiments/{experiment_id}"
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(
        f"/experiments/{experiment_id}"
    )

    assert get_response.status_code == 404

def test_create_experiment_with_blank_name_returns_422(client):
    response = client.post(
        "/experiments/",
        json={
            "name": "   ",
            "description": "Invalid request",
        },
    )

    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)