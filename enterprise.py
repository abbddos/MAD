import os
from app import app, db

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port)