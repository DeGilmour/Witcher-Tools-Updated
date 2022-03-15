from loot_generator import app
from loot_generator import Flask
from flask import render_template, redirect, url_for, flash, request, get_template_attribute, Markup
import random
import json
from operator import itemgetter
from loot_generator import loot_generator_controller

error_message = loot_generator_controller.error_message

@app.route('/home/tools/combat', methods=['GET', 'POST'])
def combatHome():
    title = "Combat Simulator"
    combatSimulator = get_template_attribute("macro_table_ini.html", "combat")
    return render_template('tools.html', title=title, combatSimulator=combatSimulator) 

@app.route('/home/tools/combat/getDamageLocation', methods=['GET', 'POST'])
def getDamageLocation():
    request_itens = request.form
    try:
        monster_location = (int(request_itens.get('monster_location')) if request_itens.get('monster_location', None) else None)
        human_location = (int(request_itens.get('human_location')) if request_itens.get('human_location', None) else None)
    except Exception as e:
        return error_message(e)

    try:
        if human_location:
            human_location = int(human_location)
        aiming =  request_itens.get('aiming')
        enemy_type = request_itens.get('enemy_type')
        attribute = request_itens.get('attribute', None)
        attribute = int(attribute)
        skill = request_itens.get('skill', None)
        skill = int(skill)
        damage = request_itens.get('damage', None)
        damage = dealWithDamage(damage=damage)
        result_location = None
        if aiming == 'yes':
            if enemy_type == 'humanoid' and human_location != 0:
                result_location = getDictRoll(human=True, value=human_location)
                result = decideRoll(attribute=attribute, skill=skill, location=result_location, damage=damage,  penalty=True)
            elif enemy_type == 'monster' and monster_location != 0:
                result_location = getDictRoll(monster=True, value=monster_location)
                result = decideRoll(attribute=attribute, skill=skill, location=result_location, damage=damage,  penalty=True)
        else:
            if enemy_type == 'humanoid' and human_location == 0:
                dict_location_humanoid_random = getDictRandom(human=True)
                result = decideRoll(attribute=attribute, skill=skill, location=dict_location_humanoid_random, damage=damage)
            elif enemy_type == 'monster' and monster_location == 0:
                dict_location_monster_random = getDictRandom(monster=True)
                result = decideRoll(attribute=attribute, skill=skill, location=dict_location_monster_random, damage=damage)
        return result
    except Exception as e:
        return error_message(e)


def decideRoll(attribute, skill, location, damage, penalty=None):
    d10 = random.randint(1,10)
    d10_list = []
    critical = None
    try:
        if penalty:
            result = (attribute + skill + d10) - location[0]
        else:
            result = (attribute + skill + d10)
        if_it_hits = damage['result'][0] * location[1]
        d10_list.append(d10)
        while d10 == 10:
            d10 = random.randint(1,10)
            d10_list.append(d10)
        if len(d10_list) > 1:
            d10_list_string =  map(str, d10_list)
            d10_list_string = '+'.join(d10_list_string)
            critical = "Congrats you rolled a total of {} criticals!!!, your complete roll is now: {}({})".format(
                len(d10_list) - 1, sum(d10_list) + (result - 10), d10_list_string + '+' + str(result - 10))
        history = "Your attribute: {}, skill: {}, the d10: {} and the location {}(-{}), resulting = {} and if it hits does {}({}) x {} = {}".format(
            attribute, skill, d10_list[0], location[2],location[0], result, damage['result'][0], damage['result'][1], location[1],if_it_hits)
        if critical:
            history = history + ". " + critical
        return {"result":result, "history":history}
    except Exception as e:
        return error_message(error_message=e)

def getDictRandom(human=None, monster=None):
    d10 = random.randint(1,10)
    dict_location = None
    if d10 == 1:
        dict_location = getDictRoll(1, human=human, monster=monster)
    elif d10 in (2,3,4):
        dict_location = getDictRoll(2, human=human, monster=monster)
    elif d10 == 5:
        dict_location = getDictRoll(3, human=human, monster=monster)
    elif d10 == 6:
        dict_location = getDictRoll(4, human=human, monster=monster)
    elif d10 in (7,8):
        dict_location = getDictRoll(5, human=human, monster=monster)
    if d10 in (9,10) and not monster:
        dict_location = getDictRoll(6, human=human, monster=monster)
    elif d10 in (9,10) and monster:
        dict_location = getDictRoll(5, human=human, monster=monster)
    if not dict_location:
        raise Exception(d10)
    return dict_location

def getDictRoll(
        value=None,
        human=None,
        monster=None):
    dict_location = None
    dict_location_humanoid_roll = {
        1:[6, 3, 'Head'],
        2: [1, 1, 'Torso'],
        3: [3, 0.5, 'R.arm'],
        4: [3, 0.5, 'L.arm'],
        5: [2, 0.5, 'R.leg'],
        6: [2, 0.5, 'L.leg']
    }
    dict_location_monster_roll = {
        1:[6, 3, 'Head'],
        2: [1, 1, 'Torso'],
        3: [3, 0.5, 'R.limb'],
        4: [3, 0.5, 'L.limb'],
        5: [2, 0.5, 'Appendices']
    }
    if human and value:
        dict_location = dict_location_humanoid_roll[value]
    elif human and not value:
        dict_location = dict_location_humanoid_roll
    if monster and value:
        dict_location = dict_location_monster_roll[value]
    elif monster and not value:
        dict_location = dict_location_monster_roll
    return dict_location

def dealWithDamage(damage):
    damage = damage.strip()
    damage = damage.split('d')
    bonus = 0
    dices = []
    try:
        if '+' in damage[1]:
            damage[1] = damage[1].split('+')
            bonus = damage[1][1]
            bonus = int(bonus)
            number_of_dice = int(damage[1][0])
        else:
            number_of_dice = int(damage[1])
        for i in range(1, int(damage[0]) + 1):
            dice = random.randint(1, number_of_dice + 1)
            dices.append(dice)
        dices_sum = sum(dices)
        dices_string = map(str, dices)
        if bonus > 0:
            history = "Number of dice rolled: {}, sum of dice rolled: {} + bonus: {}.".format(damage[0], dices, bonus)
            result = dices_sum + bonus
        else:
            history = "Number of dice rolled: {}, sum of dice rolled: {}.".format(damage[0], dices)
            result = dices_sum
        return {"history": history, "result": [result, '+'.join(dices_string)]}
    except Exception as e:
        return error_message(error_message=e)

@app.route('/home/tools/getDefense', methods=['GET', 'POST'])
def getDefense():
    attack = int(request.form.get('attack_value'))
    defense = int(request.form.get('defense_value'))

    difference = attack - defense
    critical = None
    if attack > defense:
        string_return = '\nThe attacker({}) has hit the defender({})!'.format(attack, defense)
    else:
        string_return = '\nThe attacker({}) missed the defender({})!'.format(attack, defense)
    if difference in range(7,9):
        critical = getDictCritical(7)
    elif difference in range(10,12):
        critical = getDictCritical(10)
    elif difference in range(13,14):
        critical = getDictCritical(13)
    elif difference >= 15:
        critical = getDictCritical(15)
    if critical:
        string_return += "And you hit a {} critical doint + {} damage".format(critical[0], critical[1])
    return {"result": string_return}

def getDictCritical(difference):
    dict_critical = {
        7: ["Simple", 3],
        10: ["Complex", 5],
        13: ["Difficult", 8],
        15: ["Deadly", 10]
    }

    return dict_critical[difference]

@app.route('/home/tools/initiativeCalculator', methods=['GET', 'POST'])
def initiativeCalculator():
    initiativeCalculator = get_template_attribute("macro_table_ini.html","table_ini")
    title = 'Initiative Calculator'
    return render_template('tools.html', initiativeCalculator=initiativeCalculator, title=title)
    
@app.route('/home/tools/calculateInitiave', methods=['GET', 'POST'])
def CalculateInitiave():
    number_of_characters = request.form.items()
    for i in number_of_characters:
        char_list = json.loads(i[0])
    for char in char_list:
        roll = random.randint(1,10)
        char['result'] = int(char['reflex']) or 0 + (roll if not char['roll'] else 0)
    list_initiave_sorted = sorted(char_list, key=itemgetter('result'), reverse=True)
    for index, value in enumerate(list_initiave_sorted):
        value['index'] = index
    return {"template": render_template('macro_table_ini.html', list_initiave_sorted=list_initiave_sorted)}