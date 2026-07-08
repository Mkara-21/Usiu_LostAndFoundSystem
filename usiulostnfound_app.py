# ==========================================
# PART 1: THE SETUP (At the very top)
import os
from flask import Flask, render_template, request, redirect, url_for

current_directory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(current_directory, 'static', 'templates'), 
            static_folder=os.path.join(current_directory, 'static'))

# Temporary list to store reports in memory until we connect a database later
lost_and_found_database = []
import os
from flask import Flask, render_template, request, redirect, url_for

current_directory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(current_directory, 'static', 'templates'), 
            static_folder=os.path.join(current_directory, 'static'))

# Temporary list to store reports in memory
lost_and_found_database = []

# 1. This displays your form when you visit /report
@app.route('/report', methods=['GET'])
def report_form():
    return render_template('Lostandfound.html')

# 2. This intercepts the submission no matter which route your browser is stuck on!
@app.route('/report', methods=['POST'])
@app.route('/submit-item', methods=['POST'])
def handle_submission():
    # Grab all the information from your form boxes safely
    item_description = request.form.get('description') or request.form.get('item_name') or request.form.get('itemDescription')
    unique_identifier = request.form.get('identifier') or request.form.get('uniqueIdentifier')
    location = request.form.get('location') or request.form.get('foundLocation')
    date_picked = request.form.get('date') or request.form.get('dateFound')

    new_report = {
        "description": item_description,
        "identifier": unique_identifier,
        "location": location,
        "date": date_picked
    }

    lost_and_found_database.append(new_report)
    print(f"\n🎉 SUCCESS! New Item Recorded: {new_report}\n")

    # Redirect right back to display the form fresh
    return redirect(url_for('report_form'))

if __name__ == '__main__':
    app.run(debug=True)

# PART 2: THE RECEIVING ROUTE (The middle section)
@app.route('/report', methods=['GET', 'POST'])
def report_form():
    if request.method == 'POST':
        # 1. Grab all the information from your form boxes
        item_description = request.form.get('description') or request.form.get('item_name') or request.form.get('itemDescription')
        unique_identifier = request.form.get('identifier') or request.form.get('uniqueIdentifier')
        location = request.form.get('location') or request.form.get('foundLocation')
        date_picked = request.form.get('date') or request.form.get('dateFound')

        # 2. Package it nicely into a dictionary
        new_report = {
            "description": item_description,
            "identifier": unique_identifier,
            "location": location,
            "date": date_picked
        }

        # 3. Save it to our list
        lost_and_found_database.append(new_report)
        print(f"\n🎉 New Item Reported successfully: {new_report}\n")

        # 4. Redirect right back to the form so it doesn't crash
        return redirect(url_for('report_form'))

    # If it's a GET request, just display the page normally
    return render_template('Lostandfound.html')


# PART 3: THE LAUNCHER (At the very bottom)
if __name__ == '__main__':
    app.run(debug=True)