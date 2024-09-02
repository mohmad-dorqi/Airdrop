

# 🎮 AirdropBot API Documentation

Welcome to the **AirdropBot API** documentation! 🚀 This API lets you manage tasks, users, and rewards within your AirdropBot application. Get ready to supercharge your bot with some awesome features! 💪

## 🌟 Getting Started

To dive in, make sure your AirdropBot application is up and running. The API is powered by Flask ⚙️ and SQLAlchemy 🛠️.

## 🔥 Endpoints

### 🎬 Cinema Tasks

#### ➕ Add a Cinema Task
- **URL:** `/api/cinema-tasks`
- **Method:** `POST`
- **Description:** Create a new cinema task! 🍿
- **Request Body:**
  ```json
  {
    "title": "Task Title",
    "description": "Task Description",
    "youtube_link": "https://youtube.com/example",
    "code": "CODE123",
    "slug": "task-slug",
    "social": "YouTube"
  }
  ```
- **Response:** 🎉
  ```json
  {
    "message": "Cinema task added successfully"
  }
  ```

#### 🔍 Get a Cinema Task
- **URL:** `/api/cinema-tasks/<string:slug>`
- **Method:** `GET`
- **Description:** Fetch details of a cinema task by its slug 🎥.
- **Response:** 📄
  ```json
  {
    "title": "Task Title",
    "description": "Task Description",
    "youtube_link": "https://youtube.com/example",
    "code": "CODE123",
    "social": "YouTube"
  }
  ```

### 🎥 Live Tasks

#### ➕ Add a Live Task
- **URL:** `/api/live-tasks`
- **Method:** `POST`
- **Description:** Create a new live task! 📡
- **Request Body:**
  ```json
  {
    "title": "Live Task Title",
    "description": "Task Description",
    "code": "LIVE123",
    "max_claims": 100,
    "coins_reward": 50,
    "social": "Instagram"
  }
  ```
- **Response:** 🥳
  ```json
  {
    "message": "Live task added successfully"
  }
  ```

#### 🏆 Claim a Live Task
- **URL:** `/api/live-task/<string:code>/claim`
- **Method:** `POST`
- **Description:** Claim a live task using its code! 🏅
- **Response:** 💰
  ```json
  {
    "message": "Task claimed successfully",
    "reward": 50
  }
  ```

#### 👥 Get Users Who Claimed a Live Task
- **URL:** `/api/live-task/<string:code>/claimed-users`
- **Method:** `GET`
- **Description:** See who claimed a specific live task! 🕵️‍♂️
- **Response:** 📃
  ```json
  [
    {
      "username": "user1",
      "wallet_address": "0x1234567890abcdef"
    },
    ...
  ]
  ```

### 📺 Channel Tasks

#### ➕ Add a Channel Task
- **URL:** `/api/channel-tasks`
- **Method:** `POST`
- **Description:** Create a new channel task! 📺
- **Request Body:**
  ```json
  {
    "channel_name": "Channel Name",
    "channel_link": "https://t.me/channel",
    "coins_reward": 30,
    "social": "Telegram"
  }
  ```
- **Response:** 🎉
  ```json
  {
    "message": "Channel task added successfully"
  }
  ```

### 👥 Referral Tasks

#### ➕ Add a Referral Task
- **URL:** `/api/referral-tasks`
- **Method:** `POST`
- **Description:** Set up a new referral task! 📈
- **Request Body:**
  ```json
  {
    "required_referrals": 5,
    "coins_reward": 100,
    "social": "Facebook"
  }
  ```
- **Response:** 🚀
  ```json
  {
    "message": "Referral task added successfully"
  }
  ```

### 📊 User Management

#### 🔍 Get User Information
- **URL:** `/api/user/<int:user_id>`
- **Method:** `GET`
- **Description:** Retrieve information about a user! 👤
- **Response:** 📄
  ```json
  {
    "id": 1,
    "username": "user1",
    "coins": 100,
    ...
  }
  ```

#### 🛠️ Update User Information
- **URL:** `/api/user/<int:user_id>`
- **Method:** `POST`
- **Description:** Update user information! ✏️
- **Request Body:**
  ```json
  {
    "wallet_address": "0x1234567890abcdef",
    "coins": 200
  }
  ```
- **Response:** 📝
  ```json
  {
    "message": "User updated successfully"
  }
  ```

### 📱 Advertisements

#### ➕ Add an Advertisement
- **URL:** `/api/ads`
- **Method:** `POST`
- **Description:** Create a new advertisement! 📢
- **Request Body:**
  ```json
  {
    "link": "https://example.com",
    "text": "Check out this awesome product!",
    "is_english": true
  }
  ```
- **Response:** 📣
  ```json
  {
    "message": "Advertisement added successfully"
  }
  ```

#### 🔍 Get All Advertisements
- **URL:** `/api/ads`
- **Method:** `GET`
- **Description:** Fetch all the ads available! 📰
- **Response:** 📄
  ```json
  [
    {
      "id": 1,
      "link": "https://example.com",
      "text": "Check out this awesome product!",
      "is_english": true
    },
    ...
  ]
  ```

### 🕹️ 2048 Game Management

#### 🔄 Reset 2048 Scores
- **URL:** `/api/2048/reset-scores`
- **Method:** `POST`
- **Description:** Reset all users' 2048 scores to zero! 🚫
- **Response:** 🔁
  ```json
  {
    "message": "All 2048 scores have been reset to 0"
  }
  ```

#### 🏆 Get Top 2048 Scores
- **URL:** `/api/2048/top-scores`
- **Method:** `GET`
- **Description:** View the top 10 scores in the 2048 game! 🎮
- **Response:** 🥇
  ```json
  [
    {
      "id": 1,
      "username": "player1",
      "score": 10000
    },
    ...
  ]
  ```

### ⏳ Pending Tasks

#### 🔍 Get Pending Tasks
- **URL:** `/api/pending-tasks`
- **Method:** `GET`
- **Description:** Fetch all pending tasks (cinema, live, channel, and referral tasks)! 📋
- **Response:** 🕑
  ```json
  {
    "cinema_tasks": [...],
    "live_tasks": [...],
    "channel_tasks": [...],
    "referral_tasks": [...]
  }
  ```

## 📅 Current Server Time

#### ⏰ Get Current Server Time
- **URL:** `/api/current_time`
- **Method:** `GET`
- **Description:** Get the current server time! 🕒
- **Response:** ⏳
  ```json
  {
    "server_time": "2024-08-21 12:34:56"
  }
  ```

## 🏆 Leaderboards

### 👑 Top Users by Coins
- **URL:** `/api/top-coins`
- **Method:** `GET`
- **Description:** See the top 10 users by their coin count! 💰
- **Response:** 🥇
  ```json
  [
    {
      "id": 1,
      "username": "user1",
      "coins": 1000
    },
    ...
  ]
  ```

### 🏅 Top Users by Referrals
- **URL:** `/api/top-referrals`
- **Method:** `GET`
- **Description:** See the top 10 users by their number of referrals! 🔗
- **Response:** 🥈
  ```json
  [
    {
      "id": 1,
      "username": "user1",
      "referred_count": 50
    },
    ...
  ]
  ```

## 🔧 Examples

### 📹 Example: Add a Cinema Task
```bash
curl -X POST http://localhost:8080/api/cinema-tasks \
-H "Content-Type: application/json" \
-d '{
  "title": "Watch this awesome video",
  "description": "Watch the video and use the code",
  "youtube_link": "https://youtube.com/example",
  "code": "VIDEO2024",
  "slug": "watch-awesome-video",
  "social": "YouTube"
}'
```

### 🏅 Example: Claim a Live Task
```bash
curl -X POST http://localhost:8080/api/live-task/LIVE123/claim


```

### 🔄 Example: Reset 2048 Scores
```bash
curl -X POST http://localhost:8080/api/2048/reset-scores
```

### 🏆 Example: Get Top 2048 Scores
```bash
curl http://localhost:8080/api/2048/top-scores
```

## 📄 License

This project is licensed under the MIT License. 📝
