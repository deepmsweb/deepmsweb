
/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */

function showFileName(input,id,text) {
    var infoArea = document.getElementById(id);
    if (input.files && input.files[0]) {
        var fileName = input.files[0].name;
        infoArea.textContent = text + fileName;
    }
}

/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        input.messages = ""
        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);

    }
}
function readURL2(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#imageResult2')
                .attr('src', e.target.result);
        };
        input.messages = ""
        reader.readAsDataURL(input.files[0]);
    }

}

/*  ==========================================
    same anorher fx
* ========================================== */
function showHide(secim) {
    $("#" + secim).toggle();
}
function showModel(secim) {
    
        $('#imagepreview').attr('src', $("#" + secim+"_img").attr('src')); // here asign the image to the modal when the user click the enlarge link
        $('#imagemodal').modal('show'); // imagemodal is the id attribute assigned to the bootstrap modal, then i use the show function
}


/*  ==========================================
    same anorher
* ========================================== */



$(function () {
    $('#upload0').on('change', function () {
        readURL(input0);
    });
    $('#upload1').on('change', function () {
        readURL(input1);
    });
    $('#upload2').on('change', function () {
        readURL2(input2);
    });

});

