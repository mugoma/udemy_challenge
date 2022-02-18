//Check if the multi-choice buttons have at least one option selected
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("quiz-submit").addEventListener("click", function (event) {
        const questions_div = document.getElementById("quiz-form").querySelectorAll('div[id*="question"]');
        for (let i = 0; i < questions_div.length; i++) {
            const element = questions_div[i];
            const checkboxes = element.querySelectorAll("input[type=checkbox]").length;
            const checked = element.querySelectorAll("input[type=checkbox]:checked").length;
            if (checkboxes > 0 && !checked) {
                alert(`You must select at least one answer for question ${i + 1}.`);
                event.preventDefault()
                return false;
            }

        }
    })

})