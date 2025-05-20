document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("preference-form");
    const routineSection = document.getElementById("routine-section");
    const routineOutput = document.getElementById("routine-output");
    const generateAgainBtn = document.getElementById("generate-again");

    form.addEventListener("submit", async (e) => {
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

        try {
            //Envia os dados para o backend Flask
            const response = await fetch("http://localhost:5000/gerar-rotina", {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify({
                    goal,
                    hours,
                    time,
                    days
                })
            });

            if (!response.ok) {
                throw new Error("Erro ao se comunicar com o servidor.");
            }

            const rotina = await response.json();
            console.log("Rotina recebida:", rotina)

            //Exibe os dados da rotina recebidos dp backend
            routineOutput.innerHTML = ""; //Limpa conteúdo anterior
            Object.entries(rotina).forEach(([dia, atividade]) => {
                const card = document.createElement("div");
                card.classList.add("routine-card");

                const title = document.createElement("h3");
                title.textContent = capitalize(dia);

                const details = document.createElement("p");
                details.textContent = atividade;

                card.appendChild(title);
                card.appendChild(details);
                routineOutput.appendChild(card);
            });

            routineSection.classList.remove("hidden");
            routineSection.scrollIntoView({behavior: "smooth"});
        
        } catch (error) {
            console.error(error);
            alert("Erro ao gerar rotina. Veja o console para mais detalhes.");
        }
    });

    generateAgainBtn.addEventListener("click", () => {
        routineSection.classList.add("hidden");
        form.reset();
    });

    //Funções auxiliares
    function capitalize(word) {
        return word.charAt(0).toUpperCase() + word.slice(1);
    }
    
});