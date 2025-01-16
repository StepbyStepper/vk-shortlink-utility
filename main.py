from dotenv import load_dotenv
import requests
from urllib.parse import urlparse
import os
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="VK Shortlink Utility")
    parser.add_argument("url", help="Ссылка для сокращения или подсчёта кликов")
    return parser.parse_args()


def check_token(token):
    url = "https://api.vk.com/method/users.get"
    params = {"access_token": token, "v": "5.131"}
    response = requests.get(url, params=params)
    response_data = response.json()
    if "error" in response_data:
        raise ValueError(f"Токен недействителен: {response_data['error'].get('error_msg', 'Неизвестная ошибка')}")
    print("Токен валиден.")


def shorten_link(token, link):
    url = "https://api.vk.com/method/utils.getShortLink"
    params = {
        "url": link,
        "access_token": token,
        "v": "5.131"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_data = response.json()
    if "error" in response_data:
        raise ValueError(f"Ошибка от API: {response_data['error'].get('error_msg', 'Неизвестная ошибка')}")
    return response_data["response"]["short_url"]


def count_clicks(token, short_link):
    parsed_url = urlparse(short_link)
    link_key = parsed_url.path.strip("/")

    if not link_key:
        raise ValueError("Ссылка некорректна: отсутствует идентификатор короткой ссылки.")

    url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "key": link_key,
        "access_token": token,
        "v": "5.131",
        "interval": "forever"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_data = response.json()

    if "error" in response_data:
        raise ValueError(f"Ошибка от API: {response_data['error'].get('error_msg', 'Неизвестная ошибка')}")

    stats = response_data.get("response", {}).get("stats", [])
    if not stats:
        raise ValueError("Нет данных о переходах по этой ссылке.")

    return stats[0]["views"]


def is_shorten_link(token, url):
    parsed_url = urlparse(url)
    link_key = parsed_url.path.strip("/")

    if parsed_url.netloc != "vk.cc":
        return False

    if not link_key:
        raise ValueError("Ссылка некорректна: отсутствует идентификатор короткой ссылки.")

    api_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "key": link_key,
        "access_token": token,
        "v": "5.131",
        "interval": "forever"
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    response_data = response.json()

    if "error" in response_data:
        error_msg = response_data['error'].get('error_msg', 'Неизвестная ошибка')
        raise ValueError(f"Ссылка недоступна: {error_msg}")

    return True


if __name__ == "__main__":
    load_dotenv()

    args = parse_arguments()

    vk_token = os.getenv("VK_ACCESS_TOKEN")
    if not vk_token:
        raise EnvironmentError(
            "Переменная окружения VK_ACCESS_TOKEN не задана. Убедитесь, что она настроена в .env файле.")

    user_input = args.url

    try:
        check_token(vk_token)

        if is_shorten_link(vk_token, user_input):
            clicks = count_clicks(vk_token, user_input)
            print(f"Количество переходов по ссылке: {clicks}")
        else:
            short_url = shorten_link(vk_token, user_input)
            print("Сокращенная ссылка: ", short_url)
    except requests.exceptions.HTTPError:
        print("Ошибка HTTP при выполнении запроса.")
    except ValueError as e:
        print(f"Ошибка: {e}")