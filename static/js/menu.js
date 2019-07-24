
var sco = document.getElementById("scolarite");
var ref = document.getElementById("referentiel");
var pro = document.getElementById("promotion");

var s_sco = document.getElementById("s-sco");
var s_ref = document.getElementById("s-ref");
var s_pro = document.getElementById("s-pro");



s_sco.style.display = 'none';
s_ref.style.display = 'none';
s_pro.style.display = 'none';

sco.onclick = function() {
    s_ref.style.display = 'none';
    s_pro.style.display = 'none';
    if (s_sco.style.display === 'none') {
        s_sco.style.display = 'block';
    } else {
        s_sco.style.display = 'none';
    }
}

ref.onclick = function() {
    s_sco.style.display = 'none';
    s_pro.style.display = 'none';
    if (s_ref.style.display === 'none') {
        s_ref.style.display = 'block';
    } else {
        s_ref.style.display = 'none';
    }
}

pro.onclick = function() {
    s_sco.style.display = 'none';
    s_ref.style.display = 'none';
    if (s_pro.style.display === 'none') {
        s_pro.style.display = 'block';
    } else {
        s_pro.style.display = 'none';
    }
}



// var bloc2 = document.getElementById('bloc2')
// function f_ajout_sco() {
//     //alert("hi papy")
//     bloc2.style.display = 'block'
// }

// var bloc3 = document.getElementById('bloc3')
// function f_ajout_ref() {
//     //alert("hi papy")
//     bloc3.style.display = 'block'
// }

// var bloc4 = document.getElementById('bloc4')
// function f_ajout_promo() {
//     //alert("hi papy")
//     bloc4.style.display = 'block'
// }