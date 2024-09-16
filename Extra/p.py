

def save_text(text, path):
    try:
        f = open(path, "a")
        f.write(text)
        f.write("\n\n\n")
    except IOError as e:
        print(f"ERROT IN save_text() : {e}")


text = 'Azmattullah'
save_text(text, r"Extra\text.txt")
