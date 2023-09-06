def test_app(client):
    response = client.get("/")
    assert b"<title>TJAL/TJCE - Crawler API</title>" in response.data

def test_invalid_input(client, app):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = client.post("/api/processos", headers=headers, json={"processo":"teste"})
    body = response.json
    assert response.status_code == 400
    assert "Você precisa enviar o número do processo (process_numbers)" in body["msg"]

def test_invalid_process(client, app):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = client.post("/api/processos", headers=headers, json={"process_numbers": "0710802-55.2018.8.02.0001,0710802-55.2018.8.02.0001,0710802-55.2018.8.12.0001,0710802-55.2018.8.02.0001"})
    body = response.json
    assert response.status_code == 400
    assert "Processo inválido (tribunal inválido)" in body["msg"]

def test_max_limit_process(client, app):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = client.post("/api/processos", headers=headers, json={"process_numbers": '''0710802-55.2018.8.02.0001,0710802-55.2018.8.02.0001,0710802-55.2018.8.12.0001,0710802-55.2018.8.02.0001,0710802-55.2018.8.02.0001,0710802-55.2018.8.02.0001,0710802-55.2018.8.12.0001,
                                                                    0710802-55.2018.8.02.0001,0710802-55.2018.8.02.0001,0710802-55.2018.8.02.0001,0710802-55.2018.8.12.0001,0710802-55.2018.8.02.0001'''})
    body = response.json
    assert response.status_code == 400
    assert "Quantidade máxima de processos por" in body["msg"]

def test_success_return(client, app):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = client.post("/api/processos", headers=headers, json={"process_numbers": "0070337-91.2008.8.06.0001,0705307-93.2019.8.02.0001"})
    body = response.json
    assert response.status_code == 200
    assert len(body["processos"]) == 2
    assert body["processos"][0]["processo"] == "0070337-91.2008.8.06.0001"
    assert body["processos"][1]["processo"] == "0705307-93.2019.8.02.0001"
    assert len(body["processos"][0]["result"]["grau1"]) == 1
    assert len(body["processos"][0]["result"]["grau2"]) == 2
    assert len(body["processos"][1]["result"]["grau1"]) == 1
    assert len(body["processos"][1]["result"]["grau2"]) == 1



