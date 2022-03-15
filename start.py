from flask_script import Manager
from loot_generator import app
from loot_generator import db
from flask_migrate import Migrate, MigrateCommand
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('migrate', MigrateCommand)
db.create_all()

if __name__ == '__main__':
    manager.run(host='0.0.0.0')
    


