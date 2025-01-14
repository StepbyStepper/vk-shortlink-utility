# VK Shortlink Utility

Утилита для работы с короткими ссылками VK: сокращение длинных ссылок и подсчёт переходов по коротким ссылкам.

---

## Требования

- Python 3.8+
- Установленные зависимости из `requirements.txt`

---

## Установка

1. **Клонируйте репозиторий**:

   ```bash
   git clone https://github.com/username/vk-shortlink-utility.git
   cd vk-shortlink-utility
   ```

2. **Установите зависимости**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Создайте файл `.env`** и добавьте токен VK:

   ```plaintext
   VK_ACCESS_TOKEN=ваш_токен
   ```

---

## Использование

### Сократить ссылку

Для сокращения длинной ссылки:

```bash
python main.py "https://example.com"
```

### Подсчитать клики по короткой ссылке

Для подсчёта количества переходов по короткой ссылке VK:

```bash
python main.py "https://vk.cc/abcd12"
```

---

## Пример результата

### Сокращение длинной ссылки

Ввод:
```bash
python main.py "https://example.com"
```
Вывод:
```plaintext
Сокращенная ссылка: https://vk.cc/abcd12
```

### Подсчёт кликов по короткой ссылке

Ввод:
```bash
python main.py "https://vk.cc/abcd12"
```
Вывод:
```plaintext
Количество переходов по ссылке: 123
```

---

## Описание работы

Этот скрипт выполняет две основные функции:

1. **Сокращение длинных ссылок** с помощью API VK (`utils.getShortLink`).
2. **Подсчёт переходов** по коротким ссылкам VK с использованием метода `utils.getLinkStats`.

Сначала скрипт проверяет, является ли ссылка короткой ссылкой VK. Если да, он пытается получить статистику переходов. Если это обычная ссылка, она сокращается с использованием API VK.

---

## Обработка ошибок

Если что-то пойдёт не так, скрипт выведет соответствующее сообщение об ошибке. Например:

- **Ошибка HTTP**:
  ```plaintext
  Ошибка HTTP при выполнении запроса.
  ```
- **Неверный токен**:
  ```plaintext
  Токен недействителен: ошибка авторизации.
  ```
- **Некорректная ссылка**:
  ```plaintext
  Ссылка некорректна: отсутствует идентификатор короткой ссылки.
  ```

---

## Лицензия

Этот проект распространяется под свободной лицензией. Вы можете использовать его для любых целей.

