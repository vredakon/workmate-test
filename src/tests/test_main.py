import pytest
import os
from src.script.main import *


project_path = os.path.join(os.path.dirname(__file__), "..", "..")


def average(values: list[int | float]) -> float: 
    return (sum(values) / len(values)).__round__(2)
      
                      
@pytest.fixture
def result_entries():
    entries = [
        {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
        {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
        {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'},
        {'name': 'iphone 14', 'brand': 'apple', 'price': '799', 'rating': '4.7'},
        {'name': 'galaxy a54', 'brand': 'samsung', 'price': '349', 'rating': '4.2'},
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.4'},
        {'name': 'iphone se', 'brand': 'apple', 'price': '429', 'rating': '4.1'},
        {'name': 'galaxy z flip 5', 'brand': 'samsung', 'price': '999', 'rating': '4.6'},
        {'name': 'redmi 10c', 'brand': 'xiaomi', 'price': '149', 'rating': '4.1'},
        {'name': 'iphone 13 mini', 'brand': 'apple', 'price': '599', 'rating': '4.5'},
    ]
    
    return entries


@pytest.fixture
def grouped_entries():
    entries = {'apple': 4.55, 'samsung': 4.53, 'xiaomi': 4.37}
    return entries


class TestProcessFiles:
    
    def test_process_files_success(self, result_entries):
        """Проверка на успешное выполнение при верных аргументах"""
        directories = ["products1.csv", "products2.csv"]
        assert process_files(directories) == result_entries
        
    
    def test_process_files_wrong_filetype_error(self):
        """Проверка на ошибку при неподходящем типе хотя бы из одного из файлов1"""
        directories = ["products1.csv", "products2.txt"]
        with pytest.raises(Exception):
            process_files(directories)
    
    
    def test_process_files_empty_directories(self):
        """Проверка на выполнение при отсутствии директорий"""
        """
        Вообще такой ситуации быть не должно так как в тестах парсера стоит проверка на наличие аргументов,
        но на всякий случай решил сделать
        """
        directories = []
        assert process_files(directories) == []
        

    def test_process_files_absolute_paths(self, result_entries):
        """Проверка на успешное выполнение при верных абсолютных расположениях"""
        directories = [os.path.join(project_path, "products1.csv"), os.path.join(project_path, "products2.csv")]
        assert process_files(directories) == result_entries
        

class TestGroupBy:
    
    def test_group_by_success(self, result_entries, grouped_entries):
        assert group_by(result_entries, "brand", "rating", average) == grouped_entries
    
    
    def test_group_by_unknown_field_name_error(self, result_entries):
        with pytest.raises(Exception):
            group_by(result_entries, "unknown", "rating", average)
    
    
    def test_group_by_unknown_function_error(self, result_entries):
        with pytest.raises(Exception):
            group_by(result_entries, "brand", "rating", unknown)
    
    
    def test_group_by_unknown_bad_entries_error(self):
        bad_result_entries = [{'_name': 'iphone 15 pro', '_brand': 'apple', '_price': '999', '_rating': '4.9'}]
        with pytest.raises(Exception):
            group_by(bad_result_entries, "brand", "rating", average)
    
    
    def test_group_by_unknown_bad_entries_type_error(self):
        bad_result_entries = ['_name', 'iphone 15 pro', '_brand', 'apple', '_price', '999', '_rating', '4.9']
        with pytest.raises(Exception):
            group_by(bad_result_entries, "brand", "rating", average)