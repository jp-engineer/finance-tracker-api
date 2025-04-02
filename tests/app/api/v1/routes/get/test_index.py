def test_get_index_welcome_message(client, api_prefix):
    response = client.get(f"{api_prefix}/get-status-message")
    assert response.status_code == 200
    assert response.json() == {"message": "finance-tracker API is running"}
