var marka_select = document.getElementById("Marka");
var seri_select = document.getElementById("Seri");
var model_select = document.getElementById("Model");
var submit_select = document.getElementById("Submit");
marka_select.onchange = function () {
    marka = marka_select.value;
    fetch('/marka=' + marka).then(function (response) {
        response.json().then(function (data) {
            var optionHTML = '';
            for (var seri of data.seriler) {
                optionHTML += '<option value="' + seri.value + '">' + seri.label + '</option>';
            }
            seri_select.innerHTML = optionHTML;
            seri_select.disabled = false;
            model_select.innerHTML = "";
            model_select.disabled = true;
        })
    });
}

seri_select.onchange = function () {
    marka = marka_select.value;
    seri = seri_select.value;
    fetch('/marka=' + marka + '&seri=' + seri).then(function (response) {
        response.json().then(function (data) {
            var optionHTML = '';
            for (var model of data.modeller) {
                optionHTML += '<option value="' + model.value + '">' + model.label + '</option>';
            }
            model_select.innerHTML = optionHTML;
            model_select.disabled = false;
        })
    });
}