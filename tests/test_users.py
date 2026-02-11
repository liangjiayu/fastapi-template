async def test_create_user(client):
	response = await client.post(
		"/api/users/",
		json={"username": "alice", "email": "alice@example.com"},
	)
	data = response.json()
	assert response.status_code == 200
	assert data["code"] == 200
	assert data["data"]["username"] == "alice"
	assert data["data"]["email"] == "alice@example.com"
	assert isinstance(data["data"]["id"], int)


async def test_get_user(client):
	# 先创建用户
	res = await client.post(
		"/api/users/",
		json={"username": "bob", "email": "bob@example.com"},
	)
	user_id = res.json()["data"]["id"]

	# 获取用户
	res = await client.get(f"/api/users/{user_id}")
	data = res.json()
	assert res.status_code == 200
	assert data["code"] == 200
	assert data["data"]["username"] == "bob"
	assert data["data"]["email"] == "bob@example.com"


async def test_get_users(client):
	# 创建两个用户
	await client.post(
		"/api/users/",
		json={"username": "user1", "email": "user1@example.com"},
	)
	await client.post(
		"/api/users/",
		json={"username": "user2", "email": "user2@example.com"},
	)

	# 获取用户列表
	res = await client.get("/api/users/")
	data = res.json()
	assert res.status_code == 200
	assert data["code"] == 200
	assert data["data"]["total"] == 2
	assert len(data["data"]["list"]) == 2
	assert data["data"]["page"] == 1


async def test_update_user(client):
	# 创建用户
	res = await client.post(
		"/api/users/",
		json={"username": "charlie", "email": "charlie@example.com"},
	)
	user_id = res.json()["data"]["id"]

	# 更新用户
	res = await client.put(
		f"/api/users/{user_id}",
		json={"username": "charlie_updated"},
	)
	data = res.json()
	assert res.status_code == 200
	assert data["code"] == 200
	assert data["data"]["username"] == "charlie_updated"
	assert data["data"]["email"] == "charlie@example.com"


async def test_delete_user(client):
	# 创建用户
	res = await client.post(
		"/api/users/",
		json={"username": "dave", "email": "dave@example.com"},
	)
	user_id = res.json()["data"]["id"]

	# 删除用户
	res = await client.delete(f"/api/users/{user_id}")
	assert res.json()["code"] == 200

	# 验证已删除
	res = await client.get(f"/api/users/{user_id}")
	assert res.json()["code"] == 404


async def test_create_user_duplicate_username(client):
	# 创建第一个用户
	await client.post(
		"/api/users/",
		json={"username": "duplicate", "email": "first@example.com"},
	)

	# 尝试创建相同 username 的用户
	res = await client.post(
		"/api/users/",
		json={"username": "duplicate", "email": "second@example.com"},
	)
	data = res.json()
	assert res.status_code == 400
	assert data["code"] == 400
	assert "already exists" in data["msg"]


async def test_get_user_not_found(client):
	res = await client.get("/api/users/9999")
	data = res.json()
	assert res.status_code == 404
	assert data["code"] == 404
