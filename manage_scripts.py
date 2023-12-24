import json
import sqlite3

conn = sqlite3.connect('stock_analysis.db', check_same_thread=False)
cursor = conn.cursor()
f = open('instruments.json', 'r')
instruments = json.load(f)
f.close()

def get_scripts():
    cursor.execute(f'SELECT * FROM scripts')
    scripts = cursor.fetchall()
    return scripts

def add_script(script):
    if script not in instruments:
        return None
    scripts = get_scripts()
    script_names = [script[0] for script in scripts]
    if script not in script_names:
        cursor.execute('INSERT INTO scripts(name) VALUES (?)', (script,))
        conn.commit()
        with open('stock_names.txt', 'r') as file:
            names = file.read().splitlines()

        names.append(script)
        with open('stock_names.txt', 'w') as file:
            file.write('\n'.join(names))
        return True
    return False

def delete_script(script):
    cursor.execute(f'''DELETE FROM scripts WHERE name = ?''', (script, ))
    if cursor.rowcount > 0:
        conn.commit()
        with open('stock_names.txt', 'r') as file:
            names = file.read().splitlines()
            if script in names:
                names.remove(script)
            else:
                print(f"{script} not found in the file.")

            with open('stock_names.txt', 'w') as file:
                file.write('\n'.join(names))

        return True
    return False