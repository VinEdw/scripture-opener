# scripture-opener

The main python script of this project is `open_scriptures_from_clipboard.py`. 
When run, the program will peridocially check the contents of the clipboard. When the contents of the clipboard update, the program will check for what looks like a Bible verse (scripture) reference. If it finds one, it will use `bible-books.json` to confirm that it is a valid scripture. 
If so, it will then create a link to the verse on [jw.org](https://www.jw.org/en/library/bible/study-bible/books/). The link opened automatically, redirecting to the [JW Library app](https://www.jw.org/en/online-help/jw-library/) and turning to the scripture there.
This is helpful when typing notes, as the scripture reference only needs to be written and copied by the user, and the computer will take care of opening it.
