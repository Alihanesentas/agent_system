import os
from datetime import datetime
from peewee import (
    SqliteDatabase, Model, CharField, TextField, 
    IntegerField, FloatField, DateTimeField, ForeignKeyField
)

DB_PATH = os.path.join(os.path.dirname(__file__), "tracker.db")
db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

class BenchmarkSession(BaseModel):
    """Tracks a test run / development iteration to compare token efficiency."""
    name = CharField(index=True)
    description = TextField(null=True)
    version_tag = CharField(default="v1.0")  # e.g., 'v1-baseline', 'v2-optimized-prompt'
    created_at = DateTimeField(default=datetime.now)

class AgentLog(BaseModel):
    """Stores token, timing, and payload details for each agent call."""
    agent_name = CharField(index=True)
    model_name = CharField(index=True)
    input_text = TextField()
    output_text = TextField()
    prompt_tokens = IntegerField(default=0)
    completion_tokens = IntegerField(default=0)
    total_tokens = IntegerField(default=0)
    estimated_cost_usd = FloatField(default=0.0)
    execution_time_ms = FloatField(default=0.0)
    status = CharField(default="success")  # 'success', 'error'
    session = ForeignKeyField(BenchmarkSession, backref="logs", null=True, on_delete="SET NULL")
    created_at = DateTimeField(default=datetime.now)

def init_db():
    db.connect(reuse_if_open=True)
    db.create_tables([BenchmarkSession, AgentLog])

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DB_PATH)
