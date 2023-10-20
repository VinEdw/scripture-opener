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
            print("Extracted Text:", extraction.group() if extraction is not None else None)
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

def extract_scripture_like_pattern(content: str) -> re.Match[str]|None:
    book_part = "(?P<book>[1-3]?[A-Z][a-z]{1,3})"
    chapter_part = "(?P<chapter>[1-9][0-9]{0,2})"
    verse_start_part = "(?P<start>[1-9][0-9]{0,2})"
    verse_end_part = r"((-|,\s?)(?P<end>[1-9][0-9]{0,2}))?"
    scripture_pattern = re.compile(book_part + r"\s" + chapter_part + ":" + verse_start_part + verse_end_part)
    found_chunk = scripture_pattern.search(content)
    return found_chunk

def parse_scripture(content: re.Match[str]):
    book = content.group("book")
    chapter = int(content.group("chapter"))
    verse_start = int(content.group("start"))
    verse_end = content.group("end")
    verse_end = int(verse_end) if (verse_end is not None) and (int(verse_end) > verse_start) else None
    return {'book': book, 'chapter': chapter, 'verse_start': verse_start, 'verse_end': verse_end}

def check_valid_scripture(scripture) -> bool:
    if scripture['book'] not in bible_books_info:
        return False 
    if (scripture['chapter']) > len(bible_books_info[scripture['book']]['verses-by-chapter']):
        return False
    verse_max = bible_books_info[scripture['book']]['verses-by-chapter'][scripture['chapter']-1]
    if scripture['verse_start'] > verse_max:
        return False
    return True

def create_scripture_link(scripture):
    book_number = str(bible_books_info[scripture['book']]['number']).rjust(2, '0')
    chapter_number = str(scripture['chapter']).rjust(3, '0')
    verse_start_number = str(scripture['verse_start']).rjust(3, '0')
    scripture_number = book_number + chapter_number + verse_start_number
    if scripture['verse_end'] is not None:
        verse_end_number = str(scripture['verse_end']).rjust(3, '0')
        scripture_number += '-' + book_number + chapter_number + verse_end_number
    return f'https://www.jw.org/finder?srcid=jwlshare&wtlocale=E&prefer=lang&bible={scripture_number}&pub=nwtsty'

if __name__ == "__main__":
    main_loop()
