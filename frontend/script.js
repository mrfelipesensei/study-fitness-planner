document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("preference-form");
    const routineSection = document.getElementById("routine-section");
    const routineOutput = document.getElementById("routine-output");
    const generateAgainBtn = document.getElementById("generate-again");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        //Coleta de dados
        const name = document.getElementById("name").value.trim();
        const goal = document.getElementById("goal").value;
        const hours = parseInt(document.getElementById("hours").value);
        const time = document.getElementById("time").value;
        const days = Array.from(
            document.querySelectorAll("input[name='days']:checked")
        ).map((el) => el.value);

        if (!name || !goal || !hours || !time || days.length === 0) {
            alert("Por favor, preencha todos os campos.");
            return;
        }


    })

});