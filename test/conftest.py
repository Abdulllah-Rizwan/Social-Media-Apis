from fastapi.testclient import TestClient;
from sqlalchemy import create_engine;
from sqlalchemy.orm import sessionmaker;
from sqlalchemy.ext.declarative import declarative_base;
from app.main import app;
from app import schemas,config,models;
from app.OAuth2 import generate_access_token;
from app.database import get_db,Base;
import pytest



SQL_ALCHEMY_DATABASE = f'postgresql://{config.setting.DATABASE_USERNAME}:{config.setting.DATABASE_PASSWORD}@{config.setting.DATABASE_HOSTNAME}:{config.setting.DATABASE_PORT}/Test_SMP_Apis';


# try:
#     conn = psycopg2.connect(host='localhost', database='SMP Apis Database', user='postgres', password='03412959275', cursor_factory=RealDictCursor);
#     cursor = conn.cursor();
#     print("DB connection successful Alhumdulilah")
# except Exception as error:
#     raise Exception("Error connecting:", error);



engine = create_engine(SQL_ALCHEMY_DATABASE);

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine);

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine);
    Base.metadata.create_all(bind=engine); 
    db = TestingSessionLocal();
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session): 
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db;
    yield TestClient(app);
    
    
@pytest.fixture
def test_user(client):
    user_data = { "name":"test", "email":"test@gmail.com", "password":"123" }
    res = client.post("/users/",json=user_data);
    new_user = res.json();
    new_user['password'] = user_data['password'];
    return new_user;

@pytest.fixture
def test_user2(client):
    user_data = { "name":"test2", "email":"test2@gmail.com", "password":"123" }
    res = client.post("/users/",json=user_data);
    new_user = res.json();
    new_user['password'] = user_data['password'];
    return new_user;
    
@pytest.fixture
def token(test_user):
    return generate_access_token({"user_id":test_user['id']});

@pytest.fixture
def authorize_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client;

@pytest.fixture
def test_posts(test_user,session,test_user2):
    posts_data = [
        {
            "title":"First title",
            "content":"First content",
            "owner_id":test_user['id']
        },
        {
            "title":"Second title",
            "content":"Second content",
            "owner_id":test_user['id']
        },
        {
            "title":"Third title",
            "content":"Third content",
            "owner_id":test_user['id']
        },
        {
            "title":"Fourth title",
            "content":"Fourth content",
            "owner_id":test_user2['id']
        },
    ]
    def create_post_model(post):
        return models.Post(**post);
    
    post_map = map(create_post_model, posts_data);
    posts = list(post_map);
    
    session.add_all(posts);
    session.commit();
    all_posts = session.query(models.Post).all();
    return all_posts;


@pytest.fixture
def test_vote(test_user, test_posts, session):
    new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_user['id']);
    session.add(new_vote);
    session.commit();
    return new_vote;
