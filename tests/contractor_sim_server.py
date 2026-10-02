"""Isolated old-UI simulation server; never connects to the workspace database."""
import os
import sys
from pathlib import Path

os.environ['BUILDINGAI_SCHEDULER'] = '0'
os.environ['BUILDINGAI_SCHEMA_SYNC'] = '0'
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))
import pytest
import test_wave1
import uvicorn

patch = pytest.MonkeyPatch()
fixture = test_wave1.env.__wrapped__(patch)
client, factory, tokens = next(fixture)
with factory() as db:
    owner = test_wave1.models.User(
        id=8, email='owner@simulation.test', full_name='Rıhtım Yapı Müteahhit',
        hashed_password=test_wave1.TEST_HASH, plan='max', role='muteahhit',
    )
    engineer = test_wave1.models.User(
        id=9, email='engineer@simulation.test', full_name='Saha Mühendisi',
        hashed_password=test_wave1.TEST_HASH, plan='max', role='muhendis',
    )
    db.add_all([owner, engineer])
    db.flush()
    db.add(test_wave1.models.Organization(id=3, name='Rıhtım Yapı', owner_user_id=8))
    db.flush()
    owner.organization_id = 3
    engineer.organization_id = 3
    db.commit()

uvicorn.run(test_wave1.app.app, host='127.0.0.1', port=8001, access_log=False)
