
function check_uncheck(value){
   if(value === 1){
        $('#monster').prop('checked', false);
   }
   else{
        $('#humanoid').prop('checked', false);
   }
}

var countd4 = 0;
var countd6 = 0;
var countd8 = 0;
var countd10 = 0;
var countd20 = 0;


function getDice(dice, reduce, dice_type, not_roll){
    if(!reduce){
        if (dice_type == 4) countd4++ 
        if (dice_type == 6) countd6++
        if (dice_type == 8) countd8++
        if (dice_type == 10) countd10++
        if (dice_type == 20) countd20++
    }
    else{
        if (dice_type == 4  && countd4 > 0) countd4--
        if (dice_type == 6 && countd6 > 0) countd6--
        if (dice_type == 8 && countd8 > 0 ) countd8--
        if (dice_type == 10 && countd10 > 0 ) countd10--
        if (dice_type == 20 && countd20 > 0) countd20--

    }
    var count = eval("countd" + dice_type);;
    return getNumberOfDice(dice, count, not_roll)
}

function getNumberOfDice(dice, count, not_roll){
    if(!not_roll){
        dice.className = ''
        dice.className = 'text-white form-control mr-4 dice-to-roll'
    }
    var dice_div = document.getElementById('div-' + dice.id)
    dice_div.innerHTML = " (" + count + ")"
}

function clearNumberOfDice(dice){
    var dice_div = document.getElementById('div-' + dice.id)
    dice_div.innerHTML = ''
    count = 0;
}

function diceRoller(){
    var dices = document.getElementsByClassName('dice-to-roll')
    var list_dice = []
    for(var c = 0; c < dices.length; c++){
        var number = document.getElementById('div-' + dices[c].id)
        console.log(number.innerHTML)
        if(number.innerHTML !== '(0)') {
            var dict_dice = {"dice": dices[c].id, 'number': number.innerHTML}
            list_dice.push(dict_dice)
        }
    }
    return postWithAjax('/dice_roller', {"dices": JSON.stringify(list_dice)}, _dicerRoller)
}

function _dicerRoller(response){
    var div_result = document.getElementById('roller-result')
    div_result.innerHTML = '';
    // div_result.innerHTML = 'You rolled: ' + response.dices + ' , for a total of ' + response.result
    div_result.innerHTML = response.message
}

function getDamageLocation(){
    var dict_form = {}
    $('input:checkbox.aiming').each(function () {
        var aiming = (this.checked ? $(this).val() : "");
        if(aiming){
            dict_form['aiming'] = this.id
        }
    });
    $('input:checkbox.enemy_type').each(function () {
        var enemy_type = (this.checked ? $(this).val() : "");
        if(enemy_type){
            dict_form['enemy_type'] = this.id
        }
    });

    var human_location = document.getElementById('human_location_select')
    dict_form['human_location'] = human_location.value
    var monster_location = document.getElementById('monster_location_select')
    dict_form['monster_location'] = monster_location.value
    var attribute = document.getElementById('attribute')
    dict_form['attribute'] = attribute.value
    var skill = document.getElementById('skill')
    dict_form['skill'] = skill.value
    var damage = document.getElementById('damage')
    dict_form['damage'] = damage.value
    postWithAjax('/home/tools/combat/getDamageLocation', dict_form, getDamageLocationPost)
}

function getDamageLocationPost(response){
    var message = document.getElementById('message')
    message.innerHTML = response['history']
    document.getElementById('attack_value').value  = response['result']
    message.style.display = 'block'
}

function NumberOfCharacters(number){
    var for_number = $('#for_number')
    for_number.html("")
    if (number.value > 30){
        number.value = 30
    }
    for(var c=0; c < number.value;c++){
        var label = "<label class='ml-3'>Character: </label>";
        var input_name = "<input name='input-name' style='width:10%;background-color: #462300;' class='input-name text-white mr-4 mt-2 rounded'>";
        var label_reflex = "<label class='ml-3'>Reflex :</label>";
        var input_reflex = "<input name='input-reflex' type='number' style='width:10%;background-color: #462300;' class='input-reflex text-white mr-4 mt-2 rounded'>";
        var label_health = "<label class='ml-3'>Health :</label>";
        var input_health = "<input name='input-health' type='number' style='width:10%;background-color: #462300;' class='input-health text-white mr-4 mt-2 rounded'>";
        var input_roll = "<input name='input-roll' id='input-roll' type='checkbox' class='input-roll'>";
        var label_roll = "<label  for='input-roll' class='ml-3'>Not Roll for this Character? :</label>";
        var for_number_html = for_number.html();
        var button = "<button class='btn btn-primary'>CalculateInitiave()</button>"
        $('#for_number').html(for_number_html + label +  input_name + label_reflex + input_reflex +  label_health + input_health + label_roll + input_roll + "<br>");
    }
}

function CalculateInitiave(){
    var class_char_name = document.getElementsByClassName('input-name')
    var class_char_reflex = document.getElementsByClassName('input-reflex')
    var class_char_health = document.getElementsByClassName('input-health')
    var class_char_roll = document.getElementsByClassName('input-roll')
    var list_char = []
    for (var i = 0; i < class_char_name.length; i++) {
        var string_key = class_char_name[i].value
        string_key = string_key.toString()
        var dict_char = {}
        dict_char['name'] = string_key
        dict_char["reflex"] = class_char_reflex[i].value
        dict_char["health"] = class_char_health[i].value
        if (class_char_roll[i].checked === true){
            dict_char['roll'] = class_char_roll[i].value
        }
        else{
            dict_char['roll'] = null
        }
        list_char.push(dict_char)
    }
    console.log(list_char)
    var dict_char = JSON.stringify(list_char);
    postWithAjax('/home/tools/calculateInitiave', dict_char, CalculateInitiavePost)
}

function CalculateInitiavePost(response){
    $('#return-table').html(response['template']);
    $("#table-ini").tableDnD();
}

function deleteTd(td_id){
    var id = 'td-' + td_id.value
    document.getElementById(id).remove()
}

var row_counter = -1;
var round_counter = 0;
var table_deact = document.getElementsByClassName('row-deactive')
var table_act = document.getElementsByClassName('row-active')
function nextCharacter(){
    if(row_counter >= table_deact.length){
        round_counter++;
        row_counter = -1;
        $('#round_counter').html('Round Counter ' + round_counter)
        $(".row-active").attr('class', 'row-deactive')
        row_counter++;
        var row_id = table_deact[row_counter].id
        $("#"+ row_id).attr('class', 'row-active')
    }
    else{
        $(".row-active").attr('class', 'row-deactive')
        row_counter++;
        var row_id = table_deact[row_counter].id
        $("#"+ row_id).attr('class', 'row-active')
    }
    
}

function deleteWeapon(weapon){
    var dict_id = {"id": weapon.value}
    console.log(dict_id)
    postWithAjax('/home/deleteWeapon', dict_id)
    setTimeout(function(){window.location.reload(); }, 100);
}

function deleteArmor(armor){
    var dict_id = {"id": armor.value}
    postWithAjax('/home/armor/delete_armor', dict_id)
    setTimeout(function(){window.location.reload(); }, 100);
}

function getDefense(defense){
    let form_data = new FormData()
    var attack_value = document.getElementById('attack_value').value;
    var dict_combat = {}
    var list_char = []
    dict_combat['attack_value'] = attack_value
    dict_combat["defense_value"] = defense.value
    list_char.push(dict_combat)
    form_data.append("attack_value", attack_value)
    form_data.append("defense_value", defense.value)
    setTimeout(function(){
        postWithAjax('/home/tools/getDefense', dict_combat, getDefensePost)
        message.style.display = 'block' }, 200);
}

function getDefensePost(response){
        message.innerHTML = ''
        message.innerHTML = message.innerHTML + response['result']
        message.style.display = 'block'
}

function postWithAjax(url, data, method){
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function(response){
            try {
                response = JSON.parse(response)
              }
            catch (e) {
                false
            }

            if(response.success === undefined && response.success != false){
                if(method) return method(response)
            }
            else{
                return onErrorResponse(response)
            }
        },
        error: function (response) {
            return onErrorResponse(response)
        }
    });
}

function onErrorResponse(err){
    let div_error = $('#div_for_error').append(err.response)
}