// User controller initializations
function init() {
    // Set the arr size display
    update_arr_slider();
    
    // Set canvas sizing
    adjust_canvas();
}
init();

// Update the slider value
function update_arr_slider() {
    let size_label = $("#arr-size").prev();
    size_label.html("Array Size: " + $("#arr-size").val());
}
$("#arr-size").on('input', update_arr_slider);

function adjust_canvas() {
    // remove hard codes later
    $("#arr-display")[0].width = window.innerWidth - 60;
    $("#arr-display")[0].height = window.innerHeight - 150;
    $("#arr-display").css("border", "30px solid #252830");
}
$(window).on('resize', adjust_canvas)



