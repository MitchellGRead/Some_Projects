// console.log($("#grade-table tr td").length)

window.setInterval(add_row, 500);
window.setInterval(check_inputs, 500);

function add_row() {
    let last_grade_val = $("#grade-table tr:last td input").eq(0).val();
    let last_weight_val = $("#grade-table tr:last td input").eq(1).val();

    if (last_grade_val != "" && last_weight_val != "") {
        $("#grade-table tr:last").after("<tr><td> <input type=\"number\" min=\"0\" max=\"100\" class=\"their-weight\" name=\"their-weight\"></td><td><input type=\"number\" min=\"0\" max=\"100\" class=\"total-weight\" name=\"total-weight\"></td></tr>");
    }
}

function check_inputs() {
    let grade_table = $("#grade-table tr td input");
    let cell_val = 0;

    for (let i = 0; i < grade_table.length; i++) {
        cell_val = grade_table.eq(i).val();

        if (cell_val > 100) {
            grade_table.eq(i).val(100);
        } else if (cell_val < 1 && i % 2 != 0 && cell_val != ""){
            grade_table.eq(i).val(1);
        } else if (cell_val < 0) {
            grade_table.eq(i).val(0);
        }
    }
}

$("#delete-row-btn").click(function () {
    if ($("#grade-table tr").length > 2) {
        $("#grade-table tr:last").prev().remove();
    }
});

$("#reset-grade-btn").click(function() {
    $("#grade-table").find("tr:gt(0)").remove();
    $("#average-grade").html();
});

$("#calculate-grade-btn").click(function() {
    let result = $("#average-grade");
    if ($("#grade-table tr").length <= 2) {
        result.css("color", "red");
        result.html("<strong>Please enter valid inputs.</strong>");
        return
    }

    let grade_table = $("#grade-table tr td input");
    let numerator = 0;
    let denominator = 0;

    for (let i = 0; i < (grade_table.length / 2) - 1; i++) {
        // gets the left * right cell in a row
        numerator += parseInt(grade_table.eq(i * 2).val(), 10) * parseInt(grade_table.eq(i * 2 + 1).val(), 10);

        // gets the right cell in a row
        denominator += parseInt(grade_table.eq(i * 2 + 1).val(), 10);
    }

    result.css("color", "black");
    result.html("<strong>Average grade is: " + numerator / denominator + "</strong>");
});