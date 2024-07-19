import unittest
import os
import datetime
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Temitope Emokpae</title>" in html
        
        # Tests relating to home page
        assert "href=\"/\"" in html
        assert "href=\"/work\"" in html
        assert "href=\"/hobbies\"" in html
        assert "href=\"/places\"" in html
        assert "href=\"/timeline\"" in html
        
    def check_post(self, data, post):
        return data['name'] == post['name'] and data['email'] == post['email'] and data['content'] == post['content']     
    
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        
        # print(json)
        
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0 # If other tests fail, their test posts may not be flushed, causing this to fail
        
        # Tests relating to the /api/timeline_post GET and POST apis
        url = "/api/timeline_post"
        first_data = {
            "name": "Johnny Doe",
            "email": "JohnnyDoe@example.com",
            "content": "Hi world, I\'m Johnny!"
        }
        self.client.post(url, data=first_data)
        second_data = {
            "name": "Jenny Doe",
            "email": "Jenny Doe@example.com",
            "content": "Hi world, I\'m Jenny!"
        }
        self.client.post(url, data=second_data)
        
        json = self.client.get(url).get_json()
        assert "timeline_posts" in json
        
        assert self.check_post(first_data, json["timeline_posts"][0]) == True
        assert self.check_post(second_data, json["timeline_posts"][1]) == True
        
        # Tests relating to the timeline page        
        
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        assert "<title>Timeline</title>" in html
        
        assert "href=\"/\"" in html
        assert "href=\"/work\"" in html
        assert "href=\"/hobbies\"" in html
        assert "href=\"/places\"" in html
        assert "href=\"/timeline\"" in html
        assert "form.addEventListener('submit', function(event)" in html
        assert first_data['name'] in html 
        assert second_data['name'] in html
        assert first_data['content'].replace('\'', "&#39;") in html
        assert second_data['content'].replace('\'', "&#39;") in html
        
    def test_malformed_timeline_post(self): 
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html
        
        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html