
def test_vote_on_post(authorize_client, test_posts):
    print("Testing votes on Post");
    res = authorize_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201;

def test_vote_twice_post(authorize_client, test_posts,test_vote):
    print("Testing twice votes on Post by same user");
    res = authorize_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 409;
    
def test_delete_vote(authorize_client, test_posts, test_vote):
    print("Testing delete votes on Post");
    res = authorize_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 201;
    
def test_vote_on_post_non_exist(authorize_client):
    print("Testing votes on Post with non exist post id");
    res = authorize_client.post("/vote/", json={"post_id": 100, "dir": 1})
    assert res.status_code == 404;
    
def test_vote_on_post_unauthorized(client, test_posts):
    print("Testing votes on Post with unauthorized user");
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401;