# test_db.py

import unittest
from peewee import *

from app import TimelinePost, get_time_line_post 

MODELS = [TimelinePost]

# use an in-memory SQLite for tests
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        
        test_db.connect()
        test_db.create_tables(MODELS)
        
    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection ... but a good practice all the same.
        test_db.drop_tables(MODELS)
        
        # Close connection to db.
        test_db.close()
        
    def check_entry(self, entry, post):
        # Given a test entry and an actual post to the same database
        # assuming they are meant to be the same entry
        # assert if their content equals
        return entry['id'] == post.id and entry['name'] == post.name and entry['email'] == post.email and entry['content'] == post.content and entry['created_at'] == post.created_at
        
    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2
        
        # TODO: Get timeline posts and assert that they are correct
        timeline_posts = get_time_line_post()['timeline_posts']
        first_entry, second_entry = timeline_posts[0], timeline_posts[1]
 
        # Assert first post is correct
        assert self.check_entry(first_entry, first_post) == True
        assert self.check_entry(second_entry, second_post) == True