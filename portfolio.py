from app import app
from app import app, db
from app.models import User, Skills

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Skills': Skills}

if __name__ == "__main__":
    app.run(debug=True)