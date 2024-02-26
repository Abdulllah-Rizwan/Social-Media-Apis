from app import schemas;
import pytest;


def test_get_all_posts(client,test_posts):
    print("Testing get all post functionality...")
    res = client.get("/posts");
    post = schemas.Post_Out(**res.json()[0])
    assert post.Post.id == test_posts[0].id
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_create_post(client, test_posts):
    print("Testing unauthorized user create post functionality...");
    res = client.post("/posts", json={"title": "new title", "content": "new content"});
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated";
    
def test_unauthorized_user_get_one_post(client, test_posts):
    print("Testing unauthorized user getting one post functionality...");
    res = client.get(f"/posts/{test_posts[0].id}");
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated";

def test_get_one_post_not_exist(authorize_client, test_posts):
    print("Testing getting one post that does not exist functionality...");
    res = authorize_client.get(f"/posts/100");
    assert res.status_code == 404
    assert res.json()["detail"] == "Post does not exist";
    
def test_get_one_post(authorize_client, test_posts):
    print("Testing getting one post functionality...");
    res = authorize_client.get(f"/posts/{test_posts[0].id}");
    post = schemas.Post_Out(**res.json());
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title  
    assert res.status_code == 200
    
@pytest.mark.parametrize("title, content, published", [
    ("hobby","Loving coding",True),
    ("study", "Studying python", False),
    ("work", "Working on python", True),
])
def test_create_post(authorize_client, test_posts, title, content, published):
    print("Testing create post functionality...");
    res = authorize_client.post("/posts", json={"title": title, "content": content, "published": published});
    created_post = schemas.Post(**res.json());
    assert res.status_code == 201;
    assert created_post.title == title;
    assert created_post.content == content;
    assert created_post.published == published;
    assert created_post.owner_id == test_posts[0].owner_id;
    
def test_create_post_default_published_true(authorize_client, test_posts):
    print("Testing create post default published equals true functionality...");
    res = authorize_client.post("/posts", json={"title": "random", "content": "random"});
    created_post = schemas.Post(**res.json());
    assert res.status_code == 201;
    assert created_post.title == "random";
    assert created_post.content == "random";
    assert created_post.published == True;
    assert created_post.owner_id == test_posts[0].owner_id;
    
def test_unauthorized_user_delete_post(client, test_posts):
    print("Testing unauthorized user delete post functionality...");
    res = client.delete(f"/posts/{test_posts[0].id}");
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated";
    
def test_delete_post_success(authorize_client, test_posts):
    print("Testing delete post functionality...");
    res = authorize_client.delete(f"/posts/{test_posts[0].id}");
    assert res.status_code == 204;
    
def test_delete_post_not_exist(authorize_client, test_posts):
    print("Testing delete post that does not exist functionality...");
    res = authorize_client.delete(f"/posts/100");
    assert res.status_code == 404
    assert res.json()["detail"] == "Post does not exist";

def test_delete_other_user_post(authorize_client, test_posts):
    print("Testing delete other user post functionality...");
    res = authorize_client.delete(f"/posts/{test_posts[3].id}");
    assert res.status_code == 403
    assert res.json()["detail"] == "Not authorized to perform requested action";
    
def test_update_post(authorize_client, test_posts):
    print("Testing update post functionality...");
    data = {"title": "updated title", "content": "updated content", "id": test_posts[0].id};
    res = authorize_client.put(f"/posts/{test_posts[0].id}", json=data);
    updated_post = schemas.Post(**res.json());
    assert res.status_code == 202;
    assert updated_post.title == data["title"];
    assert updated_post.content == data["content"];

def test_update_other_user_post(authorize_client, test_posts):
    print("Testing update other user post functionality...");
    data = {"title": "updated title", "content": "updated content", "id": test_posts[3].id};
    res = authorize_client.put(f"/posts/{test_posts[3].id}", json=data);
    assert res.status_code == 403
    assert res.json()["detail"] == "Not authorized to perform requested action";
    
def test_unauthorized_user_update_post(client, test_posts):
    print("Testing unauthorized user update post functionality...");
    res = client.put(f"/posts/{test_posts[0].id}");
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated";
    
def test_update_post_not_exist(authorize_client, test_posts):
    print("Testing update post that does not exist functionality...");
    data = {"title": "updated title", "content": "updated content", "id": 100};
    res = authorize_client.put(f"/posts/100", json=data);
    assert res.status_code == 404
    assert res.json()["detail"] == "Post does not exist";