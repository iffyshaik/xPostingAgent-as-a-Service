# Database Schema Reference

## Users Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  subscription_tier VARCHAR(50) DEFAULT 'free',
  api_quota_daily INTEGER DEFAULT 5,
  api_quota_used_today INTEGER DEFAULT 0,
  quota_reset_date DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## UserConfigurations Table
```sql
CREATE TABLE user_configurations (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  persona TEXT DEFAULT 'Professional and engaging',
  tone VARCHAR(100) DEFAULT 'informative',
  style VARCHAR(100) DEFAULT 'conversational',
  language VARCHAR(10) DEFAULT 'en',
  default_source_count INTEGER DEFAULT 5,
  research_preference VARCHAR(50) DEFAULT 'balanced',
  platform_preference VARCHAR(20) DEFAULT 'typefully',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## Requests Table
```sql
CREATE TABLE requests (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  original_topic TEXT NOT NULL,
  content_topic TEXT,
  status VARCHAR(50) DEFAULT 'pending',
  content_type VARCHAR(20) NOT NULL,
  auto_post BOOLEAN DEFAULT FALSE,
  source_count_limit INTEGER DEFAULT 5,
  thread_tweet_count INTEGER,
  max_article_length INTEGER,
  include_source_citations BOOLEAN DEFAULT FALSE,
  citation_count INTEGER DEFAULT 1,
  platform VARCHAR(20) DEFAULT 'typefully',
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## ResearchSources Table
```sql
CREATE TABLE research_sources (
  id SERIAL PRIMARY KEY,
  request_id INTEGER REFERENCES requests(id) ON DELETE CASCADE,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  source_type VARCHAR(20) NOT NULL,
  url TEXT,
  title TEXT,
  author TEXT,
  publication_date DATE,
  source_domain VARCHAR(255),
  verification_status VARCHAR(20) DEFAULT 'pending',
  relevance_score DECIMAL(3,2),
  freshness_score DECIMAL(3,2),
  summary TEXT,
  key_points TEXT[],
  is_used BOOLEAN DEFAULT FALSE,
  verification_attempts INTEGER DEFAULT 0,
  last_verified_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## TopicSourceUsage Table
```sql
CREATE TABLE topic_source_usage (
  id SERIAL PRIMARY KEY,
  content_topic_hash VARCHAR(64),
  source_url_hash VARCHAR(64),
  usage_count INTEGER DEFAULT 1,
  last_used_at TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(content_topic_hash, source_url_hash)
);
```

## Summaries Table
```sql
CREATE TABLE summaries (
  id SERIAL PRIMARY KEY,
  request_id INTEGER REFERENCES requests(id) ON DELETE CASCADE,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  combined_summary TEXT NOT NULL,
  combined_key_points TEXT[] NOT NULL,
  source_count INTEGER NOT NULL,
  is_used BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## ContentQueue Table
```sql
CREATE TABLE content_queue (
  id SERIAL PRIMARY KEY,
  request_id INTEGER REFERENCES requests(id) ON DELETE CASCADE,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  content_type VARCHAR(20) NOT NULL,
  generated_content TEXT NOT NULL,
  status VARCHAR(20) DEFAULT 'draft',
  scheduled_for TIMESTAMP,
  platform VARCHAR(20) NOT NULL,
  post_response TEXT,
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  posted_at TIMESTAMP
);
```

## ThreadMetadata Table
```sql
CREATE TABLE thread_metadata (
  id SERIAL PRIMARY KEY,
  content_queue_id INTEGER REFERENCES content_queue(id) ON DELETE CASCADE,
  requested_tweet_count INTEGER NOT NULL,
  actual_tweet_count INTEGER NOT NULL,
  max_tweet_length INTEGER DEFAULT 280,
  thread_structure JSONB NOT NULL,
  citation_tweets JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## UserSessions Table
```sql
CREATE TABLE user_sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  token_hash VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

> **Use this as a reference for implementing models, migrations, and data layer tests.**
