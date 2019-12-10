const DEFAULT_COLOR = '#61b3ff';
const COMPARE_COLOR = '#fa4848';
const SWAP_COLOR = '#67cc56';

class visualizer {
    constructor(canvas, arr) {
        this.canvas = canvas;
        this.sort_data = arr;
        this.display_data = [...arr];
        this.color = Array(arr.length).fill(DEFAULT_COLOR);
        this.actions = [];
        this.num_swaps = 0;
        this.num_comps = 0;
        this.finished = false;

        draw_array(this.canvas, this.display_data, this.color);
    }

    get_sorting_func(algo_input) {
        let avail_algos = {
            'quick_sort': quick_sort,
            'merge_sort': merge_sort,
            'selection_sort': selection_sort,
            // 'insertion_sort': insertion_sort,
            // 'heap_sort': heap_sort,
        };

        return avail_algos[algo_input];
    }

    get_sort_data() {
        return this.sort_data;
    }

    add_swap_action(i, j) {
        this.actions.push(['swap', i, j]);
    }

    add_compare_action(i, j) {
        this.actions.push(['compare', i, j]);
    }
    
    get_swap_count() {
        return this.num_swaps;
    }

    get_comp_count() {
        return this.num_comps;
    }

    check_status() {
        return this.actions.length == 0;
    }
    
    set_finished(bool) {
        this.finished = bool;
    }

    get_finished() {
        return this.finished;
    }


    animate_sorting(handler, speed) {
        let id = window.setInterval(function () {
            if (handler.check_status()) {
                clearInterval(id);
                handler.set_finished(true);
            }

            handler._consume_action();
            $("#sort-metrics").html("Comparisons: " + handler.get_comp_count() + "<br>" +
                "Swaps: " + handler.get_swap_count());
        }, speed);

    }

    _consume_action() {
        if (this.actions.length < 1) {
            draw_array(this.canvas, this.display_data, this.color);
            return;
        }

        let data = this.actions.shift();
        console.log(data);
        let action = data[0];
        let i = data[1];
        let j = data[2];
        
        if (action == 'swap') {
            // Assign the colors
            this.color[i] = SWAP_COLOR;
            this.color[j] = SWAP_COLOR;

            // Swap the values in display array
            let temp = this.display_data[i];
            this.display_data[i] = this.display_data[j];
            this.display_data[j] = temp;

            // Increment swap counter
            this.num_swaps += 1;
        } else if (action == 'compare') {
            //Assign the colors
            this.color[i] = COMPARE_COLOR;
            this.color[j] = COMPARE_COLOR;

            // Increment comparisons counter
            this.num_comps += 1;
        }
        
        // Redraw the array
        draw_array(this.canvas, this.display_data, this.color);
        
        // Reset the colours
        this.color[i] = DEFAULT_COLOR;
        this.color[j] = DEFAULT_COLOR;
    }

}


function draw_array(canvas, arr, color) {
    let c = canvas.getContext('2d');
    c.clearRect(0, 0, innerWidth, innerHeight);

    let margin = 2; // How large of gap between the bars - lower makes gap larger and supports higher array sizes
    let y_margin = 20; // How far above the canvas to be - lower puts closer to bottom.
    let spacing = canvas.width / (margin * arr.length + arr.length + 1);
    let bar_width = spacing * margin;

    let x = spacing;
    for (let i = 0; i < arr.length; i++) {
        c.fillStyle = color[i];
        c.fillRect(x, canvas.height - y_margin, bar_width, -arr[i] * (canvas.height - y_margin * 2));
        x += spacing + bar_width;
    }
}

function selection_sort(animation, arr) {
    let min = 0;
    for (let i = 0; i < arr.length; i++) {
        min = i;
        for (let j = i + 1; j < arr.length; j++) {
            if (arr[j] < arr[min]) {
                min = j;
                animation.add_compare_action(j, min);
            }            
        }

        if (i != min) {
            swap(arr, i, min);
            animation.add_swap_action(i, min);
        }
    }
}


function merge_sort(animation, arr) {
    if (arr.length <= 1) {
        return arr
    }

    let mid = Math.ceil(arr.length / 2);
    let left = arr.slice(0, mid);
    let right = arr.slice(mid);

    left = merge_sort(animation, left);
    right = merge_sort(animation, right);

    return merge(left, right);
}

function merge(animation, left, right) {
    let res = [];
    let left_index = 0;
    let right_index = 0;

    while (left.length > left_index && right.length > right_index) {
        if (left[left_index] < right[right_index]) {
            // animation.add_compare_action(left_index, right_index);

            res.push(left[left_index]);
            left_index += 1;
        } else if (right[right_index] >= left[left_index]) {
            // animation.add_compare_action(right_index, left_index);

            res.push(right[right_index]);
            right_index += 1;
        }
    }

    return res.concat(left.slice(left_index)).concat(right.slice(right_index));
}


function quick_sort(animation, arr, low, high) {
    if (low == undefined) {
        low = 0;
    }

    if (high == undefined) {
        high = arr.length - 1;
    }

    if (low < high) {
        pivot = partition(animation, arr, low, high);
        quick_sort(animation, arr, low, pivot - 1);
        quick_sort(animation, arr, pivot + 1, high);
    }
}

function partition(animation, arr, low, high) {
    pivot_index = low;
    for (let i = low; i < high; i++) {
        if (arr[i] < arr[high]) {
            animation.add_compare_action(i, high);

            if (i != pivot_index) {
                swap(arr, i, pivot_index);
                animation.add_swap_action(i, pivot_index);
            }
            pivot_index += 1;
        }
    }
    swap(arr, high, pivot_index);
    animation.add_swap_action(high, pivot_index);

    return pivot_index;
}

function swap(arr, i, j) {
    let temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}


// /**
//  * TODO
//  * write sorting algorithm
//  * ensure sorting actions 
//  * step through each sorting action and update the canvas
//  *      consume the action (pop) once it has been animated
//  * Look into several algos and see how they work and what is needed!!
//  */