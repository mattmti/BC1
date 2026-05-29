import sys
import os
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch('builtins.input', side_effect=['1', '7']), \
     patch('connexion.login.login'), \
     patch('viewTour.viewPublicTours', create=True):
    import menu


class TestMainMenu:

    def test_choice_1_calls_login_and_connected_menu(self):
        with patch('builtins.input', return_value='1'), \
             patch('connexion.login.login') as mock_login, \
             patch('menu.connectedMenu') as mock_connected:
            menu.mainMenu()
            mock_login.assert_called_once()
            mock_connected.assert_called_once()

    def test_choice_2_calls_view_public_tours(self):
        inputs = iter(['2', '1'])
        with patch('builtins.input', side_effect=inputs), \
             patch('viewTour.viewPublicTours', create=True) as mock_view, \
             patch('connexion.login.login'), \
             patch('menu.connectedMenu'):
            menu.mainMenu()
            mock_view.assert_called_once()

    def test_invalid_choice_prints_error(self, capsys):
        inputs = iter(['invalid', '1'])
        with patch('builtins.input', side_effect=inputs), \
             patch('connexion.login.login'), \
             patch('menu.connectedMenu'):
            menu.mainMenu()
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out


class TestConnectedMenu:

    def test_choice_1_views_city_list(self):
        inputs = iter(['1', '7'])
        with patch('builtins.input', side_effect=inputs), \
             patch('gestion.viewList.viewList') as mock_view:
            menu.connectedMenu()
            mock_view.assert_called_once()

    def test_choice_2_adds_one_city(self):
        inputs = iter(['2', 'Paris', 'no', '7'])
        with patch('builtins.input', side_effect=inputs), \
             patch('gestion.addCity.addCity') as mock_add:
            menu.connectedMenu()
            mock_add.assert_called_once_with('Paris')

    def test_choice_2_adds_multiple_cities(self):
        inputs = iter(['2', 'Paris', 'Lyon', 'no', '7'])
        with patch('builtins.input', side_effect=inputs), \
             patch('gestion.addCity.addCity') as mock_add:
            menu.connectedMenu()
            assert mock_add.call_count == 2
            mock_add.assert_any_call('Paris')
            mock_add.assert_any_call('Lyon')

    def test_choice_3_generates_tour(self):
        from connexion import login as _login
        _login.currentUser = 'testUser'
        inputs = iter(['3', '7'])
        with patch('builtins.input', side_effect=inputs), \
             patch('ittineraire.generateTour.loadCitiesInFiles') as mock_gen:
            menu.connectedMenu()
            mock_gen.assert_called_once_with('testUser')

    def test_choice_4_views_my_tours(self):
        inputs = iter(['4', '7'])
        with patch('builtins.input', side_effect=inputs), \
             patch('viewMyTour.viewMyTours', create=True) as mock_view:
            menu.connectedMenu()
            mock_view.assert_called_once()

    def test_choice_5_deletes_city(self):
        inputs = iter(['5', '7'])
        with patch('builtins.input', side_effect=inputs), \
             patch('gestion.deleteCity.deleteCity') as mock_delete:
            menu.connectedMenu()
            mock_delete.assert_called_once()

    def test_choice_6_deletes_all_cities(self):
        inputs = iter(['6', '7'])
        with patch('builtins.input', side_effect=inputs), \
             patch('gestion.deleteAll.DeleteEveryCity') as mock_delete:
            menu.connectedMenu()
            mock_delete.assert_called_once()

    def test_choice_7_logs_out(self):
        from connexion import login as _login
        _login.currentUser = 'testUser'
        with patch('builtins.input', return_value='7'):
            menu.connectedMenu()
        assert _login.currentUser is None

    def test_invalid_choice_prints_error(self, capsys):
        inputs = iter(['invalid', '7'])
        with patch('builtins.input', side_effect=inputs):
            menu.connectedMenu()
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out