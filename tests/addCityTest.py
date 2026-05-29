import sys
import os
import pytest
import json
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gestion import addCity


PARIS = {"nom": "Paris", "lat": 48.8566, "long": 2.3522}
LYON  = {"nom": "Lyon",  "lat": 45.7640, "long": 4.8357}


def makeApiResponse(status="OK", lat=48.8566, lng=2.3522):
    if status == "ZERO_RESULTS":
        return {"status": "ZERO_RESULTS"}
    return {
        "status": "OK",
        "results": [{"geometry": {"location": {"lat": lat, "lng": lng}}}]
    }


class TestGetCityCoords:

    def testValidCityReturnsCoords(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = makeApiResponse(lat=48.8566, lng=2.3522)
        with patch("requests.get", return_value=mock_resp):
            result = addCity.getCityCoords("Paris")
        assert result == PARIS

    def testInvalidCityReturnsNone(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = makeApiResponse(status="ZERO_RESULTS")
        with patch("requests.get", return_value=mock_resp):
            result = addCity.getCityCoords("XYZNotACity")
        assert result is None

    def testInvalidCityPrintsError(self, capsys):
        mock_resp = MagicMock()
        mock_resp.json.return_value = makeApiResponse(status="ZERO_RESULTS")
        with patch("requests.get", return_value=mock_resp):
            addCity.getCityCoords("XYZNotACity")
        assert "XYZNotACity" in capsys.readouterr().out

    def testPassesCityNameToApi(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = makeApiResponse()
        with patch("requests.get", return_value=mock_resp) as mock_get:
            addCity.getCityCoords("Lyon")
        call_params = mock_get.call_args.kwargs["params"]
        assert call_params["address"] == "Lyon"


class TestIsCityPresent:

    def testCityPresent(self):
        assert addCity.isCityPresent([PARIS], "Paris") is True

    def testCityAbsent(self):
        assert addCity.isCityPresent([PARIS], "Lyon") is False

    def testCaseInsensitiveLower(self):
        assert addCity.isCityPresent([PARIS], "paris") is True

    def testCaseInsensitiveUpper(self):
        assert addCity.isCityPresent([PARIS], "PARIS") is True

    def testEmptyListReturnsFalse(self):
        assert addCity.isCityPresent([], "Paris") is False

    def testMultipleCities(self):
        assert addCity.isCityPresent([PARIS, LYON], "Lyon") is True


class TestGetUserEntry:

    def testExistingUserIsFound(self):
        data = [{"pseudo": "alice", "villes": [PARIS]}]
        entry = addCity.getUserEntry(data, "alice")
        assert entry["pseudo"] == "alice"
        assert entry["villes"] == [PARIS]

    def testDataNotModifiedForExistingUser(self):
        data = [{"pseudo": "alice", "villes": []}]
        addCity.getUserEntry(data, "alice")
        assert len(data) == 1

    def testNewUserIsCreated(self):
        data = []
        entry = addCity.getUserEntry(data, "bob")
        assert entry == {"pseudo": "bob", "villes": []}

    def testNewUserAppendedToData(self):
        data = [{"pseudo": "alice", "villes": []}]
        addCity.getUserEntry(data, "bob")
        assert len(data) == 2
        assert data[1]["pseudo"] == "bob"

    def testReturnsCorrectUserAmongMultiple(self):
        data = [
            {"pseudo": "alice", "villes": []},
            {"pseudo": "bob",   "villes": [PARIS]},
        ]
        entry = addCity.getUserEntry(data, "bob")
        assert entry["villes"] == [PARIS]


class TestLoadCities:

    def testLoadsJsonFromFile(self):
        fake_data = [{"pseudo": "alice", "villes": []}]
        m = mock_open(read_data=json.dumps(fake_data))
        with patch("builtins.open", m):
            result = addCity.loadCities()
        assert result == fake_data

    def testReturnsList(self):
        m = mock_open(read_data=json.dumps([]))
        with patch("builtins.open", m):
            result = addCity.loadCities()
        assert isinstance(result, list)


class TestSaveCities:

    def testWritesJsonToFile(self):
        fake_data = [{"pseudo": "alice", "villes": [PARIS]}]
        m = mock_open()
        with patch("builtins.open", m):
            addCity.saveCities(fake_data)
        handle = m()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        assert json.loads(written) == fake_data


class TestAddCity:

    def testAddsCitySuccessfully(self, capsys):
        data = [{"pseudo": "alice", "villes": []}]
        with patch("connexion.login.currentUser", "alice"), \
             patch("gestion.addCity.getCityCoords", return_value=PARIS), \
             patch("gestion.addCity.loadCities", return_value=data), \
             patch("gestion.addCity.saveCities") as mock_save:
            result = addCity.addCity("Paris")
        assert result == [PARIS]
        mock_save.assert_called_once()
        assert "Paris added to your list" in capsys.readouterr().out

    def testDoesNotAddDuplicate(self, capsys):
        data = [{"pseudo": "alice", "villes": [PARIS]}]
        with patch("connexion.login.currentUser", "alice"), \
             patch("gestion.addCity.getCityCoords", return_value=PARIS), \
             patch("gestion.addCity.loadCities", return_value=data), \
             patch("gestion.addCity.saveCities") as mock_save:
            result = addCity.addCity("Paris")
        assert result is None
        mock_save.assert_not_called()
        assert "already in the list" in capsys.readouterr().out

    def testCreatesUserEntryIfMissing(self):
        data = []
        with patch("connexion.login.currentUser", "newUser"), \
             patch("gestion.addCity.getCityCoords", return_value=PARIS), \
             patch("gestion.addCity.loadCities", return_value=data), \
             patch("gestion.addCity.saveCities"):
            result = addCity.addCity("Paris")
        assert result == [PARIS]

    def testDoesNotAffectOtherUsers(self):
        data = [
            {"pseudo": "alice", "villes": [PARIS]},
            {"pseudo": "bob",   "villes": []},
        ]
        with patch("connexion.login.currentUser", "bob"), \
             patch("gestion.addCity.getCityCoords", return_value=LYON), \
             patch("gestion.addCity.loadCities", return_value=data), \
             patch("gestion.addCity.saveCities"):
            addCity.addCity("Lyon")
        assert data[0]["villes"] == [PARIS]
        assert data[1]["villes"] == [LYON]
