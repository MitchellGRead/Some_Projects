const DEFAULT_COLOR = '#61b3ff';
const CURRENT_INDEX_COLOR = '#fa4848';
const SWAP_COLOR = '#67cc56';

let canvas = $("#arr-display")[0];

// array and animation variables
let arr_to_sort = [];
let colors = [];
let sort_actions = [];

let algo_to_use = '';

/**
 * TODO
 * modify to not be whole numbers
 */
function create_arr() {
    /**
     * Generates a new random array for sorting
     */
    arr_to_sort = [];
    colors = [];
    let num_vals = parseInt($("#arr-size").val());
    let val = 0;

    for (let i = 0; i < num_vals; i++) {
        val = Math.floor(Math.random() * (num_vals * 2) + 10);
        colors.push(DEFAULT_COLOR);
        arr_to_sort.push(val);
    }

    draw_array(canvas, arr_to_sort, colors);
}
$("#gen-arr").click(create_arr);

/**
 * TODO
 * modify rect y-axis to fit dynamically
 * allow for negatives
 * redraw the array on window resize
 * modify to draw without whole numbers
 */
function draw_array(canvas, arr, colors) {
    /**
     * Draws the generated array to the canvas
     */
    let c = canvas.getContext('2d');

    clear_canvas(c);

    let margin = 2;
    let spacing = canvas.width / (margin * arr.length + arr.length + 1);
    let bar_width = spacing * margin;

    let x = bar_width / 2;
    for (let i = 0; i < arr.length; i++) {
        c.fillStyle = colors[i];
        c.fillRect(x, canvas.height - 20, bar_width, -arr[i]);
        x += spacing + bar_width;
    }
}

function clear_canvas(context) {
    /**
     * Clears the canvas
     */
    context.clearRect(0, 0, innerWidth, innerHeight);
}

function compare(i, j) {
    /**
     * Compares two array index values.
     * Less then zero meanings arr[i] > arr[j]
     */
    sort_actions.push(['compare', i, j]);
    return arr_to_sort[i] - arr_to_sort[j];
}

function less_then(i, j) {
    /**
     * Sees if value at index i is < value at index j
     */
    return compare(i, j) < 0;
}

function swap(i, j) {
    /**
     * Swaps the values of index i and j in the array
     */
    let temp = arr_to_sort[i];
    arr_to_sort[i] = arr_to_sort[j];
    arr_to_sort[j] = temp;

    sort_actions.push(['swap', i, j]);
    return;
}

$("#start-sort").click(function() {
    algo_to_use = $("#algo-select").val();
});

function quick_sort() {
    console.log('quicky boi');
    return
}


/**
 * TODO
 * determine what algo to use when the user clicks the start button
 * write sorting algorithm
 * ensure sorting actions 
 * step through each sorting action and update the canvas
 *      consume the action (pop) once it has been animated
 */