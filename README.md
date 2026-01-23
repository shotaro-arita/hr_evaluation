# HR Evaluation App

人事評価フロー（自己評価 → 管理者評価）を想定した、評価シート作成・入力・閲覧を行うサンプルアプリです。  
ポートフォリオ用途として、UI/UX設計、型設計、API連携、権限切り替えの実装をまとめています。

## Features
- 社員コード + パスワードによるJWTログイン
- 評価期間の取得と、対象社員の評価シート一覧表示
- 自己評価/管理者評価の入力とステータス更新（下書き・確定）
- 管理者は評価対象社員の切り替えが可能

## Tech Stack
- Frontend: React 19, TypeScript, Vite, MUI, React Router
- Backend: Django 6, Django REST Framework, SimpleJWT
- DB: PostgreSQL 16 (Docker), SQLite (ローカルのデフォルト)
- Infra: Docker Compose

## Structure
```
.
├─ backend/    # Django API + Domain/Usecase/Adapter構成
├─ frontend/   # React + MUI のSPA
└─ docker-compose.yml
```

## Local Setup (Docker)
```
docker compose up --build
```

## Environment Variables (Backend)
開発時は `backend/.env` を用意します。
```
cp backend/.env.example backend/.env
```
必須:
- `DJANGO_SECRET_KEY`
任意:
- `DJANGO_DEBUG`（`True` or `False`。未設定は `False`）

初回のみDBマイグレーションとサンプルデータ投入:
```
docker compose exec web python manage.py migrate

docker compose exec web python manage.py import_employee /app/evaluations/fixtures/employee_sample.json
docker compose exec web python manage.py import_user /app/evaluations/fixtures/user_sample.json
docker compose exec web python manage.py import_period /app/evaluations/fixtures/period_sample.json
docker compose exec web python manage.py import_evaluation_item /app/evaluations/fixtures/evaluation_item_sample.json
docker compose exec web python manage.py import_evaluation_item_position_relation /app/evaluations/fixtures/evaluation_item_position_relation_sample.json
docker compose exec web python manage.py import_evaluation_assignment /app/evaluations/fixtures/evaluation_assignment_sample.json
```

起動後アクセス:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## Sample Login
`backend/evaluations/fixtures/user_sample.json` のユーザーでログインできます。  
例: `employee_code = E0002`, `password = password123`

## API Overview
- `POST /api/token/` : JWT発行
- `GET /api/evaluations/users/` : 自分のプロフィール取得
- `GET /api/evaluations/periods/` : 評価期間一覧
- `GET /api/evaluations/evaluation_assignments/` : 管理者の評価対象一覧
- `GET /api/evaluations/evaluation_sheets/?employee_id=...` : 評価シート一覧
- `GET /api/evaluations/evaluation_sheets/{uuid}/` : 評価シート詳細
- `PUT /api/evaluations/evaluation_sheets/{uuid}/update_own/` : 自己評価更新
- `PUT /api/evaluations/evaluation_sheets/{uuid}/update_by_manager/` : 管理者評価更新

## Notes
- フロントは `/api` へのリクエストをViteのプロキシで `web:8000` に転送しています。
- バックエンドはDomain/Usecase/Adapter/Infrastructureのレイヤ構成で、責務分割を意識しています。
