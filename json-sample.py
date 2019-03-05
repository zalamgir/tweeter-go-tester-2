import json
import psycopg2
import requests
import time

conn = psycopg2.connect(database="jsonb_test", user="maxroach", host="localhost", port=26257)
conn.set_session(autocommit=True)
cur = conn.cursor()

#url = "https://www.reddit.com/r/programming.json"
after = {"after": "null"}

for n in range(300):
    req = requests.get(url, params=after, headers={"User-Agent": "Python"})

    resp = req.json()
    after = {"after": str(resp['data']['after'])}

    data = json.dumps(resp)

    cur.execute("""INSERT INTO jsonb_test.programming (posts)
                SELECT json_array_elements(%s->'data'->'children')""", (data,))

    time.sleep(2)

cur.close()
conn.close()
