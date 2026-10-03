from decimal import Decimal

from test_wave1 import env, headers
import models
from migrations.wave2_chain import upgrade
from sqlalchemy import create_engine, inspect, text


def test_rihtim_measurement_payment_chain(env):
    client, factory, tokens = env
    with factory() as db:
        db.delete(db.get(models.Hakedis, 11))
        work = db.get(models.IsKalemi, 11)
        work.poz_no, work.tanim, work.birim = 'RHTM-01', 'Rıhtım güçlendirme', 'm³'
        work.metraj, work.birim_fiyat, work.toplam_fiyat = 120, 1250000, 150000000
        db.commit()
    h3, h6, h4 = headers(tokens, 3), headers(tokens, 6), headers(tokens, 4)
    area = client.post('/api/v2/santiye/11/areas', headers=h3, json={'name':'Rıhtım A', 'kind':'bolge'})
    assert area.status_code == 200, area.text
    area_id = area.json()['id']
    contract = client.post('/api/v2/santiye/11/contracts', headers=h3,
        json={'name':'Liman işi', 'direction':'employer', 'counterparty':'İşveren A', 'currency':'TRY'})
    assert contract.status_code == 200, contract.text
    contract_id = contract.json()['id']
    line = client.post(f'/api/v2/contracts/{contract_id}/lines', headers=h3,
        json={'work_item_id':11, 'code':'RHTM-01', 'quantity':'120', 'unit_price':'12500'})
    assert line.status_code == 200, line.text
    line_id = line.json()['id']
    payload = {'area_id':area_id, 'contract_line_id':line_id, 'work_date':'2026-09-28',
        'reported_quantity':'30', 'basis':'Ölçüm krokisi R-1', 'request_key':'rihtim-1'}
    measure = client.post('/api/v2/santiye/11/measurements', headers=h3, json=payload)
    assert measure.status_code == 200, measure.text
    mid = measure.json()['id']
    assert client.post('/api/v2/santiye/11/measurements', headers=h3, json=payload).json()['id'] == mid
    assert client.post(f'/api/v2/measurements/{mid}/submit', headers=h3).status_code == 200
    assert client.post(f'/api/v2/measurements/{mid}/review', headers=h3,
        json={'accepted_quantity':'28','reason':'2 m³ ölçü dışında'}).status_code == 403
    review = client.post(f'/api/v2/measurements/{mid}/review', headers=h6,
        json={'accepted_quantity':'28','reason':'2 m³ ölçü dışında'})
    assert review.status_code == 200, review.text
    assert review.json()['remaining_quantity'] == '28.000'
    payment = client.post(f'/api/v2/contracts/{contract_id}/payments', headers=h3,
        json={'start_date':'2026-09-01','end_date':'2026-09-30'})
    assert payment.status_code == 200, payment.text
    pid = payment.json()['id']
    assert client.post(f'/api/v2/payments/{pid}/allocations', headers=h4,
        json={'measurement_id':mid,'quantity':'28'}).status_code == 403
    first_part = client.post(f'/api/v2/payments/{pid}/allocations', headers=h3,
        json={'measurement_id':mid,'quantity':'10'})
    assert first_part.status_code == 200, first_part.text
    assert Decimal(client.get('/api/v2/santiye/11/measurements',headers=h3).json()['measurements'][0]['remaining_quantity']) == 18
    allocation = client.post(f'/api/v2/payments/{pid}/allocations', headers=h3,
        json={'measurement_id':mid,'quantity':'18'})
    assert allocation.status_code == 200, allocation.text
    assert Decimal(allocation.json()['period_amount']) == Decimal('350000')
    assert client.post(f'/api/v2/payments/{pid}/allocations', headers=h3,
        json={'measurement_id':mid,'quantity':'0.001'}).status_code == 409
    detail = client.get(f'/api/v2/payments/{pid}/allocations', headers=h3)
    assert detail.status_code == 200
    assert detail.json()['allocations'][0]['measurement']['basis'] == 'Ölçüm krokisi R-1'
    assert client.patch('/api/hakedis/kalem-guncelle',headers=h3,
        json={'hakedis_kalem_id':client.get(f'/api/hakedis/detay/{pid}',headers=h3).json()['kalemler'][0]['id'],
              'bu_donem_miktar':29}).status_code == 409
    url=f'/api/hakedis/durum-guncelle/{pid}'
    assert client.patch(url,headers=h3,json={'durum':'onay_bekliyor'}).status_code == 200
    assert client.patch(url,headers=h3,json={'durum':'onaylandi'}).status_code == 403
    assert client.patch(url,headers=h4,json={'durum':'onaylandi'}).status_code == 403
    assert client.patch(url,headers=h6,json={'durum':'onaylandi'}).status_code == 200
    assert client.patch(url,headers=h6,json={'durum':'onaylandi'}).status_code == 200
    with factory() as db:
        assert db.get(models.Hakedis,pid).toplam_tutar == 35000000
        assert db.get(models.FieldMeasurement,mid).allocated_quantity == 28
        assert db.query(models.MeasurementDecision).filter_by(measurement_id=mid).count() == 2
        assert db.query(models.PaymentDecision).filter_by(payment_id=pid).count() == 2
        db.get(models.IsKalemi,11).birim_fiyat = 9900000
        db.commit()
        assert db.get(models.Hakedis,pid).toplam_tutar == 35000000


def test_cross_project_measurement_and_project_city(env):
    client, factory, tokens = env
    response=client.post('/santiye-ekle',headers=headers(tokens,1),json={'ad':'İzmir Rıhtım','sehir':'İzmir'})
    assert response.status_code == 200, response.text
    sid=response.json()['id']
    rows=client.get('/santiyeler',headers=headers(tokens,1)).json()['santiyeler']
    assert next(x for x in rows if x['id']==sid)['sehir']=='İzmir'
    assert next(x for x in rows if x['id']==sid)['ilerleme'] is None
    assert next(x for x in rows if x['id']==sid)['durum'] is None
    assert next(x for x in rows if x['id']==sid)['isg_durumu'] is None
    assert client.post(f'/santiye-guncelle/{sid}',headers=headers(tokens,1),json={'ad':'İzmir Rıhtım 2'}).status_code==200
    rows=client.get('/santiyeler',headers=headers(tokens,1)).json()['santiyeler']
    assert next(x for x in rows if x['id']==sid)['sehir']=='İzmir'
    assert client.get('/api/v2/santiye/12/measurements',headers=headers(tokens,3)).status_code==404


def test_additive_migration_is_repeatable(tmp_path):
    engine=create_engine(f'sqlite:///{tmp_path / "copy.db"}')
    models.User.__table__.create(engine, checkfirst=True)
    models.Santiye.__table__.create(engine, checkfirst=True)
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO users (id,email,is_admin,auth_provider,email_verified) VALUES (1,'legacy@example.com',0,'local',0)"))
        connection.execute(text("INSERT INTO santiyeler (id,user_id,ad,sehir) VALUES (1,1,'Eski proje','İzmir')"))
    before=set(inspect(engine).get_table_names())
    upgrade(engine)
    after=set(inspect(engine).get_table_names())
    assert before.issubset(after)
    assert {'work_areas','contracts','field_measurements','inventory_movements'}.issubset(after)
    upgrade(engine)
    assert set(inspect(engine).get_table_names()) == after
    with engine.connect() as connection:
        assert connection.execute(text('SELECT ad,sehir FROM santiyeler WHERE id=1')).one() == ('Eski proje','İzmir')
    engine.dispose()


def test_project_level_measurement_allows_incomplete_draft(env):
    client, factory, tokens = env
    h=headers(tokens,3)
    contract=client.post('/api/v2/santiye/11/contracts',headers=h,json={
        'name':'Küçük iş','direction':'employer','counterparty':'İşveren','currency':'TRY'})
    assert contract.status_code==200,contract.text
    line=client.post(f"/api/v2/contracts/{contract.json()['id']}/lines",headers=h,json={
        'work_item_id':11,'code':'D-01','quantity':'10','unit_price':'100'})
    assert line.status_code==200,line.text
    draft=client.post('/api/v2/santiye/11/measurements',headers=h,json={'request_key':'direct-draft'})
    assert draft.status_code==200,draft.text
    mid=draft.json()['id']
    assert client.post(f'/api/v2/measurements/{mid}/submit',headers=h).status_code==422
    edited=client.patch(f'/api/v2/measurements/{mid}',headers=h,json={
        'contract_line_id':line.json()['id'],'work_date':'2026-09-29',
        'reported_quantity':'2','basis':'Saha ölçüm tutanağı'})
    assert edited.status_code==200,edited.text
    submitted=client.post(f'/api/v2/measurements/{mid}/submit',headers=h)
    assert submitted.status_code==200,submitted.text
    assert submitted.json()['area_id'] is None


def test_general_and_mahal_work_items_remain_visible(env):
    client, factory, tokens=env
    with factory() as db:
        db.add(models.IsKalemi(santiye_id=11, mahal_id=None, poz_no='GEN-01',
            tanim='Rıhtım genel imalatı', birim='m³', metraj=5,
            birim_fiyat=10000, toplam_fiyat=50000))
        db.commit()
    response=client.get('/api/v2/santiye/11/is-kalemleri',headers=headers(tokens,3))
    assert response.status_code==200,response.text
    rows=response.json()['kalemler']
    assert any(x['poz_no']=='GEN-01' and x['mahal_id'] is None for x in rows)
    assert any(x['mahal_id']==11 for x in rows)
    assert client.get('/api/metraj/ozet/11',headers=headers(tokens,3)).json()['toplam_kalem']==2


def test_google_button_target_starts_stateful_oauth(env, monkeypatch):
    import app as main_app
    client, _, _=env
    monkeypatch.setattr(main_app,'GOOGLE_CLIENT_ID','test-client-id')
    response=client.get('/auth/google/login',follow_redirects=False)
    assert response.status_code in (302,307)
    assert response.headers['location'].startswith(main_app.GOOGLE_AUTH_URL)
    assert 'state=' in response.headers['location']
    assert 'oauth_state=' in response.headers['set-cookie']
    assert client.get('/auth/google/callback?code=fake',follow_redirects=False).status_code==400


def test_catalog_and_stock_ledger(env):
    client, factory, tokens = env
    h=headers(tokens,3)
    catalog=client.get('/api/v2/materials',headers=h)
    assert catalog.status_code==200
    beton=next(x for x in catalog.json()['materials'] if x['key']=='beton')
    assert beton['stock_quantity'] is None
    custom=client.post('/api/v2/materials',headers=h,json={'name':'Özel grout','unit':'kg'})
    assert custom.status_code==200, custom.text
    assert client.post('/api/v2/materials',headers=h,json={'name':'Özel grout','unit':'kg'}).status_code==409
    key=custom.json()['key']
    base={'material_key':key,'unit':'kg','variant':'20 kg torba','quantity':'100',
          'kind':'receipt','request_key':'test-stock-receipt'}
    receipt=client.post('/api/v2/santiye/11/inventory/movements',headers=h,json=base)
    assert receipt.status_code==200,receipt.text
    assert Decimal(receipt.json()['balance'])==100
    replay=client.post('/api/v2/santiye/11/inventory/movements',headers=h,json=base)
    assert replay.status_code==200 and replay.json()['replayed']
    issue=client.post('/api/v2/santiye/11/inventory/movements',headers=h,json={**base,
        'kind':'issue','quantity':'30','request_key':'test-stock-issue','work_item_id':11})
    assert issue.status_code==200,issue.text
    assert Decimal(issue.json()['balance'])==70
    assert client.post('/api/v2/santiye/11/inventory/movements',headers=h,json={**base,
        'kind':'issue','quantity':'71','request_key':'test-stock-overspend'}).status_code==409
    stock=client.get('/api/v2/santiye/11/inventory',headers=h).json()
    assert Decimal(stock['balances'][0]['quantity'])==70
    assert len(stock['movements'])==2
    assert client.get('/api/v2/santiye/12/inventory',headers=h).status_code==404


def test_manual_daily_report_without_ai_and_project_isolation(env):
    client, factory, tokens=env
    body={'santiye_id':11,'report_date':'2026-09-29','summary':'Rıhtım A bölümünde ölçüm yapıldı.'}
    first=client.post('/daily-reports/manual',headers=headers(tokens,3),json=body)
    assert first.status_code==200,first.text
    second=client.post('/daily-reports/manual',headers=headers(tokens,3),json={**body,'summary':'Ölçüm ve kroki hazır.'})
    assert second.status_code==200 and second.json()['id']==first.json()['id']
    listed=client.get('/daily-reports?santiye_id=11',headers=headers(tokens,3))
    assert listed.status_code==200
    assert listed.json()['raporlar'][0]['summary']=='Ölçüm ve kroki hazır.'
    assert client.post('/daily-reports/manual',headers=headers(tokens,3),json={**body,'santiye_id':12}).status_code==404


def test_hakedis_detay_yeni_alanlar_mevcut(env):
    """hakedis_detay yanıtında yeni alanlar her zaman mevcut, kaynak ilerleme."""
    client, factory, tokens = env
    r = client.get('/api/hakedis/detay/11', headers=headers(tokens, 3))
    assert r.status_code == 200, r.text
    h = r.json()['hakedis']
    for key in ('hazirlayan_id', 'hazirlayan_ad', 'onaylayan_id', 'onaylayan_ad'):
        assert key in h, f"Eksik alan: {key}"
    # Seed hakediş hazirlayan_id=None — ad da None olmalı
    assert h['hazirlayan_id'] is None
    assert h['hazirlayan_ad'] is None
    # Kalemler için kaynak alanı
    for k in r.json()['kalemler']:
        assert k.get('kaynak') in ('manuel', 'ilerleme'), f"Geçersiz kaynak: {k.get('kaynak')}"


def test_hazirlayan_ad_cozumleniyor(env):
    """API üzerinden oluşturulan hakedişte hazirlayan_id ve hazirlayan_ad doğru dolar."""
    client, factory, tokens = env
    # env function-scoped: her test kendi izole DB'sine sahip
    with factory() as db:
        db.delete(db.get(models.Hakedis, 11))
        db.commit()
    r = client.post('/api/hakedis/olustur', headers=headers(tokens, 3),
                    json={'santiye_id': 11, 'donem_baslangic': '2026-10-01', 'donem_bitis': '2026-10-31'})
    assert r.status_code == 200, r.text
    pid = r.json()['hakedis_id']
    detail = client.get(f'/api/hakedis/detay/{pid}', headers=headers(tokens, 3))
    assert detail.status_code == 200, detail.text
    h = detail.json()['hakedis']
    assert h['hazirlayan_id'] == 3
    assert h['hazirlayan_ad'] == 'Test 3'
    assert h['onaylayan_id'] is None
    assert h['onaylayan_ad'] is None
    # Kalem kaynak: ilerleme tabanlı oluşturulmuş
    for k in detail.json()['kalemler']:
        assert k['kaynak'] == 'ilerleme'


def test_decisions_actor_ad(env):
    """decisions endpoint'inde actor_ad batch yüklenir ve doğru çözümlenir."""
    client, factory, tokens = env
    with factory() as db:
        db.delete(db.get(models.Hakedis, 11))
        db.commit()
    pid = client.post('/api/hakedis/olustur', headers=headers(tokens, 3),
                      json={'santiye_id': 11, 'donem_baslangic': '2026-10-01', 'donem_bitis': '2026-10-31'}).json()['hakedis_id']
    # user 3 taslak → onay_bekliyor
    tr = client.patch(f'/api/hakedis/durum-guncelle/{pid}', headers=headers(tokens, 3),
                      json={'durum': 'onay_bekliyor'})
    assert tr.status_code == 200, tr.text
    dec = client.get(f'/api/hakedis/decisions/{pid}', headers=headers(tokens, 3))
    assert dec.status_code == 200, dec.text
    d = dec.json()['decisions']
    assert len(d) == 1
    assert d[0]['actor_id'] == 3
    assert d[0]['actor_ad'] == 'Test 3'
    assert d[0]['previous_status'] == 'taslak'
    assert d[0]['new_status'] == 'onay_bekliyor'
    assert 'created_at' in d[0]
    # Eski alanlar değişmemiş
    assert 'reason' in d[0]
