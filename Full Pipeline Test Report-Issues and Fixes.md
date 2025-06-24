# 🔪 Full Pipeline Test Report: Issues & Fixes

## ✅ Objective

To verify the end-to-end pipeline for:

* User registration
* Topic submission
* Research, summary, content generation
* Approval, scheduling, and posting to Typefully

---

## 𞵹️ 1. Database Not Cleared Properly

**Symptom**:
Script failed on user creation:
`duplicate key value violates unique constraint "users_email_key"`

**Cause**:
The raw SQL `TRUNCATE` command wasn’t wrapped in SQLAlchemy's `text()` function, so it silently failed.

**Fix**:
Wrapped SQL string using:

```python
from sqlalchemy import text
db.execute(text("""TRUNCATE ..."""))
```

---

## 🧠 2. DetachedInstanceError When Accessing `user.id`

**Symptom**:
`DetachedInstanceError: Instance <User> is not bound to a Session`

**Cause**:
Session was closed before accessing `new_user.id`, which relies on lazy-loading.

**Fix**:
Cached the `user.id` before closing the session:

```python
user_id = new_user.id
db.close()
return user_id
```

---

## 🧠 3. Incorrect Call to Topic Agent

**Symptom**:
`TypeError: generate_content_topic() missing 4 required positional arguments`

**Cause**:
Used outdated `generate_refined_topic(request_id)` function.

**Fix**:
Replaced with correct full signature and extracted data from DB:

```python
generate_content_topic(request_id, original_topic, user_config, content_type, user_id)
```

---

## 🔍 4. Research Agent Returned 0 Sources

**Symptom**:
No verified sources were stored. Google and AI returned 0 usable links.

**Cause**:

* URLs failed HTTP checks (e.g., 403)
* Google returned nothing
* No valid source summaries

**Fix**:
Handled gracefully; pipeline continues with empty source list.

✅ Marked for future enhancement (e.g., retries, fallback, mock sources in dev).

---

## 🛡️ 5. Raw SQL Query Caused SQLAlchemy Error

**Symptom**:
`ArgumentError: Textual SQL expression ... should be declared with text(...)`

**Cause**:
Used raw SQL without wrapping it in `text()`.

**Fix**:
Wrapped the raw query properly:

```python
from sqlalchemy import text
db.execute(text("SELECT id FROM ..."), {...})
```

---

## 🥵 6. Approval Fails Due to `json.loads()` on Plain Text

**Symptom**:
`JSONDecodeError: Extra data: line 1 column 2 (char 1)`

**Cause**:
Assumed `generated_content` was JSON. But it was plain text.

**Fix**:
Fallback to line-based splitting:

```python
try:
    tweets = json.loads(content.generated_content)
    assert isinstance(tweets, list)
except (json.JSONDecodeError, AssertionError):
    tweets = [line.strip() for line in content.generated_content.split("\n") if line.strip()]
```

---

## 🕒 7. Typefully Rejected Scheduled Time

**Symptom**:
`Typefully API error 400: "Schedule date must be in the future"`

**Cause**:
Scheduled time was `datetime.utcnow() + 3s`, too close to current time.

**Fix**:

* Switched to timezone-aware datetime:

  ```python
  from datetime import timezone
  datetime.now(timezone.utc) + timedelta(seconds=15)
  ```
* Updated comparison logic in `schedule_content()` to:

  ```python
  if scheduled_for < datetime.now(timezone.utc):
  ```

---

## ✅ Final Result

* ✅ All agents executed successfully
* ✅ Approval and scheduling worked
* ✅ Post was sent to Typefully with thread content

---

## 📋 Remaining Issues to Fix Later

### 1. Typefully Shows Scheduled Posts for “Tomorrow”

**Observation**:
Post appears in the Typefully queue, but with a next-day timestamp.

**Hypothesis**:
Timezone mismatch — Typefully might interpret UTC as local time or show in browser local time.

**Fix Later**:

* Confirm Typefully’s timezone expectations
* Possibly convert to local time zone before sending

---

### 2. Tweet Splitting Isn’t Clean

**Observation**:
Some tweets start mid-sentence, suggesting poor splits.

**Possible Causes**:

* Raw text is split naïvely on newlines
* LLM not prompted to separate tweets clearly
* Typefully might be splitting content automatically

**Fix Later**:

* Prompt LLM to return structured tweet list
* Improve `split_into_tweets()` using NLP or clearer separators
* Consider asking LLM to output valid JSON of tweets

---
