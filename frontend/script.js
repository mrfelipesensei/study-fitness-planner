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

        //Geração fictícia da rotina
        routineOutput.innerHTML = ""; //Limpa conteúdo anterior
        days.forEach((day) => {
            const card = document.createElement("div");
            const title = document.createElement("h3");
            const details = document.createElement("p");

            title.textContent = capitalize(day);
            details.textContent = generateRoutine(goal, hours, time);

            card.appendChild(title);
            card.appendChild(details);
            routineOutput.appendChild(card);
        });

        //Exibir rotina
        routineSection.classList.remove("hidden");
        routineSection.scrollIntoView({behavior: "smooth"});
    });

    generateAgainBtn.addEventListener("click", () => {
        routineSection.classList.add("hidden");
        form.reset();
    });

});