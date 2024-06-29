alembic init -t async alembic

### 升级

alembic upgrade head

### 创建

alembic revision --autogenerate -m "init"

### 回退

alembic  downgrade
