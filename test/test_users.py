from app import schemas;
import pytest
from jose import jwt;
from app.config import setting;





def test_root(client):
    res = client.get("/");
    assert res.json().get("message") == "Hello World from server";
    assert res.status_code == 200;
    
def test_create_user(client):
    print("Testing create user functionality...");
    res = client.post("/users/",json={"name":"test","email":"test@gmail.com","password":"123"});
    new_user = schemas.User_Out(**res.json());
    assert res.status_code == 201;
    assert new_user.email == "test@gmail.com";
    
def test_login(client,test_user):
    print("Testing login functionality...");
    res = client.post("/login", data={"username":test_user['email'], "password":test_user['password']});
    res_login = schemas.Token(**res.json());
    payload = jwt.decode(res_login.token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM]);
    id = payload.get("user_id");
    assert id == test_user['id'];
    assert res_login.token_type == "Bearer";
    assert res.status_code == 200;


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com','123',403),
    ('test@gmail.com', 'wrongpassword', 403),
    ( None, '123', 422),
    ('test@gmail.com', None, 422)
])
def test_login_fail(client, test_user,email,password,status_code):
    print("Testing login failure functionality...");
    res = client.post("/login",data={"username":email, "password":password});
    assert res.status_code == status_code;