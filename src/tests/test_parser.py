import pytest
import os
import sys
import argparse


def create_parser():
    """Функция создающая парсер с аргументами"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", "-f", type=str, required=True, nargs="+")
    parser.add_argument("--report", "-r", type=str, required=True)
    return parser


@pytest.fixture
def parser():
    return create_parser()


class TestParser:
    
    def test_args_short(self, parser) -> None:
        """Проверка коротких аргументов"""
        args = parser.parse_args(["-f", "products1.csv", "products2.csv", "-r", "average-rating"])
        assert args.files == ["products1.csv", "products2.csv"]
        assert args.report == "average-rating"
        
    
    def test_args_long(self, parser):
        """Проверка полных аргументов"""
        args = parser.parse_args(["--files", "products1.csv", "products2.csv", "--report", "average-rating"])
        assert args.files == ["products1.csv", "products2.csv"]
        assert args.report == "average-rating"
        
    
    def test_mixed_args(self, parser):
        """Проверка смешанных аргументов"""
        args = parser.parse_args(["--files", "products1.csv", "products2.csv", "--report", "average-rating"])
        assert args.files == ["products1.csv", "products2.csv"]
        assert args.report == "average-rating"


class TestParserErrors:
    
    def test_known_and_unknown_args_error(self, parser):
        """Проверка на ошибку при наличии известных и неизвестных аргументов"""
        with pytest.raises(SystemExit):
            parser.parse_args(["-f" "products.csv", "-r", "average-rating", "-u", "unknown-arg"])
        
    
    def test_unknown_args_error(self, parser):
        """Проверка на ошибку при наличие только неизвестных аргументов"""
        with pytest.raises(SystemExit):
            parser.parse_args(["-u", "unknown-arg"])
            
    
    def test_empty_args_error(self, parser):
        """Проверка на ошибку при отсутствии аргументов"""
        with pytest.raises(SystemExit):
            parser.parse_args()
            
            
    def test_empty_args_values_error(self, parser):
        """Проверка на ошибку при отсутствии значений аргументов"""
        with pytest.raises(SystemExit):
            parser.parse_args(["-f", "-r"])
            

    def test_empty_args_flags_error(self, parser):
        """Проверка на ошибку при отсутствии флагов"""
        with pytest.raises(SystemExit):
            parser.parse_args(["products.csv", "average-rating"])