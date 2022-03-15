from os import name
from sqlalchemy.orm import base
from loot_generator import app, db
from flask import render_template, redirect, url_for, flash, request, get_template_attribute, Markup, send_from_directory
from loot_generator.model.loot_generator_model import WeaponWitcher, Concealment, Effect, Type, Availability, SavedWeapons, ArmorWitcher, AvailabilityArmor, ArmorWitcherLocation, SavedArmors
import random
import json
from sqlalchemy.sql import func


@app.route('/home', methods=['GET', 'POST'])
def generate_weapon(list_weapon_random=None, weapons=None, weapon_id=None, availability_id=None):
    title = 'Weapons Generator'
    weapons = WeaponWitcher.query.all()
    weapons_list = []
    rarities_list = []
    rarities = Availability.query.all()
    weapons_list = toDict(instances=weapons)
    rarities_list =  toDict(instances=rarities)
    result = {"weapon": weapons_list, "rarity": rarities_list}
    return render_template('generate_weapon.html', 
        title=title,
        result=result,
        list_weapon_random=list_weapon_random,
        weapon_id=weapon_id,
        availability_id=availability_id)

# def updateWeaponWitcher():
#     weapon_ = WeaponWitcher.query.filter_by(id=12).first()
#     weapon_.weapon_hand = [1]
#     weapon_.weapon_weight = [0.3, 0.5]
#     db.session.add(weapon_)
#     db.session.commit()

def toDict(instances):
    instance_list = []
    for instance in instances:
        instance_list.append({col.name: getattr(instance, col.name) for col in instance.__table__.columns})
    return instance_list

def getType(type_id=None):
    r_type = random.randint(3,6)
    weapon = Type.query.all()
    lista_weapon = []
    for i in weapon:
        dict_weapon = {"id": i.id, 'name': i.name}
        lista_weapon.append(dict_weapon)
    if not type_id:
        type_ = Type.query.filter_by(id=r_type).first()
    else:
        type_ = Type.query.filter_by(id=type_id).first()
    return [type_.name, type_.id]

def getWeapon():
    weapons = WeaponWitcher.query.all()
    weapons = toDict(weapons)
    weapons_id = [i['id'] for i in weapons]
    r_weapon = random.randint(1, len(weapons_id) - 1)
    weapon_ = WeaponWitcher.query.filter_by(id=weapons_id[r_weapon]).first()
    return weapon_

def getEffect(effect_id=None):
    effect = Effect.query.all()
    r_effect = random.randint(1,len(effect))
    if not effect_id:
        effect_ = Effect.query.filter_by(id=r_effect).first()
    else:
        effect_ = Effect.query.filter_by(id=effect_id).first()
    return effect_

def getConcealment(concealment_id=None):
    concealment = Concealment.query.all()
    _concealment = random.randint(1,len(concealment))
    if not concealment_id:
        concealment_ = Concealment.query.filter_by(id=_concealment).first()
    else:
        concealment_ = Concealment.query.filter_by(id=concealment_id).first()
    return concealment_.name

def getAvailability():
    rarity = Availability.query.all()
    _rarity = random.randint(1,len(rarity))
    rarity_ = Availability.query.filter_by(id=_rarity).first()
    return rarity_

def getArmorEffect():
    r_effect = random.randint(0,1)
    dict_effect = {
        0: "Full Cover",
        1: "Restricted Vision"
    }
    return dict_effect[r_effect]

@app.route('/home/calculeteRandom', methods=['GET', 'POST'])
def calculeteRandom():
    list_weapon_random = []
    hands = ["One Handed", "Two handed"]
    dict_weapon_random = {}
    r_type = getType()
    r_acc = random.randint(0,3)
    r_dmg_dice = random.randint(2,6)
    r_dmg_dice_mod = random.randint(0,3)
    r_rel = random.randint(0,20)
    r_hands =  random.randint(0,1)
    # r_weight =  random.randint(0,20)
    availability_instance = getAvailability()
    r_cost = random.randint(availability_instance.weapon_cost[0],availability_instance.weapon_cost[1] )
    r_en = random.randint(0, availability_instance.weapon_enhancement)
    dict_weapon_random['type']  = r_type[0]
    dict_weapon_random['type_id']  = r_type[1]
    dict_weapon_random['accuracy']  = r_acc
    dict_weapon_random['damage']  = "%sd+%s" % (r_dmg_dice, r_dmg_dice_mod)
    dict_weapon_random['reliability']  = r_rel
    dict_weapon_random['hands'] = hands[r_hands]
    weapon_instance = getWeapon()
    if not weapon_instance:
        raise Exception(weapon_instance)
        return generate_weapon(list_weapon_random=list_weapon_random)
    if isinstance(weapon_instance.weapon_range, list):
        r_range = random.randint(0, len(weapon_instance.weapon_range) - 1)
        dict_weapon_random['range'] = weapon_instance.weapon_range[r_range]
    else:
       dict_weapon_random['range'] = weapon_instance.weapon_range
    dict_weapon_random['effect'] = getEffect().name
    dict_weapon_random['weight'] = random.randint(0, len(weapon_instance.weapon_weight) - 1)
    dict_weapon_random['cost'] = r_cost
    dict_weapon_random['name'] = weapon_instance.name
    dict_weapon_random['enhancements'] = r_en
    dict_weapon_random['concealment'] = getConcealment()
    dict_weapon_random['availability']  = availability_instance.name
    list_weapon_random.append(dict_weapon_random)
    return generate_weapon(list_weapon_random=list_weapon_random)


@app.route('/home/calculeteWeapon', methods=['GET', 'POST'])
def calculeteWeapon():
    weapon = request.form.get('weapon', 1)
    rarity = request.form.get('rarity', 1)
    weapon_instance = WeaponWitcher.query.filter_by(id=weapon).first()
    availability_instance = Availability.query.filter_by(id=rarity).first()
    hands = ["One Handed", "Two handed"]
    dict_weapon_random = {}
    r_acc = random.randint(0,3)
    r_dmg_dice = random.randint(2,6)
    r_dmg_dice_mod = random.randint(0,3)
    r_rel = random.randint(5,20)
    r_hands =  random.randint(0,1)
    r_weight =  random.randint(0, len(weapon_instance.weapon_weight) - 1)
    r_cost = random.randint(availability_instance.weapon_cost[0],availability_instance.weapon_cost[1] )
    r_en = random.randint(0,availability_instance.weapon_enhancement)
    dict_weapon_random['accuracy']  = r_acc
    if availability_instance.id in (4, 5) and r_dmg_dice < 6:
        r_dmg_dice = random.randint(5,7)
    dict_weapon_random['damage']  = "%sd+%s" % (r_dmg_dice, r_dmg_dice_mod)
    dict_weapon_random['reliability']  = r_rel
    # dict_weapon_random['hands'] = hands[r_hands]
    if len(weapon_instance.weapon_hand) == 1:
        r_hands = 0
    dict_weapon_random['hands'] = weapon_instance.weapon_hand[r_hands]
    if isinstance(weapon_instance.weapon_range, list):
        r_range = random.randint(0, len(weapon_instance.weapon_range) - 1)
        dict_weapon_random['range'] = weapon_instance.weapon_range[r_range]
    else:
       dict_weapon_random['range'] = weapon_instance.weapon_range
    if isinstance(weapon_instance.weapon_Concealment, list):
        r_con = random.randint(0, len(weapon_instance.weapon_Concealment) - 1)
        r_con = weapon_instance.weapon_Concealment[r_con]
        dict_weapon_random['concealment'] = getConcealment(concealment_id=r_con)
    if isinstance(weapon_instance.weapon_type, list):
        r_type = random.randint(0, len(weapon_instance.weapon_type) - 1)
        r_type = weapon_instance.weapon_type[r_type]
        dict_weapon_random['type']  = getType(type_id=r_type)[0]
        dict_weapon_random['type_id']  = getType(type_id=r_type)[1]
    dict_weapon_random['effect'] = getEffect().name
    # dict_weapon_random['weight'] = r_weight
    dict_weapon_random['weight'] = weapon_instance.weapon_weight[r_weight]
    dict_weapon_random['cost'] = r_cost
    dict_weapon_random['name'] = weapon_instance.name
    dict_weapon_random['enhancements'] = r_en
    dict_weapon_random['availability']  = availability_instance.name
    dict_weapon_random['effect_id']  =  getEffect().id
    list_weapon_random = []
    list_weapon_random.append(dict_weapon_random)
    return generate_weapon(
        list_weapon_random=list_weapon_random, 
        weapon_id=weapon_instance.id, availability_id=availability_instance.id)

@app.route('/home/save_weapon', methods=['GET', 'POST'])
def saveWeapon():
    effect_id = request.form.get('effect_id')
    effect = getEffect(effect_id=effect_id)
    try:
        saved = SavedWeapons(
            name=request.form.get('name'),
            weapon_range=request.form.get('weapon_range'),
            weapon_Concealment=request.form.get('weapon_Concealment'),
            weapon_type=int(request.form.get('weapon_type')),
            weapon_cost=request.form.get('weapon_cost'),
            weapon_enhancement=request.form.get('weapon_enhancement'),
            damage=request.form.get('damage'),
            availability=request.form.get('availability'),
            hands=request.form.get('hands'),
            effect=request.form.get('effect'),
            weight=request.form.get('weight'),
            accuracy=request.form.get('accuracy'),
            reliability=request.form.get('reliability'),
            description=effect.description)
        db.session.add(saved)
        db.session.commit()
    except Exception as e:
        return error_message(e)
    return redirect(url_for('savedWeapons'))

@app.route('/home/saved_weapons', methods=['GET', 'POST'])
def savedWeapons(searched=False):
    types = Type.query.all()
    if not searched:
        saved = SavedWeapons.query.join(
            Type, SavedWeapons.weapon_type==Type.id).with_entities(Type.name.label('type_name'), 
            SavedWeapons.name,
            SavedWeapons.accuracy,
            SavedWeapons.availability,
            SavedWeapons.weapon_type,
            SavedWeapons.id,
            SavedWeapons.damage,
            SavedWeapons.effect,
            SavedWeapons.weapon_Concealment,
            SavedWeapons.weapon_cost,
            SavedWeapons.weight,
            SavedWeapons.weapon_range,
            SavedWeapons.weapon_enhancement,
            SavedWeapons.reliability,
            SavedWeapons.weapon_Concealment,
            SavedWeapons.description).all()
    else:
        saved = searched

    title = 'Saved Weapons'
    weapons = True
    return render_template(
        'saved.html', 
        saved=saved, 
        title=title,
        types=types,
        weapons=True)


@app.route('/home/deleteWeapon', methods=['GET', 'POST'])
def deleteWeapon():
    weapon_id = int(request.form.get('id'))
    weapon_obj = SavedWeapons.query.filter_by(id=weapon_id).first()
    db.session.delete(weapon_obj)
    db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

def insertWeapon():
    saved = AvailabilityArmor(
        name='Relic', armor_cost=[1500, 2500], armor_enhancement=3, ev_negative=[1, 3])
    db.session.add(saved)
    db.session.commit()

@app.route('/home/armor/generate', methods=['GET', 'POST'])
def GenerateArmor(
        list_return=None, armor_Location_id=None, rarity_armor_id=None,
        armor_name=None ):
    armors_list = [
        {"id": 0, "name": 'Light Armor'} , 
        {"id": 1, "name": 'Medium Armor'}, 
        {"id": 2, "name":'Heavy Armor'}
    ]
    if rarity_armor_id:
        rarity_armor_id = int(rarity_armor_id)
    if armor_Location_id:
        armor_Location_id = int(armor_Location_id)
    rarity_armor = AvailabilityArmor.query.all()
    rarity_armor = toDict(instances=rarity_armor)
    armor_Location = ArmorWitcherLocation.query.all()
    armor_location = toDict(instances=armor_Location)
    result = {}
    result = {"armors": armors_list, "armor_location": armor_location, "rarity_armor": rarity_armor }
    title = 'Generate Armor'
    return render_template(
        'generate_armor.html', 
        result=result, 
        list_return=list_return,
        armor_Location_id=armor_Location_id,
        rarity_armor_id=rarity_armor_id,
        armor_name=armor_name,
        title=title
        )

@app.route('/home/armor/calculate', methods=['GET', 'POST'])
def calculeteArmor():
    list_return = []
    random_generation = request.form.get('random', None)
    if not random_generation:
        try:
            armor_location_req = int(request.form.get('armor_location', None))
            rarity_req = int(request.form.get('rarity_req', None))
            armor_name = request.form.get('armor', None)
            armor_instance = None
            if armor_name and armor_location_req:
                armor_instance = ArmorWitcher.query.filter_by(name=armor_name, armor_location=armor_location_req).first()
                availability_instance = AvailabilityArmor.query.filter_by(id=rarity_req).first()
        except Exception as e:
            return error_message(error_message=e)
    else:
        armors_list = [
            {"id": 0, "name": 'Light Armor'} , 
            {"id": 1, "name": 'Medium Armor'}, 
            {"id": 2, "name":'Heavy Armor'}
        ]
        armor_name = armors_list[random.randint(0, 2)]
        armor_name = armor_name['name']
        rarity_req = None
        armor_location_req = None
        rand = random.randint(1, 4)
        if armor_name and rand:
            armor_instance = ArmorWitcher.query.filter_by(name=armor_name, armor_location=rand).first()
            availability_instance = AvailabilityArmor.query.filter_by(id=rand).first()
            armor_name = None
    dict_armor = {}
    if len(availability_instance.armor_cost) > 1:
        r_cost = random.randint(availability_instance.armor_cost[0], availability_instance.armor_cost[1])
        dict_armor['cost'] = r_cost
    
    if len(availability_instance.ev_negative) > 1:
        r_bonus = random.randint(availability_instance.ev_negative[0], availability_instance.ev_negative[1])
        dict_armor['bonus'] = r_bonus
    else:
        r_bonus = random.randint(0, availability_instance.ev_negative[0])
        dict_armor['bonus'] = r_bonus

    r_ench = random.randint(0, availability_instance.armor_enhancement)
    dict_armor['ench'] = r_ench
    if isinstance(armor_instance.sp, list):
        r_sp = random.randint(0, len(armor_instance.sp) - 1)
        dict_armor['sp'] = armor_instance.sp[r_sp]
    else:
       dict_armor['sp'] = armor_instance.sp

    if isinstance(armor_instance.reliability, list):
        r_reliability= random.randint(0, len(armor_instance.reliability) - 1)
        dict_armor['reliability'] = armor_instance.reliability[r_reliability]
    else:
       dict_armor['reliability'] = armor_instance.reliability
    
    if isinstance(armor_instance.weight, list):
        r_weight = random.randint(0, len(armor_instance.weight) - 1)
        dict_armor['weight'] = armor_instance.weight[r_weight]
    else:
       dict_armor['weight'] = armor_instance.weight

    if isinstance(armor_instance.ev, list):
        r_ev = random.randint(0, len(armor_instance.ev) - 1)
        dict_armor['ev'] = armor_instance.weight[r_ev]
    else:
       dict_armor['weight'] = armor_instance.weight
    dict_armor['ev'] = dict_armor.get('ev', '0')
    dict_armor['name'] = armor_instance.name
    dict_armor['rarity'] = availability_instance.name
    if dict_armor['name'] in ['Medium Armor', 'Heavy Armor']:
        dict_armor['effect'] = getArmorEffect()
    
    list_return.append(dict_armor)
    return GenerateArmor(
        list_return=list_return, 
        rarity_armor_id=rarity_req,
        armor_Location_id=armor_location_req,
        armor_name=armor_name)

@app.route('/home/armor/saved_armor', methods=['GET', 'POST'])
def savedArmors(searched=False):
    if not searched:
        saved = SavedArmors.query.all()
    else:
        saved = searched
    title = 'Saved Armors'
    weapons =  False
    return render_template('saved.html', saved=saved, title=title, weapons=weapons)

@app.route('/home/armor/save_armor', methods=['GET', 'POST'])
def saveArmor():
    try:
        saved = SavedArmors(
            name=request.form.get('name'),
            enhancement=request.form.get('enhancement'),
            type=request.form.get('type'),
            cost=request.form.get('cost'),
            description=request.form.get('description'),
            availability=request.form.get('availability'),
            effect=request.form.get('effect'),
            weight=request.form.get('weight'),
            reliability=request.form.get('reliability'),
            stopping_power=request.form.get('stopping_power'))
        db.session.add(saved)
        db.session.commit()
    except Exception as e:
        return error_message(e)
    return redirect(url_for('savedArmors'))
   
@app.route('/home/armor/delete_armor', methods=['GET', 'POST'])
def deleteArmor():
    _id = int(request.form.get('id'))
    try:
        _obj = SavedArmors.query.filter_by(id=_id).first()
        db.session.delete(_obj)
        db.session.commit()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except:
        return json.dumps({'success':False}), 200, {'ContentType':'application/json'} 

def insertWeapon():
    saved = AvailabilityArmor(
        name='Relic', armor_cost=[1500, 2500], armor_enhancement=3, ev_negative=[1, 3])
    db.session.add(saved)
    db.session.commit()

@app.route('/error', methods=['POST'])
def error_message(error_message, request=True):
    #Gettin the erro_message template
    macro_error = get_template_attribute("macro_table_ini.html", "error_message")
    #Passing the erro message
    re = macro_error(message=error_message)
    # To html
    re = Markup(re)
    if error_message:
        return json.dumps({'success':False, 'response': re}), 200, {'ContentType':'application/json'} 

@app.route('/search_weapon', methods=['POST'])
def onSearchWeapon():
    weapon_name = request.form.get('weapon_name', None)
    cost = int(request.form.get('cost', None)) if request.form.get('cost', None) and request.form.get('cost', None) != 0 else None
    type = int(request.form.get('type', None)) if request.form.get('type', None) and request.form.get('type', None) != 0 else None
    base_query = SavedWeapons.query.join(
            Type, SavedWeapons.weapon_type==Type.id).with_entities(Type.name.label('type_name'), 
            SavedWeapons.accuracy,
            SavedWeapons.availability,
            SavedWeapons.weapon_type,
            SavedWeapons.id,
            SavedWeapons.damage,
            SavedWeapons.effect,
            SavedWeapons.weapon_Concealment,
            SavedWeapons.weapon_cost,
            SavedWeapons.weight,
            SavedWeapons.weapon_range,
            SavedWeapons.weapon_enhancement,
            SavedWeapons.reliability,
            SavedWeapons.weapon_Concealment,
            SavedWeapons.description,
            SavedWeapons.name)
    if weapon_name or type or cost :
        if weapon_name:
            base_query = base_query.filter(
                    SavedWeapons.name.ilike(r"%{}%".format(weapon_name))).all()

        if type:
            base_query = base_query.filter(SavedWeapons.weapon_type==type).all()

        if cost and cost == 1:
            base_query = base_query.order_by(SavedWeapons.weapon_cost.desc()).all()
        elif cost and cost == 2:
            base_query = base_query.order_by(SavedWeapons.weapon_cost.asc()).all()
    else:
        base_query = False

    return savedWeapons(searched=base_query)

@app.route('/search_armor', methods=['POST'])
def onSearchArmor():
    armor_name = request.form.get('armor_name', None)
    try:
        base_query = SavedArmors.query
        if armor_name:
            if armor_name:
                base_query = base_query.filter(SavedArmors.name.ilike(r"%{}%".format(armor_name))).all()
        else:
            base_query =  False
    except Exception as e:
        return error_message(e)
    return savedArmors(searched=base_query)

@app.route('/dice_roller', methods=['POST'])
def diceRoller():
    dices = request.form.get('dices', None)
    list_return = []
    dices = json.loads(dices)
    for dice in dices:
        dice_type = dice['dice']
        dice_to_roll = dice['dice'].replace('d', '')
        number_to_roll = dice['number'].strip()
        number_to_roll = dice['number'].replace('(', '').replace(')', '')
        list_of_dice = []
        for i in range(0, int(number_to_roll)):
            dice_return = random.randint(1, int(dice_to_roll))
            list_of_dice.append(dice_return)
        list_string =  map(str, list_of_dice)
        list_string = '+'.join(list_string)
        dict_result = {"dice_type": dice_type, "sum": sum(list_of_dice), "dices": list_string}
        list_return.append(dict_result)
    def getDiceMessage():
        message = ''
        for dice_type in list_return:
            if dice_type['sum'] > 0:
                message += dice_type['dice_type'] + ': ' + "You rolled the total of " + str(dice_type['sum']) + "(" + str(dice_type['dices']) + ")</br>"
        return message
    return {'message': getDiceMessage()}

    