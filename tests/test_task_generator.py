import unittest
from unittest.mock import patch
from source.task_generator import TaskGenerator

class TestTaskGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = TaskGenerator()

    def test_init_exception_handling(self):
        """Проверяем, что при ошибке парсера используются запасные коды."""
        # Патчим parse_file так, чтобы он кидал ошибку
        with patch('source.task_generator.parse_file', side_effect=ValueError("Empty")):
            gen = TaskGenerator()
            self.assertIn((1, 2, 3), gen.valid_codes_pool)

    def test_generate_task_basic(self):
        """Проверяем, что генератор возвращает данные нужных типов."""
        secret, rules = self.generator.generate_task(num_rules=2)
        self.assertIsInstance(secret, tuple)
        self.assertIsInstance(rules, list)
        self.assertEqual(len(rules), 2)

    def test_pool_refresh(self):
        """Проверяем восстановление пула."""
        self.generator.active_pool = []
        self.generator.generate_task(num_rules=1)
        self.assertGreater(len(self.generator.active_pool), 0)

    def test_attribute_error_does_not_break_loop(self):
        """Проверяем, что левые методы в списке правил не вешают генератор."""
        # Добавляем мусор в правила
        self.generator.rule_generator.combinations_list.append(("fake_method", ()))
        # Если не упало с AttributeError — тест пройден
        res = self.generator.generate_task(num_rules=1)
        self.assertIsNotNone(res)

    def test_fallback_logic(self):
        """Тестируем ветку, когда уникальное решение не найдено."""
        # Заставляем генератор думать, что решений всегда 0 или много
        with patch.object(self.generator.rule_generator, 'find_all_solutions', return_value=[]):
            secret, rules = self.generator.generate_task(num_rules=1)
            # Должен вернуться любой код из valid_codes_pool
            self.assertIn(secret, self.generator.valid_codes_pool)