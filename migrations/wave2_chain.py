"""Add Dalga 2 tables without rewriting existing rows.

Usage: python -m migrations.wave2_chain sqlite:///path/to/copy.db
Run against a backed-up database during deployment. Re-running is safe.
"""
import sys
from sqlalchemy import create_engine
import models

TABLES = (
    "work_areas", "contracts", "contract_lines", "field_measurements",
    "measurement_evidence", "measurement_decisions", "payment_contracts", "payment_allocations", "payment_decisions",
    "inventory_movements",
)


def upgrade(engine):
    for name in TABLES:
        models.Base.metadata.tables[name].create(engine, checkfirst=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m migrations.wave2_chain DATABASE_URL")
    upgrade(create_engine(sys.argv[1]))
