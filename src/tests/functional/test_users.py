import json
# from src import db
from src.api.models import User

#--------------- get -----------------------------------------------

def test_all_users(test_app, test_database, add_user):
    print("Debug: in test_all_users()")
    test_database.session.query(User).delete()  # new
    add_user('hao', 'hao@gmail.com')
    add_user('jeffrey', 'jeffrey@gmail.com')
    client = test_app.test_client()
    resp = client.get('/users')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert 'hao' in data[0]['username']
    assert 'hao@gmail.com' in data[0]['email']
    assert 'jeffrey' in data[1]['username']
    assert 'jeffrey@gmail.com' in data[1]['email']



def test_single_user(test_app, test_database, add_user):
    print("Debug: in test_single_user()")
    user = add_user('jeffrey', 'jeffrey@yahoo.com')
    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'jeffrey' in data['username']
    assert 'jeffrey@yahoo.com' in data['email']



# def test_single_user(test_app, test_database):
#     user = User(username='jeffrey', email='jeffrey@yahoo.com')
#     db.session.add(user)
#     db.session.commit()
#
#     client = test_app.test_client()
#     resp = client.get(f'/users/{user.id}')
#     data = json.loads(resp.data.decode())
#
#     # print("debug 1: {}".format(resp.status_code))
#     # print("debug 2: {}".format(data['username']))
#     # print("debug 3: {}".format(data['email']))
#
#     assert resp.status_code == 200
#     assert 'jeffrey' in data['username']
#     assert 'jeffrey@yahoo.com' in data['email']


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/users/999')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'User 999 does not exist' in data['message']


#--------------- post ----------------------------------------------

def test_add_user(test_app, test_database):
    print("In test_add_user()")
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'hao',
            'email': 'hao@yahoo.com'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'hao@yahoo.com was added!' in data['message']


# 都没有
def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


# 没有username
def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({"email": "john@yahoo.com"}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


# 测试 已存在
def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    # 先创建
    client.post(
        '/users',
        data=json.dumps({
            'username': 'hao',
            'email': 'hao@yahoo.com'
        }),
        content_type='application/json',
    )
    # 再创建，already exists.
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'hao',
            'email': 'hao@yahoo.com'
        }),
        content_type='application/json',
    )

    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry. That email already exists.' in data['message']


