from app import registry

from .conftest import connect_ws, register


class TestRegistration:
    def test_register_returns_id_and_name(self, client):
        me = register(client)
        assert me["id"]
        assert "(" in me["name"] and ")" in me["name"]

    def test_phone_user_agent_detected(self, client):
        me = register(client, "Mozilla/5.0 (iPhone; Mobile) Safari")
        assert me["kind"] == "Phone"
        assert "Phone" in me["name"]

    def test_desktop_user_agent_detected(self, client):
        me = register(client, "Mozilla/5.0 Chrome/120")
        assert me["kind"] == "Desktop"

    def test_names_are_unique(self, client):
        names = {register(client)["id"] for _ in range(10)}
        assert len(names) == 10

    def test_unknown_client_gets_lookup_none(self):
        assert registry.get_client("nope") is None


class TestPeers:
    def test_empty_when_alone(self, client):
        me = register(client)
        with connect_ws(client, me["id"]) as ws:
            peers = ws.receive_json()
        assert peers == {"event": "peers", "peers": []}

    def test_peers_exclude_self(self, client):
        a = register(client, "Chrome A")
        b = register(client, "Chrome B")
        with connect_ws(client, a["id"]) as wsa:
            wsa.receive_json()
            with connect_ws(client, b["id"]) as wsb:
                update_for_a = wsa.receive_json()
                ids_a = [p["id"] for p in update_for_a["peers"]]
                assert b["id"] in ids_a
                assert a["id"] not in ids_a
                wsb.receive_json()

    def test_disconnect_removes_peer(self, client):
        a = register(client, "Chrome A")
        b = register(client, "Chrome B")
        with connect_ws(client, a["id"]) as wsa:
            wsa.receive_json()
            with connect_ws(client, b["id"]) as wsb:
                wsa.receive_json()
                wsb.receive_json()
            after_leave = wsa.receive_json()
        ids = [p["id"] for p in after_leave["peers"]]
        assert b["id"] not in ids


class TestTextTransfer:
    def test_text_delivery(self, client):
        sender = register(client, "Chrome Sender")
        receiver = register(client, "Firefox Receiver")
        with connect_ws(client, receiver["id"]) as wsr:
            wsr.receive_json()
            response = client.post(
                f"/api/send/{receiver['id']}/text",
                json={"sender_id": sender["id"], "text": "hello beam"},
            )
            assert response.status_code == 200
            msg = wsr.receive_json()
            assert msg["event"] == "text"
            assert msg["text"] == "hello beam"

    def test_text_to_offline_peer_404(self, client):
        sender = register(client)
        response = client.post(
            f"/api/send/ghost/text",
            json={"sender_id": sender["id"], "text": "hi"},
        )
        assert response.status_code == 404

    def test_cannot_send_to_self(self, client):
        me = register(client)
        with connect_ws(client, me["id"]) as ws:
            ws.receive_json()
            response = client.post(
                f"/api/send/{me['id']}/text",
                json={"sender_id": me["id"], "text": "note to self"},
            )
            assert response.status_code == 400

    def test_empty_text_rejected(self, client):
        sender = register(client)
        receiver = register(client)
        with connect_ws(client, receiver["id"]) as wsr:
            wsr.receive_json()
            response = client.post(
                f"/api/send/{receiver['id']}/text",
                json={"sender_id": sender["id"], "text": ""},
            )
            assert response.status_code == 422


class TestFileTransfer:
    def test_file_delivery_and_one_time_download(self, client):
        sender = register(client, "Chrome Sender")
        receiver = register(client, "Safari Receiver")
        with connect_ws(client, receiver["id"]) as wsr:
            wsr.receive_json()
            response = client.post(
                f"/api/send/{receiver['id']}/file",
                data={"sender_id": sender["id"]},
                files={"files": ("notes.txt", b"secret content")},
            )
            assert response.status_code == 200
            msg = wsr.receive_json()
            assert msg["event"] == "files"
            file_info = msg["files"][0]
            assert file_info["name"] == "notes.txt"
            assert file_info["size"] == len(b"secret content")

            dl = client.get(f"/download/{file_info['token']}")
            assert dl.status_code == 200
            assert dl.content == b"secret content"

            second = client.get(f"/download/{file_info['token']}")
            assert second.status_code == 404

    def test_multiple_files(self, client):
        sender = register(client, "Chrome S")
        receiver = register(client, "Edge R")
        with connect_ws(client, receiver["id"]) as wsr:
            wsr.receive_json()
            response = client.post(
                f"/api/send/{receiver['id']}/file",
                data={"sender_id": sender["id"]},
                files=[
                    ("files", ("a.txt", b"AAA")),
                    ("files", ("b.txt", b"BBB")),
                ],
            )
            assert response.status_code == 200
            msg = wsr.receive_json()
            assert len(msg["files"]) == 2

    def test_download_invalid_token_404(self, client):
        assert client.get("/download/bogus-token").status_code == 404

    def test_file_to_offline_peer_404(self, client, tmp_path):
        sender = register(client)
        response = client.post(
            "/api/send/offline/file",
            data={"sender_id": sender["id"]},
            files={"files": ("x.txt", b"x")},
        )
        assert response.status_code == 404

    def test_expired_transfer_is_purged(self, client, monkeypatch):
        path = registry.STORAGE / "old.txt"
        path.write_bytes(b"old")
        token = registry.add_transfer(path, "old.txt")
        registry.transfers[token]["created_at"] -= 10_000
        registry.cleanup_expired()
        assert registry.pop_transfer(token) is None
        assert not path.exists()


class TestMisc:
    def test_health(self, client):
        assert client.get("/health").json() == {"status": "ok"}

    def test_qr_endpoint_returns_svg(self, client):
        response = client.get("/qr.svg")
        assert response.status_code == 200
        assert b"<svg" in response.content or b"<?xml" in response.content

    def test_home_serves_dashboard(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "DropBeam" in response.text

    def test_ws_with_unknown_id_rejected(self, client):
        try:
            with connect_ws(client, "ghost"):
                pass
            raised = False
        except Exception:
            raised = True
        assert raised
