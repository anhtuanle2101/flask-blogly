from unittest import TestCase
from app import app
from models import db, User, Post, Tag, PostTag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UsersViewTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        user = User(first_name='David', last_name='Johnson')
        db.session.add(user)
        db.session.commit()

        self.user_id=user.id
    
    def tearDown(self):
        db.session.rollback()

    def test_redirects(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 302)

    def test_users(self):
        with app.test_client() as client:
            res = client.get('/', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('David Johnson', html)
    
    def test_add(self):
        with app.test_client() as client:
            data = {'first_name':'Thu', 'last_name':'Tran'}
            res = client.post('/users/new', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Thu Tran', html)

    def test_delete(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn('David Johnson', html)

class ManyToManyTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all() 
        User.query.delete()
        Post.query.delete()
        Tag.query.delete()
        PostTag.query.delete()

        # add users
        user1 = User(first_name = 'John', last_name = 'Carter')
        user2 = User(first_name = 'Lang', last_name = 'Scott')
        user3 = User(first_name = 'Michael', last_name = 'Jackson')
        user4 = User(first_name = 'Annie', last_name ='Johnson')

        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()

        # add posts
        post1 = Post(title='New Horizon', content='asdaszxczxdfasda', user_id=1)
        post2 = Post(title='Avengers', content='Marvel is the Best!', user_id=1)
        post3 = Post(title='Nintendo Switch', content='Best game console ever!', user_id=3)
        post4 = Post(title='Ipad vs Iphone', content='They are obviously different', user_id=2)
        post5 = Post(title='Google vs Facebook', content='Google > Facebook', user_id=3)
        post6 = Post(title='How Intenet Works', content='Google.com and search for how Internet works', user_id=4)

        db.session.add_all([post1, post2, post3, post4, post5, post6])
        db.session.commit()

        #tags
        tag1 = Tag(name='savetheworld!!')
        tag2 = Tag(name='rolling')
        tag3 = Tag(name='BLM')
        tag4 = Tag(name='Gaming4Life!')

        db.session.add_all([tag1,tag2,tag3,tag4])
        db.session.commit()

        #posts_tags
        post_tag1 = PostTag(post_id=1, tag_id=1)
        post_tag2 = PostTag(post_id=1, tag_id=2)
        post_tag3 = PostTag(post_id=2, tag_id=4)
        post_tag4 = PostTag(post_id=2, tag_id=2)
        post_tag5 = PostTag(post_id=2, tag_id=3)
        post_tag6 = PostTag(post_id=3, tag_id=1)
        post_tag7 = PostTag(post_id=4, tag_id=4)
        post_tag8 = PostTag(post_id=5, tag_id=3)
        post_tag9 = PostTag(post_id=6, tag_id=2)

        db.session.add_all([post_tag1,post_tag2,post_tag3,post_tag4,post_tag5, post_tag6,post_tag7,post_tag8,post_tag9])
        db.session.commit()
    
    def tearDown(self):
        db.session.rollback()
    
    def test_edit_user(self):
        with app.test_client() as client:
            data = {'first_name':'ArmStrong', 'last_name':'Tran'}
            res = client.post('/users/1/edit', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('ArmStrong Tran', html)
            self.assertNotIn('John Carter', html)
    
    def test_delete_cascade_user(self):
        with app.test_client() as client:
            res = client.post('/users/1/delete', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn('John Carter', html)
            self.assertEqual(len(Post.query.filter(Post.user_id == 1).all()), 0)

    def test_create_post(self):
        with app.test_client() as client:
            data = {'title':'Pikachu', 'content':'Pikachu is Pokemon'}
            res = client.post('/users/1/posts/new', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('Pikachu', html)
            self.assertIn('Pikachu is Pokemon', html)
    
    def test_delete_post(self):
        with app.test_client() as client:
            res = client.post('/posts/1/delete', follow_redirects=True)
            res = client.get('/users/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn('New Horizon', html)


    

