import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

current_directory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(current_directory, 'static', 'templates'), 
            static_folder=os.path.join(current_directory, 'static'))

app.secret_key = 'usiu_lost_n_found_secure_key_2026'

# Configure a folder to save uploaded item images
UPLOAD_FOLDER = os.path.join(current_directory, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Temporary in-memory databases
lost_and_found_database = []
claims_database = []

@app.route('/report', methods=['GET'])
def report_form():
    # Grabs whoever is logged in. If no one is logged in, it will show the login/signup screen!
    current_role = session.get('role', None) 
    current_user_name = session.get('user_name', 'Guest')
    
    return render_template(
        'Lostandfound.html', 
        found_items=lost_and_found_database, 
        claims=claims_database,
        role=current_role,
        user_name=current_user_name
    )

@app.route('/submit-item', methods=['POST'])
def handle_item_submission():
    item_category = request.form.get('category')
    item_description = request.form.get('description')
    unique_identifier = request.form.get('identifier')
    location = request.form.get('location')
    date_picked = request.form.get('date')
    contact = request.form.get('finder_contact')
    
    file = request.files.get('item_photo')
    filename = None
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    new_report = {
        "category": item_category,
        "description": item_description,
        "identifier": unique_identifier,
        "location": location,
        "date": date_picked,
        "contact": contact,
        "image_path": f"uploads/{filename}" if filename else None
    }

    lost_and_found_database.append(new_report)
    print(f"\n🤝 FOUND ITEM LOGGED: {new_report}\n")
    return redirect(url_for('report_form'))

@app.route('/submit-claim', methods=['POST'])
def handle_claim_submission():
    claimed_item = request.form.get('claimed_item')
    proof_identifier = request.form.get('proof_identifier')
    contact = request.form.get('owner_contact')

    new_claim = {
        "claimed_item": claimed_item,
        "proof_identifier": proof_identifier,
        "contact": contact,
        "status": "Pending Verification"
    }

    claims_database.append(new_claim)
    print(f"\n🔍 NEW OWNER CLAIM SUBMITTED: {new_claim}\n")
    return redirect(url_for('report_form'))

@app.route('/logout')
def handle_logout():
    session.clear()  # This completely wipes out the active role!
    session['role'] = None  # Explicitly forces role to be hidden
    return redirect(url_for('report_form'))

# Temporary registered users database simulator
# Pre-populating one master security account for testing
registered_users = {
    "123456789": {
        "name": "Admin Officer",
        "email": "security@usiu.ac.ke",
        "password": "password123",
        "role": "security"
    }
}

# REWRITTEN ROUTE: Process Account Registration with Strict Digit Length Validation
@app.route('/signup', methods=['POST'])
def handle_signup():
    selected_role = request.form.get('role_selection')
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    user_id = request.form.get('user_id').strip()
    password = request.form.get('password')

    # Strict Validation: Check ID lengths based on USIU-A policy
    if selected_role == 'student' and len(user_id) != 6:
        # Returns a basic browser warning if rules are broken
        return "❌ Registration Failed: Student IDs must be exactly 6 digits.", 400
        
    if selected_role == 'security' and len(user_id) != 9:
        return "❌ Registration Failed: Security Officer Badge IDs must be exactly 9 digits.", 400

    # Check if user already exists
    if user_id in registered_users:
        return "❌ User already exists! Go back and log in.", 400

    # Save user into memory record storage
    registered_users[user_id] = {
        "name": full_name,
        "email": email,
        "password": password,
        "role": selected_role
    }
    
    print(f"\n🔐 DATABASE COMMITTED: New account registered for {full_name} ({user_id})")

    # Log them in dynamically
    session['role'] = selected_role
    session['user_id'] = user_id
    session['user_name'] = full_name

    return redirect(url_for('report_form'))


# REWRITTEN ROUTE: Strict Portal Login Verification
@app.route('/login', methods=['POST'])
def handle_login():
    selected_role = request.form.get('role_selection')
    user_id = request.form.get('user_id').strip()
    password = request.form.get('password')

    # Verify if user exists in our records
    if user_id in registered_users:
        account = registered_users[user_id]
        
        # Verify both password and chosen dashboard role match
        if account['password'] == password and account['role'] == selected_role:
            session['role'] = selected_role
            session['user_id'] = user_id
            session['user_name'] = account['name']
            print(f"\n✅ ACCESS GRANTED: {account['name']} logged into {selected_role} view.")
            return redirect(url_for('report_form'))

    # If verification fails at any stage
    print(f"\n🚨 ACCESS DENIED: Invalid login attempt for ID {user_id}")
    return "❌ Authentication Failed: Invalid Credentials or unauthorized role selected.", 401

if __name__ == '__main__':
    app.run(debug=True)