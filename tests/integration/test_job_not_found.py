from __future__ import annotations


def test_get_missing_job_returns_404(client):
    # The client fixture uses a fresh, empty test database for each test.
    response = client.get("/jobs/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}
