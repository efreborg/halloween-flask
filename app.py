import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# Use /tmp for the database file, as it's a writable directory in many cloud environments.
db_path = os.path.join(os.getenv("TMPDIR", "/tmp"), "fairies.db")
db_uri = f"sqlite:///{db_path}"

fairy_names = [
    'Adan', 'Aine', 'Aoibheann', 'Blodeuwedd', 'Bran', 'Caelan', 'Cliodhna', 'Eira', 'Elara',
    'Faolan', 'Fia', 'Fionnuala', 'Gwydion', 'Lir', 'Midir', 'Morwenna', 'Niamh', 'Oisin', 'Orla',
    'Rhiannon', 'Ronan', 'Saoirse', 'Siofra', 'Tadhg', 'Torin']

app = Flask(__name__, template_folder='templates', static_folder='static')
# It's important to set a secret key for session management.
# You should replace 'your-secret-key' with a real, securely generated secret key.
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FairyMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(50), unique=True, nullable=False)
    message = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<FairyMessage {self.page_name}>'

# It's better to create tables once at startup or via a separate command.
# Using app.app_context() ensures this runs when the app is initialized.
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('unified_form.html')

@app.route("/fairy/<string:page_name>")
def fairy_page(page_name):
    """Render a page for a given fairy, showing their message."""
    # We can add a list of valid fairies to prevent users from accessing non-existent pages.
    if page_name not in fairy_names:
        return "Fairy not found!", 404

    message_entry = FairyMessage.query.filter_by(page_name=page_name).first()
    message = message_entry.message if message_entry else ""
    return render_template(f'{page_name}.html', message=message)

@app.route("/update-fairy", methods=["GET", "POST"])
def update_fairy():
    # Protect this route
    if request.method == "POST":
        page = request.form.get("page")
        message = request.form.get("message")

        if page not in fairy_names:
            return "Invalid page selected", 400

        message_entry = FairyMessage.query.filter_by(page_name=page).first()

        if message_entry:
            message_entry.message = message
        else:
            message_entry = FairyMessage(page_name=page, message=message)
            db.session.add(message_entry)

        db.session.commit()

        return redirect(url_for('fairy_page', page_name=page))

    return render_template('unified_form.html')

def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    main()