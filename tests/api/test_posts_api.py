import pytest
from playwright.sync_api import APIRequestContext


@pytest.mark.api
def test_get_all_posts_returns_100_items(api_context: APIRequestContext):
    response = api_context.get("/posts")

    assert response.status == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) == 100


@pytest.mark.api
@pytest.mark.smoke
def test_get_single_post_returns_correct_structure(api_context: APIRequestContext):
    response = api_context.get("/posts/1")

    assert response.status == 200
    post = response.json()
    assert post["id"] == 1
    assert "userId" in post
    assert "title" in post
    assert "body" in post


@pytest.mark.api
def test_create_post_returns_201_with_id(api_context: APIRequestContext):
    payload = {"title": "Automation Test Post", "body": "Created by Playwright", "userId": 1}

    response = api_context.post("/posts", data=payload)

    assert response.status == 201
    created = response.json()
    assert "id" in created
    assert created["title"] == payload["title"]


@pytest.mark.api
def test_update_post_returns_modified_data(api_context: APIRequestContext):
    payload = {"id": 1, "title": "Updated Title", "body": "Updated body", "userId": 1}

    response = api_context.put("/posts/1", data=payload)

    assert response.status == 200
    updated = response.json()
    assert updated["title"] == "Updated Title"


@pytest.mark.api
def test_delete_post_returns_200(api_context: APIRequestContext):
    response = api_context.delete("/posts/1")

    assert response.status == 200


@pytest.mark.api
def test_get_comments_for_post(api_context: APIRequestContext):
    response = api_context.get("/posts/1/comments")

    assert response.status == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) > 0
    assert all("email" in c for c in comments)


@pytest.mark.api
def test_get_nonexistent_post_returns_404(api_context: APIRequestContext):
    response = api_context.get("/posts/99999")

    assert response.status == 404


@pytest.mark.api
def test_filter_posts_by_user(api_context: APIRequestContext):
    response = api_context.get("/posts?userId=1")

    assert response.status == 200
    posts = response.json()
    assert all(p["userId"] == 1 for p in posts)
