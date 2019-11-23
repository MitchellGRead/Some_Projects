const DEFAULT_COLOR = '#61b3ff';
const COMPARE_COLOR = '#fa4848';
const SWAP_COLOR = '#67cc56';

class sorting {
    constructor(canvas, arr) {
        this.canvas = canvas;
        this.sort_data = arr;
        this.display_data = [];
        this.color = [];
        this.actions = [];

        for (let i = 0; i < arr.length; i++) {
            this.display_data.push(arr[i]);
            this.color.push(DEFAULT_COLOR);
        }

        this.draw_array();
    }

    draw_array() {
        let c = this.canvas.getContext('2d');
        c.clearRect(0, 0, innerWidth, innerHeight);

        let margin = 2;
        let y_margin = 20;
        let spacing = this.canvas.width / (margin * this.display_data.length + this.display_data.length + 1);
        let bar_width = spacing * margin;

        let x = bar_width / 2;
        for (let i = 0; i < this.display_data.length; i++) {
            c.fillStyle = this.color[i];
            c.fillRect(x, this.canvas.height - y_margin, bar_width, -this.display_data[i] * (this.canvas.height - y_margin * 2));
            x += spacing + bar_width;
        }
    }
    
    swap(i, j) {
        this.actions.push(['swap', i, j]);
        let temp = this.sort_data[i];
        this.sort_data[i] = this.sort_data[j];
        this.sort_data[j] = temp;
    }

    compare(i, j) {
        /**
         * Compares if the value at index i is less then the value at index j
         */
        this.actions.push(['compare', i, j]);
        return this.sort_data[i] < this.sort_data[j];
    }

    less_then(i, j) {
        /**
         * See if the value at index i is less then that at index j
         */
        return this.compare(i, j);
    }

    get_sorting_func(algo_input) {
        let avail_algos = {
            'quick_sort': quick_sort,
            'merge_sort': merge_sort,
        };

        return avail_algos[algo_input];
    }

    length() {
        return this.sort_data.length;
    }

    print_arr() {
        console.log(this.sort_data);
    }

    get_actions() {
        return this.actions;
    }

    _sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async animate_sorting(speed) {
        if (this.actions.length < 1) {
            return;
        }

        for (let i = 0; i < this.actions.length; i++) {
            this._consume_action();
            this._sleep(speed);
        }
    }

    _consume_action() {
        if (this.actions.length < 1) {
            return;
        }

        let data = this.actions.shift();
        let action = data[0];
        let index_i = data[1];
        let index_j = data[2];
        
        if (action == 'swap') {
            // Assign the colors
            this.color[index_i] = SWAP_COLOR;
            this.color[index_j] = SWAP_COLOR;

            // Swap the values in display array
            let temp = this.display_data[index_i];
            this.display_data[index_i] = this.display_data[index_j];
            this.display_data[index_j] = temp;
        } else if (action == 'compare') {
            //Assign the colors
            this.color[index_i] = COMPARE_COLOR;
            this.color[index_j] = COMPARE_COLOR;
        }
        
        // Redraw the array
        this.draw_array();
        
        // Reset the colours
        this.color[index_i] = DEFAULT_COLOR;
        this.color[index_j] = DEFAULT_COLOR;
    }

}

function merge_sort(animation, low, high) {
    return
}


function quick_sort(animation, low, high) {
    let arr_length = animation.length();
    if (low == undefined) {
        low = 0;
    }

    if (high == undefined) {
        high = arr_length - 1;
    }

    if (low < high) {
        pivot = partition(animation, low, high);
        quick_sort(animation, low, pivot);
        quick_sort(animation, pivot + 1, high);
    }
}

function partition(animation, low, high) {
    pivot_index = Math.floor(low + (high - low) / 2);
    i = low - 1;
    j = high + 1;

    while (true) {
        do {
            i += 1;
        } while (animation.less_then(i, pivot_index));

        do {
            j -= 1;
        } while (animation.less_then(pivot_index, j));

        if (i >= j) {
            return j;
        }

        animation.swap(i, j);
    }
}


// /**
//  * TODO
//  * write sorting algorithm
//  * ensure sorting actions 
//  * step through each sorting action and update the canvas
//  *      consume the action (pop) once it has been animated
//  * Look into several algos and see how they work and what is needed!!
//  */