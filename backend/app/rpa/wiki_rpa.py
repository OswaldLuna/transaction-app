import sys
from playwright.sync_api import sync_playwright
import requests

API_URL = "http://localhost:8000/assistant/summarize" 

def extract_first_paragraph(term: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to Wikipedia
        page.goto("https://es.wikipedia.org/wiki/Especial:Buscar")

        # Search term
        page.fill("input[name='search']", term)
        page.keyboard.press("Enter")

        page.wait_for_selector("p")

        paragraph = page.query_selector("p").inner_text()

        browser.close()

        return paragraph


def send_to_api(text: str):
    payload = {"text": text}
    res = requests.post(API_URL, json=payload)

    if res.status_code != 200:
        raise Exception(f"Error: {res.text}")

    return res.json()["summary"]


def run_rpa(term: str):
    print(f"🔍 Buscando: {term}")
    paragraph = extract_first_paragraph(term)

    print("\n📘Párrafo extraído:")
    print(paragraph)

    summary = send_to_api(paragraph)

    print("\nResumen generado por IA:")
    print(summary)

    return summary

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python wiki_rpa.py <termino>")
        sys.exit(1)

    term = " ".join(sys.argv[1:])
    run_rpa(term)
