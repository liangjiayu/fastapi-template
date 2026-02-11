import uuid


async def _create_conversation(client):
	"""辅助函数：创建对话并返回其 UUID"""
	res = await client.post(
		"/api/conversations/",
		json={"user_id": "test_user", "title": "Test Conversation"},
	)
	return res.json()["data"]["id"]


async def test_create_message(client):
	# 先创建对话
	conversation_id = await _create_conversation(client)

	# 创建消息
	response = await client.post(
		"/api/messages/",
		json={
			"conversation_id": conversation_id,
			"role": "user",
			"content": "Hello",
		},
	)
	data = response.json()
	assert response.status_code == 200
	assert data["code"] == 200
	assert data["data"]["role"] == "user"
	assert data["data"]["content"] == "Hello"
	assert data["data"]["status"] == "success"
	assert "id" in data["data"]


async def test_get_message(client):
	# 创建对话和消息
	conversation_id = await _create_conversation(client)
	res = await client.post(
		"/api/messages/",
		json={
			"conversation_id": conversation_id,
			"role": "assistant",
			"content": "Hi there",
		},
	)
	message_id = res.json()["data"]["id"]

	# 获取消息
	res = await client.get(f"/api/messages/{message_id}")
	data = res.json()
	assert res.status_code == 200
	assert data["code"] == 200
	assert data["data"]["id"] == message_id
	assert data["data"]["content"] == "Hi there"


async def test_get_messages_by_conversation(client):
	# 创建对话
	conversation_id = await _create_conversation(client)

	# 创建两条消息
	await client.post(
		"/api/messages/",
		json={
			"conversation_id": conversation_id,
			"role": "user",
			"content": "First message",
		},
	)
	await client.post(
		"/api/messages/",
		json={
			"conversation_id": conversation_id,
			"role": "assistant",
			"content": "Second message",
		},
	)

	# 获取对话的消息列表
	res = await client.get(f"/api/messages/conversation/{conversation_id}")
	data = res.json()
	assert res.status_code == 200
	assert data["code"] == 200
	assert data["data"]["total"] == 2
	assert len(data["data"]["list"]) == 2


async def test_update_message(client):
	# 创建对话和消息
	conversation_id = await _create_conversation(client)
	res = await client.post(
		"/api/messages/",
		json={
			"conversation_id": conversation_id,
			"role": "user",
			"content": "Original content",
		},
	)
	message_id = res.json()["data"]["id"]

	# 更新消息
	res = await client.put(
		f"/api/messages/{message_id}",
		json={"content": "Updated content", "status": "error"},
	)
	data = res.json()
	assert res.status_code == 200
	assert data["code"] == 200
	assert data["data"]["content"] == "Updated content"
	assert data["data"]["status"] == "error"


async def test_delete_message(client):
	# 创建对话和消息
	conversation_id = await _create_conversation(client)
	res = await client.post(
		"/api/messages/",
		json={
			"conversation_id": conversation_id,
			"role": "user",
			"content": "To delete",
		},
	)
	message_id = res.json()["data"]["id"]

	# 删除消息
	res = await client.delete(f"/api/messages/{message_id}")
	assert res.json()["code"] == 200

	# 验证已删除
	res = await client.get(f"/api/messages/{message_id}")
	assert res.json()["code"] == 404


async def test_create_message_invalid_conversation(client):
	# 使用不存在的对话 ID
	fake_conversation_id = str(uuid.uuid4())
	res = await client.post(
		"/api/messages/",
		json={
			"conversation_id": fake_conversation_id,
			"role": "user",
			"content": "Hello",
		},
	)
	data = res.json()
	assert res.status_code == 404
	assert data["code"] == 404
	assert "Conversation not found" in data["msg"]


async def test_get_message_not_found(client):
	fake_uuid = str(uuid.uuid4())
	res = await client.get(f"/api/messages/{fake_uuid}")
	data = res.json()
	assert res.status_code == 404
	assert data["code"] == 404
