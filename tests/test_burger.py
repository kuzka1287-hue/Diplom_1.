# tests/test_burger.py

import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient


class TestBurger:
    """Класс с тестами для Burger."""

    # ---- Тесты для set_buns ----

    def test_set_buns(self, burger):
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 100.0
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun
        assert burger.bun.get_name() == "white bun"
        assert burger.bun.get_price() == 100.0

    # ---- Тесты для add_ingredient ----

    def test_add_ingredient(self, burger):
        mock_ingredient = Mock(spec=Ingredient)
        mock_ingredient.get_name.return_value = "cutlet"
        mock_ingredient.get_price.return_value = 150.0
        burger.add_ingredient(mock_ingredient)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient

    # ---- Тесты для remove_ingredient ----

    def test_remove_ingredient(self, burger):
        ing1 = Mock(spec=Ingredient)
        ing2 = Mock(spec=Ingredient)
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ing2

    def test_remove_ingredient_out_of_range(self, burger):
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

    # ---- Тесты для move_ingredient ----

    def test_move_ingredient(self, burger):
        ing1 = Mock(spec=Ingredient)
        ing2 = Mock(spec=Ingredient)
        ing3 = Mock(spec=Ingredient)
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.add_ingredient(ing3)
        burger.move_ingredient(0, 2)
        assert burger.ingredients[0] == ing2
        assert burger.ingredients[1] == ing3
        assert burger.ingredients[2] == ing1

    def test_move_ingredient_out_of_range(self, burger):
        with pytest.raises(IndexError):
            burger.move_ingredient(5, 0)

    # ---- Параметризованные тесты для get_price ----

    @pytest.mark.parametrize(
        "bun_price, ingredient_prices, expected_price",
        [
            (100.0, [50.0, 30.0], 280.0),
            (200.0, [], 400.0),
            (150.0, [10.0, 20.0, 30.0], 360.0),
        ]
    )
    def test_get_price(self, burger, bun_price, ingredient_prices, expected_price):
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        for price in ingredient_prices:
            mock_ing = Mock(spec=Ingredient)
            mock_ing.get_price.return_value = price
            burger.add_ingredient(mock_ing)
        assert burger.get_price() == expected_price

    # ---- Параметризованные тесты для get_receipt ----

    @pytest.mark.parametrize(
        "bun_name, bun_price, ingredients_info, expected_lines",
        [
            (
                "black bun",
                100.0,
                [],
                [
                    "(==== black bun ====)",
                    "(==== black bun ====)",
                    "Price: 200.0"
                ]
            ),
            (
                "white bun",
                200.0,
                [("SAUCE", "hot sauce", 100.0)],
                [
                    "(==== white bun ====)",
                    "= sauce hot sauce =",
                    "(==== white bun ====)",
                    "Price: 500.0"
                ]
            ),
            (
                "red bun",
                300.0,
                [
                    ("SAUCE", "chili sauce", 50.0),
                    ("FILLING", "cutlet", 150.0)
                ],
                [
                    "(==== red bun ====)",
                    "= sauce chili sauce =",
                    "= filling cutlet =",
                    "(==== red bun ====)",
                    "Price: 800.0"
                ]
            ),
        ]
    )
    def test_get_receipt(self, burger, bun_name, bun_price, ingredients_info, expected_lines):
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        for ing_type, ing_name, ing_price in ingredients_info:
            mock_ing = Mock(spec=Ingredient)
            mock_ing.get_type.return_value = ing_type
            mock_ing.get_name.return_value = ing_name
            mock_ing.get_price.return_value = ing_price
            burger.add_ingredient(mock_ing)
        receipt = burger.get_receipt()
        receipt_lines = receipt.split('\n')
        assert len(receipt_lines) == len(expected_lines)
        for expected, actual in zip(expected_lines, receipt_lines):
            assert expected == actual
