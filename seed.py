'''Seed file to make sample data for users db.'''

from models import User, db, Post, Tag, PostTag
from app import app

# reset all tables
db.drop_all()
db.create_all()

# empty out all tables
User.query.delete()

# add users
user1 = User(first_name = 'John', last_name = 'Carter')
user2 = User(first_name = 'Lang', last_name = 'Scott', image_url = 'https://lh3.googleusercontent.com/proxy/2BUk0-jB6p5YU22s0arYirkr4LxPCnCf6p86lNnhYTl2ierazzRht5LKvGXI3CZKZ8Y85_4o6VCUOVelauzk173m1VXCGzivMCDKOS07c2QxANkP4TX_ktvu4FpAy0Gz2dw')
user3 = User(first_name = 'Michael', last_name = 'Jackson', image_url = 'https://static.wikia.nocookie.net/disney/images/2/2c/Michael_Jackson.jpg/revision/latest?cb=20210115030919')
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

