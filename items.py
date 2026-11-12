import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def add_item(title, difficulty_level, rating, user_id, classes):
    # FLAW 2: INJECTION
    sql = f"""INSERT INTO items (title, difficulty_level, rating, user_id)
          VALUES ('{title}', '{difficulty_level}', '{rating}', '{user_id}')"""
    db.execute(sql)

    item_id = db.last_insert_id()

    for class_title, class_value in classes:
        sql = f"""INSERT INTO item_classes (item_id, title, value)
                VALUES ('{item_id}', '{class_title}', '{class_value}')"""
        db.execute(sql)
# FIXING FLAW 2: INJECTION
#    sql = """INSERT INTO items (title, difficulty_level, rating, user_id)
#             VALUES (?, ?, ?, ?)"""
#    db.execute(sql, [title, difficulty_level, rating, user_id])

#    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
#    for class_title, class_value in classes:
#        db.execute(sql, [item_id, class_title, class_value])

def add_comment(item_id, user_id, comment_text):
    # FLAW 2: INJECTION
    sql = f"""INSERT INTO comments (item_id, user_id, comment_text)
             VALUES ('{item_id}', '{user_id}', '{comment_text}')"""
    db.execute(sql)
# FIXING FLAW 2: INJECTION
#    sql = """INSERT INTO comments (item_id, user_id, comment_text)
#             VALUES (?, ?, ?)"""
#    db.execute(sql, [item_id, user_id, comment_text])

def get_comments(item_id):
    # FLAW 2: INJECTION
    sql = f"""SELECT comments.comment_text, users.id user_id, users.username
             FROM comments, users
             WHERE comments.item_id = {item_id} AND comments.user_id = users.id
             ORDER BY comments.id DESC"""
    return db.query(sql)
# FIXING FLAW 2: INJECTION
#    sql = """SELECT comments.comment_text, users.id user_id, users.username
#             FROM comments, users
#             WHERE comments.item_id = ? AND comments.user_id = users.id
#             ORDER BY comments.id DESC"""
#    return db.query(sql, [item_id])

def get_classes(item_id):
    # FLAW 2: INJECTION
    sql = f"SELECT title, value FROM item_classes WHERE item_id = {item_id}"
    return db.query(sql)
# FIXING FLAW 2: INJECTION
#    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
#    return db.query(sql, [item_id])

def item_count():
    sql = "SELECT COUNT(*) FROM items"
    res = db.query(sql)
    return res[0][0] if res else 0

def get_items(page, page_size):
    # FLAW 2: INJECTION
    limit = page_size
    offset = page_size * (page - 1)
    sql = f"""SELECT items.id, items.title, users.id user_id, users.username
             FROM items, users
             WHERE items.user_id = users.id
             ORDER BY items.id DESC
             LIMIT {page_size} OFFSET {offset}"""
    return db.query(sql)
# FIXING FLAW 2: INJECTION
#    sql = """SELECT items.id, items.title, users.id user_id, users.username
#             FROM items, users
#             WHERE items.user_id = users.id
#             ORDER BY items.id DESC
#             LIMIT ? OFFSET ?"""
#    limit = page_size
#    offset = page_size * (page - 1)
#    return db.query(sql, [limit, offset])

def get_item(item_id):
    # FLAW 2: INJECTION
    sql = f"""SELECT items.id,
                    items.title,
                    items.min_players,
                    items.max_players,
                    items.age_recommendation,
                    items.difficulty_level,
                    items.duration,
                    items.rating,
                    users.id user_id,
                    users.username
             FROM items, users
             WHERE items.user_id = users.id AND
                   items.id = {item_id}"""
    result = db.query(sql)
    return result[0] if result else None
# FIXING FLAW 2: INJECTION
#    sql = """SELECT items.id,
#                    items.title,
#                    items.min_players,
#                    items.max_players,
#                    items.age_recommendation,
#                    items.difficulty_level,
#                    items.duration,
#                    items.rating,
#                    users.id user_id,
#                    users.username
#             FROM items, users
#             WHERE items.user_id = users.id AND
#                    items.id = ?"""
#    result = db.query(sql, [item_id])
#    return result[0] if result else None

def update_item(item_id, title, difficulty_level, rating, classes):
    # FLAW 2: INJECTION
    sql = f"""UPDATE items SET title = '{title}',
                              difficulty_level = '{difficulty_level}',
                              rating = '{rating}'
                          WHERE id = {item_id}"""
    db.execute(sql)

    sql = f"DELETE FROM item_classes WHERE item_id = {item_id}"
    db.execute(sql)

    for class_title, class_value in classes:
        sql = f"""INSERT INTO item_classes (item_id, title, value)
                  VALUES ('{item_id}', '{class_title}', '{class_value}')"""
        db.execute(sql)
# FIXING FLAW 2: INJECTION
#    sql = """UPDATE items SET title = ?,
#                              difficulty_level = ?,
#                              rating = ?
#                          WHERE id = ?"""
#    db.execute(sql, [title, difficulty_level, rating, item_id])

#    sql = "DELETE FROM item_classes WHERE item_id = ?"
#    db.execute(sql, [item_id])

#    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
#    for class_title, class_value in classes:
#        db.execute(sql, [item_id, class_title, class_value])

def remove_item(item_id):
    # FLAW 2: INJECTION
    sql = f"DELETE FROM comments WHERE item_id = {item_id}"
    db.execute(sql)
    sql = f"DELETE FROM item_classes WHERE item_id = {item_id}"
    db.execute(sql)
    sql = f"DELETE FROM items WHERE id = {item_id}"
    db.execute(sql)
# FIXING FLAW 2: INJECTION
#    sql = "DELETE FROM comments WHERE item_id = ?"
#    db.execute(sql, [item_id])
#    sql = "DELETE FROM item_classes WHERE item_id = ?"
#    db.execute(sql, [item_id])
#    sql = "DELETE FROM items WHERE id = ?"
#    db.execute(sql, [item_id])

def find_items(query):
    # FLAW 2: INJECTION
    like = "%" + query + "%"
    sql = f"""SELECT id, title
             FROM items
             WHERE title LIKE '{like}'
             ORDER BY title DESC"""
    return db.query(sql)
# FIXING FLAW 2: INJECTION
#    sql = """SELECT id, title
#             FROM items
#             WHERE title LIKE ?
#             ORDER BY title DESC"""
#    like = "%" + query + "%"
#    return db.query(sql, [like])
