$(function () {
    adjust_canvas();
    update_arr_slider();
});

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

let algo_to_use = $("#algo-select").val();
$("#algo-select").change(function () {
    algo_to_use = $("#algo-select").val();
});

/**
 * Variables that will be used for the animation
 */
let arr_to_sort = [];
let animation_controller = null;

function create_arr() {
    /**
     * Generates a new random array for sorting
     */
    arr_to_sort = [];
    let num_vals = parseInt($("#arr-size").val());
    let val = 0;

    for (let i = 0; i < num_vals; i++) {
        val = Math.random();
        if (val < 0.05) val += .05;
        arr_to_sort.push(val);
    }

    let canvas = $("#arr-display")[0];
    animation_controller = new sorting(canvas, arr_to_sort);
}
$("#gen-arr").click(create_arr);

function run_animation() {
    if (animation_controller == null) {
        $("#error-modal").modal({
            keyboard: true,
            focus: true,
        });
        return
    }

    let sorting_algo = animation_controller.get_sorting_func(algo_to_use);

    sorting_algo(animation_controller);
    
    animation_controller.animate_sorting(500);
}
$("#start-sort").click(run_animation);




