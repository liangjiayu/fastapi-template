import uuid


async def test_create_conversation(client):
	response = await client.post(
		"/api/conversations/",
		json={
			"user_id": "user_1",
			"title": "Test Chat",
			"model_name": "gpt-4",
		},
	)
	data = response.json()
	assert response.status_code == 200
	assert data["code"] == 200
	assert data["data"]["user_id"] == "user_1"
	assert data["data"]["title"] == "Test Chat"
	assert data["data"]["model_name"] == "gpt-4"
	assert "id" in data["data"]
	assert "created_at" in data["data"]
	assert "updated_at" in data["data"]


async def test_get_conversation(client):
	# 创建对话
	res = await client.post(
		"/api/conversations/",
		json={"user_id": "user_1", "title": "Chat 1"},
	)
	conversation_id = res.json()["data"]["id"]

	# 获取对话
	res = await client.get(f"/api/conversations/{conversation_id}")
	data = res.json()
	assert res.status_code == 200
	assert data["code"] == 200
	assert data["data"]["id"] == conversation_id
	assert data["data"]["title"] == "Chat 1"


async def test_get_conversations(client):
	# 创建两个对话
	await client.post(
		"/api/conversations/",
		json={"user_id": "user_1", "title": "Chat 1"},
	)
	await client.post(
		"/api/conversations/",
		json={"user_id": "user_2", "title": "Chat 2"},
	)

	# 获取对话列表
	res = await client.get("/api/conversations/")
	data = res.json()
	assert res.status_code == 200
	assert data["code"] == 200
	assert data["data"]["total"] == 2
	assert len(data["data"]["list"]) == 2


async def test_get_conversations_filter_by_user_id(client):
	# 为 user_1 创建 2 个对话
	for i in range(2):
		await client.post(
			"/api/conversations/",
			json={"user_id": "user_1", "title": f"Chat {i}"},
		)

	# 为 user_2 创建 1 个对话
	await client.post(
		"/api/conversations/",
		json={"user_id": "user_2", "title": "Other chat"},
	)

	# 按 user_id 过滤
	res = await client.get("/api/conversations/", params={"user_id": "user_1"})
	data = res.json()
	assert res.status_code == 200
	assert data["code"] == 200
	assert data["data"]["total"] == 2
	assert len(data["data"]["list"]) == 2
	for item in data["data"]["list"]:
		assert item["user_id"] == "user_1"


async def test_update_conversation(client):
	# 创建对话
	res = await client.post(
		"/api/conversations/",
		json={"user_id": "user_1", "title": "Original Title"},
	)
	conversation_id = res.json()["data"]["id"]

	# 更新对话
	res = await client.put(
		f"/api/conversations/{conversation_id}",
		json={"title": "Updated Title"},
	)
	data = res.json()
	assert res.status_code == 200
	assert data["code"] == 200
	assert data["data"]["title"] == "Updated Title"
	assert data["data"]["user_id"] == "user_1"


async def test_delete_conversation(client):
	# 创建对话
	res = await client.post(
		"/api/conversations/",
		json={"user_id": "user_1", "title": "To Delete"},
	)
	conversation_id = res.json()["data"]["id"]

	# 删除对话
	res = await client.delete(f"/api/conversations/{conversation_id}")
	assert res.json()["code"] == 200

	# 验证已删除
	res = await client.get(f"/api/conversations/{conversation_id}")
	assert res.json()["code"] == 404


async def test_get_conversation_not_found(client):
	fake_uuid = str(uuid.uuid4())
	res = await client.get(f"/api/conversations/{fake_uuid}")
	data = res.json()
	assert res.status_code == 404
	assert data["code"] == 404
