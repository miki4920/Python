import pandas as pd
import sqlite3

timestamps = ["2018-10"]

for timestamp in timestamps:
    connection = sqlite3.connect(f"{timestamp}.db")
    c = connection.cursor()
    limit = 5000
    last_unix = 0
    cur_length = limit
    counter = 0
    test_done = False
    while cur_length == limit:
        df = pd.read_sql(
            f" WHERE unix > {last_unix} and parent NOT NULL and score > 0 ORDER BY unix ASC LIMIT {limit}",
            connection)
        last_unix = df.tail(1)['unix'].values[0]
        cur_length = len(df)
        if not test_done:
            with open('test.from', 'a', encoding='utf8') as f:
                for content in df['parent'].values:
                    f.write(content + '\n')

            with open('test.to', 'a', encoding='utf8') as f:
                for content in df['comment'].values:
                    f.write(str(content) + '\n')

            test_done = True

        else:
            with open('train.from', 'a', encoding='utf8') as f:
                for content in df['parent'].values:
                    f.write(content + '\n')

            with open('train.to', 'a', encoding='utf8') as f:
                for content in df['comment'].values:
                    f.write(str(content) + '\n')

        counter += 1
        if counter % 20 == 0:
            print(counter * limit, 'rows completed so far')