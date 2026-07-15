"""Populate the database with realistic USIU-A demo data, including photos.

Run with:  ./venv/bin/python seed_mockdata.py
It regenerates the item/claim demo set each time (users are preserved/topped up).
"""
import os

from werkzeug.security import generate_password_hash

from usiulostnfound_database import init_db, get_connection, DB_PATH

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, 'static', 'uploads')
os.makedirs(UPLOADS, exist_ok=True)


# ---------------------------------------------------------------------------
# Demo item set — real item photos (sourced from Wikimedia Commons / Flickr)
# live in static/uploads. Each row:
#   (category, description, identifier, location, date, contact, status, image_path)
# ---------------------------------------------------------------------------
ITEMS = [
    ('Electronics', 'iPhone 13 Pro, alpine green', 'IMEI ends 4471, hairline scratch on camera bump',
     'SAC Building cafeteria, near counter', '2026-07-14', '0712-334-556', 'Checked-In',
     'uploads/real_iphone.jpg'),
    ('Electronics', 'Samsung Galaxy S23, lavender', 'Small barcode sticker on the back',
     'Library, 2nd floor study pods', '2026-07-13', '0720-118-990', 'Checked-In',
     'uploads/real_samsung.jpg'),
    ('Electronics', 'Lenovo 65W AC laptop adapter', 'Coiled black cable, worn spec label',
     'Lillian Beam Auditorium', '2026-07-12', 'kmwangi@usiu.ac.ke', 'Pending Security',
     'uploads/real_charger.jpg'),
    ('Documents', 'National ID card (photo ID)', 'Holder surname and photo visible on card',
     'Chandaria School of Business lobby', '2026-07-14', '0733-445-221', 'Checked-In',
     'uploads/real_studentid.jpg'),
    ('Documents', 'Passport, navy blue cover', 'Holder initials W.K.',
     'Freida Brown Student Center', '2026-07-11', '0700-900-100', 'Checked-In',
     'uploads/real_passport.jpg'),
    ('Keys', 'Ford car key fob with 2 house keys', 'Grey coin token on the key ring',
     'Parking Lot B, near gate', '2026-07-15', '0742-556-778', 'Pending Security',
     'uploads/real_keys.jpg'),
    ('Wallets', 'Tan leather bi-fold wallet', 'Hand-stitched edges, loyalty cards, no cash',
     'Mess Hall dining area', '2026-07-13', 'jdoe@usiu.ac.ke', 'Checked-In',
     'uploads/real_wallet.jpg'),
    ('Books', 'Stack of education textbooks', "'Intentional Tech' and 'Science Teaching Essentials'",
     'Library circulation desk', '2026-07-10', '0755-221-334', 'Checked-In',
     'uploads/real_textbook.jpg'),
    ('Other', 'Black stainless steel water bottle', 'Steel screw cap, small dent on the base',
     'Sports Complex, basketball court', '2026-07-12', '0711-002-003', 'Checked-In',
     'uploads/real_bottle.jpg'),
    ('Other', 'Eyeglasses with thin metal frame', 'In a red hard case',
     'Auditorium row F', '2026-07-09', '0799-887-665', 'Claimed',
     'uploads/real_glasses.jpg'),
]

# Mock student accounts (password shown for demo login)
STUDENTS = [
    ('100200', 'Jane Wanjiru', 'jwanjiru@usiu.ac.ke', 'pass123'),
    ('205311', 'Alex Otieno', 'aotieno@usiu.ac.ke', 'pass123'),
]


def seed():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    # Fresh demo set for items & claims (keep the users table intact)
    cur.execute("DELETE FROM claims")
    cur.execute("DELETE FROM items")

    # Top up mock students without clobbering existing accounts
    for user_id, name, email, pw in STUDENTS:
        exists = cur.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if not exists:
            cur.execute(
                "INSERT INTO users (user_id, name, email, password, role) VALUES (?,?,?,?,?)",
                (user_id, name, email, generate_password_hash(pw), 'student'),
            )

    id_by_desc = {}
    for cat, desc, ident, loc, date, contact, status, image_path in ITEMS:
        cur.execute(
            """INSERT INTO items (category, description, identifier, location, date, contact, image_path, status)
               VALUES (?,?,?,?,?,?,?,?)""",
            (cat, desc, ident, loc, date, contact, image_path, status),
        )
        id_by_desc[desc] = cur.lastrowid

    # A couple of demo claims: one still pending, one already approved (its item is 'Claimed')
    iphone_id = id_by_desc['iPhone 13 Pro, alpine green']
    glasses_id = id_by_desc['Eyeglasses with thin metal frame']

    cur.execute(
        """INSERT INTO claims (item_id, claimed_item, proof_identifier, contact, status)
           VALUES (?,?,?,?, 'Pending')""",
        (iphone_id, 'iPhone 13 Pro, alpine green',
         'It is the alpine green colour and the IMEI ends in 4471.',
         '0712-334-556'),
    )
    cur.execute(
        """INSERT INTO claims (item_id, claimed_item, proof_identifier, contact, status)
           VALUES (?,?,?,?, 'Approved')""",
        (glasses_id, 'Eyeglasses with thin metal frame',
         'They are in a red hard case with my initials on the lens cloth.',
         '0799-887-665'),
    )

    conn.commit()
    n_items = cur.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    n_claims = cur.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
    conn.close()
    print(f"Seeded {n_items} items and {n_claims} claims into {os.path.basename(DB_PATH)}.")


if __name__ == '__main__':
    seed()
