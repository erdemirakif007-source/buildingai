import os
os.environ['DATABASE_URL'] = 'sqlite://'
os.environ['BUILDINGAI_SCHEMA_SYNC'] = '0'
os.environ['GEMINI_API_KEY'] = ''
os.environ['SECRET_KEY'] = 'isolated-regression-key-never-use-in-production'
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import app, auth, models, database

TEST_HASH = auth.get_password_hash("TestPass123")

@pytest.fixture
def env(monkeypatch):
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    models.Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    def get_db():
        with factory() as db:
            try:
                yield db
            except Exception:
                db.rollback()
                raise
    app.app.dependency_overrides[database.get_db] = get_db
    monkeypatch.setattr(database, 'SessionLocal', factory)
    monkeypatch.setattr(app.limiter, 'enabled', False)
    app.global_rate_limiter.cache.clear()
    with factory() as db:
        for i in range(1, 8):
            db.add(models.User(id=i, email=f'user{i}@example.test', full_name=f'Test {i}',
                hashed_password=TEST_HASH, plan='max', role='yonetici'))
        db.flush()
        db.add_all([models.Organization(id=1,name='Org A',owner_user_id=1), models.Organization(id=2,name='Org B',owner_user_id=2)])
        db.flush()
        for i in (1,3,4,5,6): db.get(models.User,i).organization_id=1
        db.get(models.User,2).organization_id=2
        db.add_all([models.Santiye(id=11,user_id=1,organization_id=1,ad='A'),models.Santiye(id=12,user_id=1,organization_id=1,ad='B'),models.Santiye(id=21,user_id=2,organization_id=2,ad='C'),models.Santiye(id=31,user_id=7,ad='Personal')])
        db.flush()
        db.add_all([models.ProjectMember(user_id=3,organization_id=1,santiye_id=11,role='muhendis'),models.ProjectMember(user_id=4,organization_id=1,santiye_id=11,role='viewer'),models.ProjectMember(user_id=5,organization_id=1,santiye_id=11,role='yonetici',status='removed'),models.ProjectMember(user_id=6,organization_id=1,santiye_id=11,role='santi_sefi'),models.ProjectMember(user_id=6,organization_id=1,santiye_id=12,role='viewer')])
        for sid in (11,12,21):
            db.add(models.Bina(id=sid,santiye_id=sid,ad='Block'))
            db.add(models.Kat(id=sid,bina_id=sid,kat_no=0))
            db.add(models.Mahal(id=sid,kat_id=sid,ad='Area'))
            db.add(models.IsKalemi(id=sid,santiye_id=sid,mahal_id=sid,tanim='Work',birim='m2',metraj=1,birim_fiyat=101,toplam_fiyat=101))
            org=1 if sid in (11,12) else 2
            db.add(models.ArchiveRecord(id=sid,organization_id=org,user_id=org,santiye_id=sid,title='Evidence',file_url=f'/static/uploads/manual_evidence/test{sid}.jpg'))
            db.add(models.DailyReport(id=sid,organization_id=org,user_id=org,santiye_id=sid,report_date='2026-09-28'))
            db.add(models.BimModel(id=sid,santiye_id=sid,dosya_adi='model.ifc',orijinal_dosya_adi='model.ifc'))
            db.add(models.Hakedis(id=sid,santiye_id=sid,organization_id=org,hakedis_no=1,donem_baslangic='2026-09-01',donem_bitis='2026-09-30'))
        db.commit()
        tokens={i:auth.create_user_token(db.get(models.User,i)) for i in range(1,8)}
    client=TestClient(app.app,raise_server_exceptions=False)
    yield client, factory, tokens
    client.close()
    app.app.dependency_overrides.clear()
    engine.dispose()

def headers(tokens,user=3): return {'Authorization':f'Bearer {tokens[user]}'}

@pytest.mark.parametrize('user,expected',[(1,[11,12]),(2,[21]),(3,[11]),(4,[11]),(5,[]),(6,[11,12]),(7,[31])])
def test_membership_scope(env,user,expected):
    c,f,t=env
    r=c.get('/santiyeler',headers=headers(t,user))
    assert r.status_code==200,r.text
    assert [x['id'] for x in r.json()['santiyeler']]==expected

@pytest.mark.parametrize('path',['/api/v2/santiye/{}/hiyerarsi','/api/v2/santiye/{}/is-kalemleri','/api/v2/is-kalemleri/{}/ilerleme','/api/v2/is-kalemleri/{}/malzemeler','/api/hakedis/detay/{}','/manual-evidence/{}','/api/bim/model/{}/progress'])
@pytest.mark.parametrize('sid',[12,21])
def test_foreign_reads(env,path,sid):
    c,f,t=env
    r=c.get(path.format(sid),headers=headers(t))
    assert r.status_code in (403,404),r.text

@pytest.mark.parametrize('path,method,body',[('/api/v2/binalar/{}','patch',{'ad':'changed'}),('/api/v2/katlar/{}','patch',{'etiket':'changed'}),('/api/v2/mahaller/{}','delete',{}),('/api/v2/is-kalemleri/{}','patch',{'metraj':99}),('/api/v2/santiye/{}/is-kalemleri','post',{'tanim':'x'}),('/api/v2/is-kalemleri/{}/ilerleme','post',{'yuzde':100,'tarih':'2026-09-28'})])
@pytest.mark.parametrize('sid',[12,21])
def test_foreign_writes(env,path,method,body,sid):
    c,f,t=env
    r=c.request(method,path.format(sid),json=body,headers=headers(t))
    assert r.status_code in (403,404),r.text
    with f() as db: assert db.query(models.IlerlemeKaydi).count()==0

@pytest.mark.parametrize('user,sid,code',[(3,11,200),(4,11,403),(6,12,403),(5,11,404)])
def test_site_roles(env,user,sid,code):
    c,f,t=env
    r=c.patch(f'/api/v2/is-kalemleri/{sid}',json={'tanim':'Updated'},headers=headers(t,user))
    assert r.status_code==code,r.text

@pytest.mark.parametrize('bulk',[False,True])
def test_cross_site_bim_mapping(env,bulk):
    c,f,t=env
    item={'ifc_global_id':'test','is_kalemi_id':12}
    r=c.post('/api/bim/model/11/mapping'+('/bulk' if bulk else ''),json={'mappings':[{'ifc_global_id':'valid','is_kalemi_id':11},item]} if bulk else item,headers=headers(t,1))
    assert r.status_code==422,r.text
    with f() as db: assert db.query(models.BimElementEslestirme).count()==0

def test_valid_progress_rounding_and_no_unapproved_stock(env):
    c,f,t=env
    for pct in (50,100,100):
        r=c.post('/api/ilerleme-kaydet',json={'is_kalemi_id':11,'yuzde':pct},headers=headers(t))
        assert r.status_code==200,r.text
        with f() as db:
            assert db.get(models.Hakedis,11).toplam_tutar==(51 if pct==50 else 101)
            assert db.query(models.StokHareket).count()==0

def test_transaction_rollback(env,monkeypatch):
    c,f,t=env
    original=app.update_hakedis_from_ilerleme
    def fail(db,work):
        original(db,work)
        raise RuntimeError('simulated after financial mutation')
    monkeypatch.setattr(app,'update_hakedis_from_ilerleme',fail)
    r=c.post('/api/ilerleme-kaydet',json={'is_kalemi_id':11,'yuzde':100},headers=headers(t))
    assert r.status_code==500
    with f() as db:
        assert db.query(models.IlerlemeKaydi).count()==0
        assert db.query(models.HakedisKalemi).count()==0
        assert db.get(models.Hakedis,11).toplam_tutar==0
        assert db.get(models.IsKalemi,11).durum=='planli'

@pytest.mark.parametrize('value',['NaN','Infinity',-1,101,'bad'])
def test_invalid_percentage(env,value):
    c,f,t=env
    assert c.post('/api/ilerleme-kaydet',json={'is_kalemi_id':11,'yuzde':value},headers=headers(t)).status_code==422

def test_registration_and_login(env):
    c,f,t=env
    r=c.post('/register',json={'email':'new@example.com','password':'ExamplePass123','full_name':'New User','plan':'max'})
    assert r.status_code==200,r.text
    r=c.post('/login',json={'email':'new@example.com','password':'ExamplePass123'})
    assert r.status_code==200,r.text
    assert r.json()['plan']=='free'
    assert 'HttpOnly' in r.headers['set-cookie']

def test_google_state_required(env):
    c,f,t=env
    assert c.get('/auth/callback/?code=untrusted',follow_redirects=False).status_code==400

def test_password_change_revokes_token(env):
    c,f,t=env
    r=c.post('/hesap/sifre',json={'token':t[3],'current_password':'TestPass123','new_password':'NewPass123'})
    assert r.status_code==200,r.text
    assert c.get('/profil',headers=headers(t)).status_code==401

def test_review_roles_and_history(env):
    c,f,t=env
    url='/api/review-items/evidence/11/decision'
    assert c.patch(url,json={'token':t[3],'status':'approved'}).status_code==403
    r=c.patch(url,json={'token':t[6],'status':'approved','note':'Checked'})
    assert r.status_code==200,r.text
    assert c.patch('/manual-evidence/11',json={'token':t[6],'title':'overwrite'}).status_code==409
    with f() as db: assert db.query(models.DecisionMessage).count()==1

def test_media_requires_authorization_before_file_lookup(env):
    c,f,t=env
    path='/static/uploads/manual_evidence/test12.jpg'
    assert c.get(path).status_code==401
    assert c.get(path,headers=headers(t)).status_code==404

def test_daily_and_archive_lists_isolated(env):
    c,f,t=env
    r=c.get('/daily-reports',headers=headers(t))
    assert r.status_code==200,r.text
    assert [x['santiye_id'] for x in r.json()['raporlar']]==[11]
    r=c.get('/arsiv',headers=headers(t))
    assert r.status_code==200,r.text
    assert all(x['santiye_id']==11 for x in r.json()['manual_evidence'])

def test_material_link_uses_migrated_catalog_and_checks_parent(env):
    c,f,t=env
    with f() as db:
        db.add(models.BirlesikMalzeme(id=101,kategori='test',ad='Test concrete',birim='m3',scrape_tipi='csb_katalog'))
        db.add(models.IsKalemiMalzeme(is_kalemi_id=12,malzeme_katalog_id=101,miktar=3))
        db.commit()
    for method in ('put','delete'):
        r=c.request(method,'/api/v2/is-kalemleri/12/malzeme/101',json={'miktar':9},headers=headers(t))
        assert r.status_code==404,r.text
    assert c.get('/api/v2/is-kalemleri/12/csb-malzemeler',headers=headers(t)).status_code==404
    r=c.post('/api/v2/is-kalemleri/11/malzeme-ekle',json={'malzeme_id':101,'miktar':2},headers=headers(t))
    assert r.status_code==200,r.text
    r=c.get('/api/v2/is-kalemleri/11/malzemeler',headers=headers(t))
    assert r.status_code==200,r.text
    assert r.json()['malzemeler'][0]['malzeme_ad']=='Test concrete'
    with f() as db:
        assert db.query(models.IsKalemiMalzeme).filter_by(is_kalemi_id=12).one().miktar==3


def test_valid_site_without_building_and_decimal_price(env):
    c,f,t=env
    r=c.post('/api/v2/santiye/11/is-kalemleri',json={'tanim':'Port reinforcement','metraj':'3','birim_fiyat_tl':'1.005'},headers=headers(t))
    assert r.status_code==200,r.text
    with f() as db:
        work=db.get(models.IsKalemi,r.json()['id'])
        assert work.mahal_id is None
        assert work.birim_fiyat==101 and work.toplam_fiyat==303


def test_review_messages_inherit_site_scope(env):
    c,f,t=env
    with f() as db:
        db.add(models.ReviewDecision(id=1,user_id=1,organization_id=1,source_type='evidence',source_id=12))
        db.commit()
    assert c.get('/karar/1/mesajlar',headers=headers(t)).status_code==404
    assert c.post('/karar/1/mesaj',json={'mesaj':'not allowed'},headers=headers(t)).status_code==404
    assert c.post('/karar/1/arsivle',headers=headers(t)).status_code==404


def test_uploaded_evidence_batch_is_atomic_and_media_private(env,monkeypatch,tmp_path):
    c,f,t=env
    from PIL import Image
    import io
    content=io.BytesIO(); Image.new('RGB',(2,2),'orange').save(content,format='JPEG')
    monkeypatch.setattr(app,'MANUAL_UPLOAD_ROOT',tmp_path)
    monkeypatch.setattr(app,'MANUAL_THUMB_ROOT',tmp_path)
    r=c.post('/manual-evidence',data={'token':t[3],'santiye_id':'12'},files={'files':('image.jpg',content.getvalue(),'image/jpeg')})
    assert r.status_code==404,r.text
    r=c.post('/manual-evidence',data={'token':t[3],'santiye_id':'11'},files=[('files',('good.jpg',content.getvalue(),'image/jpeg')),('files',('empty.jpg',b'','image/jpeg'))])
    assert r.status_code==400,r.text
    with f() as db: assert db.query(models.ArchiveRecord).count()==3
    assert list(tmp_path.iterdir())==[]


def test_approved_financial_history_remains_and_failed_regression_rolls_back(env):
    c,f,t=env
    with f() as db:
        db.add(models.Hakedis(id=99,organization_id=1,santiye_id=11,hakedis_no=0,donem_baslangic='2026-08-01',donem_bitis='2026-08-31',durum='onaylandi',toplam_tutar=51))
        db.add(models.HakedisKalemi(hakedis_id=99,is_kalemi_id=11,bu_donem_miktar=.5,bu_donem_tutar=51,kumulatif_miktar=.5))
        db.commit()
    r=c.post('/api/ilerleme-kaydet',json={'is_kalemi_id':11,'yuzde':25},headers=headers(t))
    assert r.status_code==409,r.text
    with f() as db:
        assert db.query(models.IlerlemeKaydi).count()==0
        assert db.get(models.Hakedis,99).toplam_tutar==51
    r=c.post('/api/ilerleme-kaydet',json={'is_kalemi_id':11,'yuzde':100},headers=headers(t))
    assert r.status_code==200,r.text
    with f() as db:
        assert db.get(models.Hakedis,11).toplam_tutar==50
        assert db.get(models.Hakedis,99).toplam_tutar==51
    assert c.delete('/api/v2/is-kalemleri/11',headers=headers(t)).status_code==409


def test_explicit_orgwide_membership(env):
    c,f,t=env
    with f() as db:
        db.add(models.ProjectMember(user_id=3,organization_id=1,santiye_id=None,role='viewer'))
        db.commit()
    assert [x['id'] for x in c.get('/santiyeler',headers=headers(t)).json()['santiyeler']]==[11,12]
    assert c.patch('/api/v2/is-kalemleri/12',json={'tanim':'x'},headers=headers(t)).status_code==403


def test_removal_effective_with_existing_token(env):
    c,f,t=env
    with f() as db:
        db.query(models.ProjectMember).filter_by(user_id=3).update({'status':'removed'})
        db.commit()
    assert c.get('/api/v2/santiye/11/hiyerarsi',headers=headers(t)).status_code==404


def test_owner_only_member_management(env):
    c,f,t=env
    with f() as db:
        member=db.query(models.ProjectMember).filter_by(user_id=4).one().id
    assert c.post('/ekip/cikar',json={'member_id':member},headers=headers(t)).status_code==403
    assert c.post('/ekip/cikar',json={'member_id':member},headers=headers(t,1)).status_code==200


def test_google_verified_subject_does_not_silently_link_local_account(env,monkeypatch):
    c,f,t=env
    class Remote:
        async def __aenter__(self): return self
        async def __aexit__(self,*args): pass
        def __init__(self,**kwargs): pass
        async def post(self,*args,**kwargs):
            return app.httpx.Response(200,json={'access_token':'isolated-test-only'})
        async def get(self,*args,**kwargs):
            return app.httpx.Response(200,json={'sub':'new-subject','email':'user3@example.test','email_verified':True})
    monkeypatch.setattr(app.httpx,'AsyncClient',Remote)
    c.cookies.set('oauth_state','test-state',path='/auth')
    r=c.get('/auth/callback/?code=test&state=test-state',follow_redirects=False)
    assert 'account_link_required' in r.headers['location']
    with f() as db: assert db.get(models.User,3).google_sub is None


def test_password_reset_code_is_bound_to_email(env):
    c,f,t=env
    import datetime
    with f() as db:
        db.add(models.ResetToken(email='user3@example.test',token='123456',expires_at=datetime.datetime.utcnow()+datetime.timedelta(minutes=5)))
        db.commit()
    r=c.post('/sifre-guncelle',json={'token':'123456','email':'user4@example.test','yeni_sifre':'newPassword123'})
    assert r.status_code==400,r.text
    with f() as db: assert not db.query(models.ResetToken).one().used

def test_payment_workflow_pdf_and_frozen_approval(env):
    c,f,t=env
    assert c.delete('/api/hakedis/sil/11',headers=headers(t)).status_code==200
    r=c.post('/api/hakedis/olustur',headers=headers(t),json={'santiye_id':11,'donem_baslangic':'2026-09-01','donem_bitis':'2026-09-30'})
    assert r.status_code==200,r.text
    hid=r.json()['hakedis_id']
    with f() as db: lid=db.query(models.HakedisKalemi).filter_by(hakedis_id=hid).one().id
    r=c.patch('/api/hakedis/kalem-guncelle',headers=headers(t),json={'hakedis_kalem_id':lid,'bu_donem_miktar':2})
    assert r.status_code==422,r.text
    r=c.patch('/api/hakedis/kalem-guncelle',headers=headers(t),json={'hakedis_kalem_id':lid,'bu_donem_miktar':.5})
    assert r.status_code==200,r.text
    assert r.json()['kalem']['bu_donem_tutar']==.51
    # Later progress cannot overwrite a reviewer-entered quantity.
    assert c.post('/api/ilerleme-kaydet',headers=headers(t),json={'is_kalemi_id':11,'yuzde':100}).status_code==200
    with f() as db: assert db.get(models.HakedisKalemi,lid).bu_donem_miktar==.5
    url=f'/api/hakedis/durum-guncelle/{hid}'
    assert c.patch(url,headers=headers(t),json={'durum':'onay_bekliyor'}).status_code==200
    assert c.patch(url,headers=headers(t),json={'durum':'onaylandi'}).status_code==403
    assert c.patch(url,headers=headers(t,6),json={'durum':'onaylandi'}).status_code==200
    assert c.patch(url,headers=headers(t,6),json={'durum':'taslak'}).status_code==409
    assert c.delete(f'/api/hakedis/sil/{hid}',headers=headers(t,6)).status_code==409
    assert c.patch('/api/hakedis/kalem-guncelle',headers=headers(t,6),json={'hakedis_kalem_id':lid,'bu_donem_miktar':1}).status_code==409
    pdf=c.get(f'/api/hakedis/pdf/{hid}',headers=headers(t))
    assert pdf.status_code==200,pdf.text[:120] if pdf.status_code!=200 else ''
    assert pdf.content.startswith(b'%PDF-')
    from pypdf import PdfReader
    import io
    content=''.join(p.extract_text() for p in PdfReader(io.BytesIO(pdf.content)).pages)
    assert '0,51 TL' in content and 'KDV' in content
    assert c.get(f'/api/hakedis/pdf/{hid}',headers=headers(t,2)).status_code==404
    with f() as db:
        assert db.get(models.Hakedis,hid).onaylayan_id==6
        assert 'onaylandi' in db.get(models.Hakedis,hid).notlar
        assert db.get(models.Hakedis,11).durum=='iptal'

@pytest.mark.parametrize('path,method,body',[
    ('/api/hakedis/olustur','post',{'santiye_id':12,'donem_baslangic':'2026-09-01','donem_bitis':'2026-09-30'}),
    ('/api/hakedis/sil/12','delete',{}),
    ('/api/hakedis/durum-guncelle/12','patch',{'durum':'onay_bekliyor'}),
    ('/api/hakedis/pdf/12','get',{}),
])
def test_payment_routes_reject_other_site(env,path,method,body):
    c,f,t=env
    r=c.request(method,path,json=body,headers=headers(t))
    assert r.status_code==404,r.text


def test_progress_cannot_regress_approved_quantity_without_draft(env):
    c,f,t=env
    with f() as db:
        payment=db.get(models.Hakedis,11)
        payment.durum='onaylandi'
        db.add(models.HakedisKalemi(hakedis_id=11,is_kalemi_id=11,bu_donem_miktar=.5,bu_donem_tutar=51))
        db.commit()
    r=c.post('/api/ilerleme-kaydet',json={'is_kalemi_id':11,'yuzde':25},headers=headers(t))
    assert r.status_code==409,r.text
    with f() as db: assert db.query(models.IlerlemeKaydi).count()==0
