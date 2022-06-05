# Open scriptures from clipboard

import pyperclip
import re
import json
import webbrowser
from time import sleep
import os

bible_books_json_file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'bible-books.json'))
with open(bible_books_json_file_path, 'r') as file:
    bible_books_text = file.read()

bible_books_info = json.loads(bible_books_text)

del bible_books_text
del bible_books_json_file_path
del os

def main_loop():
    old_clipboard = pyperclip.paste()
    while True:
        status, new_clipboard = check_clipboard_change(old_clipboard)
        print("Clipboard Update Detected:", status)
        if status:
            old_clipboard = new_clipboard
            extraction = extract_scripture_like_pattern(old_clipboard)
            print("Extracted Text:", extraction)
            if extraction:
                scripture = parse_scripture(extraction)
                if check_valid_scripture(scripture):
                    print("Valid Scripture")
                    url = create_scripture_link(scripture)
                    webbrowser.open(url)
                else:
                    print("Invalid Scripture")
        print("-"*50)
        sleep(3)

def check_clipboard_change(old_content: str) -> tuple[bool, str]:
    new_content = pyperclip.paste()
    return (old_content != new_content, new_content)

def extract_scripture_like_pattern(content: str):
    scripture_pattern = re.compile("[1-3]?[A-Z][a-z]{1,3} [1-9][0-9]{0,2}:[1-9][0-9]{0,2}")
    found_chunk = scripture_pattern.search(content)
    if found_chunk:
        return found_chunk.group()
    return ""

def parse_scripture(content: str):
    split_text = content.split()
    book = split_text[0]
    numbers = split_text[1]
    chapter = numbers.split(":")[0]
    verse = numbers.split(":")[1]
    return {'book': book, 'chapter': int(chapter), 'verse': int(verse)}

def check_valid_scripture(scripture) -> bool:
    if scripture['book'] not in bible_books_info:
        return False 
    if (scripture['chapter']) > len(bible_books_info[scripture['book']]['verses-by-chapter']):
        return False
    if scripture['verse'] > bible_books_info[scripture['book']]['verses-by-chapter'][scripture['chapter']-1]:
        return False
    return True

def create_scripture_link(scripture):
    book_number = str(bible_books_info[scripture['book']]['number']).rjust(2, '0')
    chapter_number = str(scripture['chapter']).rjust(3, '0')
    verse_number = str(scripture['verse']).rjust(3, '0')
    scripture_number = book_number + chapter_number + verse_number
    return f'https://www.jw.org/finder?srcid=jwlshare&wtlocale=E&prefer=lang&bible={scripture_number}&pub=nwtsty'

if __name__ == "__main__":
    main_loop()
