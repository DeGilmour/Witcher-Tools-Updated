
from loot_generator import db


class WeaponWitcher(db.Model):
    __tablename__ = "weapon_generator"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    weapon_range = db.Column(db.PickleType())
    weapon_Concealment = db.Column(db.PickleType(), db.ForeignKey('concealment.id'), nullable=False)
    weapon_type = db.Column(db.PickleType(), db.ForeignKey('type.id'), nullable=False)
    weapon_hand = db.Column('weapon_hand', db.PickleType())
    weapon_weight = db.Column('weapon_weight', db.PickleType())
    def __init__(self, name, weapon_range, weapon_Concealment, weapon_type, weapon_hand, weapon_weight):
        self.name = name
        self.weapon_range = weapon_range
        self.weapon_Concealment = weapon_Concealment
        self.weapon_type = weapon_type
        self.weapon_hand = weapon_hand
        self.weapon_weight = weapon_weight
      
    def __repr__(self):
        return "<Name %r>" % self.name

class ArmorWitcher(db.Model):
    __tablename__ = "armor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    armor_location = db.Column(db.Integer(), db.ForeignKey('armor_location.id'))
    ev = db.Column(db.PickleType(), nullable=False)
    weight = db.Column(db.PickleType(), nullable=False)
    reliability = db.Column(db.PickleType(), nullable=True)
    sp = db.Column(db.PickleType(), nullable=True)
    def __init__(self, name, armor_location, ev, weight, reliability, sp):
        self.name = name
        self.armor_location = armor_location
        self.ev = ev
        self.weight = weight
        self.reliability = reliability
        self.sp = sp
      
    def __repr__(self):
        return "<Name %r>" % self.name

class ArmorWitcherLocation(db.Model):
    __tablename__ = "armor_location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    def __init__(self, name):
        self.name = name
      
    def __repr__(self):
        return "<Name %r>" % self.name

class Concealment(db.Model):
    __tablename__ = "concealment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __repr__(self):
        return "<Name %r>" % self.name

class Effect(db.Model):
    __tablename__ = "effect"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __repr__(self):
        return "<Name %r>" % self.name

class Type(db.Model):
    __tablename__ = "type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<ID %r>" % self.id

class Availability(db.Model):
    __tablename__ = "rarity"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    weapon_cost = db.Column(db.PickleType())
    weapon_enhancement = db.Column(db.Integer)
    def __init__(self, name, weapon_cost, weapon_enhancement):
        self.name = name
        self.weapon_cost = weapon_cost
        self.weapon_enhancement = weapon_enhancement
    
    def __repr__(self):
        return "<Name %r> <Id %r>" % (self.name, self.id)

class AvailabilityArmor(db.Model):
    __tablename__ = "armor_rarity"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    armor_cost = db.Column(db.PickleType())
    armor_enhancement = db.Column(db.Integer)
    ev_negative = db.Column(db.PickleType())
    def __init__(self, name, armor_cost, armor_enhancement, ev_negative):
        self.name = name
        self.armor_cost = armor_cost
        self.armor_enhancement = armor_enhancement
        self.ev_negative = ev_negative
    
    def __repr__(self):
        return "<Name %r> <Id %r>" % (self.name, self.id)

class SavedWeapons(db.Model):
    __tablename__ = "saved_weapons_w"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    weapon_range = db.Column(db.PickleType())
    weapon_Concealment = db.Column(db.PickleType(),db.ForeignKey('concealment.id'), nullable=False)
    weapon_type = db.Column(db.Integer, db.ForeignKey('type.id'),  nullable=False)
    weapon_enhancement = db.Column(db.Integer)
    weapon_cost = db.Column(db.Integer)
    description = db.Column(db.String(300), nullable=False)
    damage = db.Column(db.String(300), nullable=False)
    availability = db.Column(db.Integer,db.ForeignKey('rarity.id'), nullable=False)
    hands = db.Column(db.Integer, nullable=False)
    effect = db.Column(db.Integer,db.ForeignKey('effect.id'), nullable=False)
    weight = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    reliability = db.Column(db.Integer)
    def __init__(self, name, weapon_range, weapon_Concealment, weapon_type, weapon_enhancement,weapon_cost,description, damage, availability, hands, effect, weight, accuracy, reliability  ):
        self.name = name
        self.weapon_range = weapon_range
        self.weapon_Concealment = weapon_Concealment
        self.weapon_type = weapon_type
        self.weapon_enhancement = weapon_enhancement
        self.weapon_cost = weapon_cost
        self.description = description
        self.damage = damage
        self.availability = availability
        self.hands = hands
        self.effect = effect
        self.weight = weight
        self.accuracy = accuracy
        self.reliability = reliability
      
    def __repr__(self):
        return "<Name %r>" % self.name

class SavedArmors(db.Model):
    __tablename__ = "saved_armors_rpg"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    enhancement = db.Column(db.Integer)
    type = db.Column(db.String(300), nullable=False)
    cost = db.Column(db.Integer)
    description = db.Column(db.String(300), nullable=True)
    availability = db.Column(db.Integer, db.ForeignKey('armor_rarity.id'), nullable=False)
    effect = db.Column(db.String(300), nullable=True)
    weight = db.Column(db.Integer)
    reliability = db.Column(db.Integer, nullable=False)
    stopping_power = db.Column(db.Integer, nullable=False)
    def __init__(self, name, enhancement, type, cost, description,availability,effect, weight, reliability, stopping_power):
        self.name = name
        self.enhancement = enhancement
        self.type = type
        self.cost = cost
        self.description = description
        self.availability = availability
        self.effect = effect
        self.weight = weight
        self.reliability = reliability
        self.stopping_power = stopping_power
      
    def __repr__(self):
        return "<Name %r>" % self.name

# def add_column(engine, table_name, column):
#     column_name = column.compile(dialect=engine.dialect)
#     column_type = column.type.compile(engine.dialect)
#     engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

# column = db.Column('weapon_hand', db.PickleType())
# add_column(db.engine, 'weapon_generator', column)