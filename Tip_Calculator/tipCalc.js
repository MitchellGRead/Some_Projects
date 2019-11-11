$("#calc-tip-button").click(tip_button);

function tip_button() {
    let bill_amt = $("#bill-total").val();
    let tip_pct = $("#tip-amount").val();
    let num_people = $("#num-people").val();
    let result = $("#result");

    error_msg = verify_entries(bill_amt, tip_pct, num_people);
    if (error_msg != "") {
        result.css("color", "red");
        result.html(error_msg);
    } else {
        let total_per_person = ((bill_amt * tip_pct) / num_people).toFixed(2);
        let success_msg = "Each person gives a <br> $" + total_per_person + " tip.";
        result.css("color", "black");
        result.html(success_msg);
    }
}

function verify_entries(bill_amt, tip_pct, num_people) {
    error_msg = "";
    if (bill_amt == "") {
        error_msg += "Your bill amount is invalid.<br>";
    }

    if (tip_pct == null) {
        error_msg += "Please select a tip percentage. <br>";
    }

    if (num_people == "") {
        error_msg += "Please enter the number of people sharing the bill. <br>";
    }

    if (num_people % 1 != 0) {
        error_msg += "Number of people must be a whole number. <br>";
    }

    return error_msg;
}