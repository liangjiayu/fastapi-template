-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE
);

CREATE INDEX ix_users_username ON users (username);
CREATE INDEX ix_users_email ON users (email);

-- 会话表
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    title VARCHAR(255),
    model_name VARCHAR(50),
    extra_data JSONB, -- 存储模型配置如 temp, top_p
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_conversations_user_id ON conversations (user_id);

-- 消息表
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- system, user, assistant
    content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'success', -- processing, success, error
    extra_data JSONB, -- 存储思考过程、Token 消耗等
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_messages_conversation_id ON messages (conversation_id);
