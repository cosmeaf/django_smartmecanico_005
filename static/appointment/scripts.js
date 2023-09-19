// document.addEventListener('DOMContentLoaded', () => {
//     const inputElement = document.getElementById('id_hour');
//     const container = inputElement.parentElement;
//     const label = document.querySelector('label[for="id_hour"]');

//     const hoursList = Array.from({ length: 10 }, (_, i) => (i + 8) + ':00');

//     const listContainer = document.createElement('div');
//     listContainer.style.display = 'flex';
//     listContainer.style.flexWrap = 'wrap';
//     listContainer.style.fontSize = 'smaller';
//     listContainer.style.marginBottom = '10px';

//     hoursList.forEach(hour => {
//         const hourButton = document.createElement('button');
//         hourButton.textContent = hour;
//         hourButton.type = 'button';
//         hourButton.style.margin = '0 5px 5px 0';
//         hourButton.addEventListener('click', () => {
//             inputElement.value = hour;
//         });

//         listContainer.appendChild(hourButton);
//     });

//     container.insertBefore(listContainer, label);

//     // Corrected portion of code
    
// });


document.addEventListener('DOMContentLoaded', () => {
    const label = document.querySelector('label[for="id_day"]');

    // Criando contêiner principal para o botão, o card e o outro botão
    const mainContainer = document.createElement('div');
    mainContainer.style.display = 'flex';
    mainContainer.style.width = '50%';
    mainContainer.style.height = '50px';
    mainContainer.style.alignItems = 'center';

    // Criando o elemento do card
    const card = document.createElement('div');
    card.style.width = 'calc(100% - 10px)';
    card.style.height = '40px';
    card.style.backgroundColor = '#f1f1f1';
    card.style.border = '1px solid #ccc';
    card.style.display = 'flex';
    card.style.flexDirection = 'column';
    card.style.justifyContent = 'center';
    card.style.alignItems = 'center';

    // Criando uma lista com os dias da semana
    const daysOfWeek = ['Dom.', 'Seg.', 'Ter.', 'Qua.', 'Qui.', 'Sex.', 'Sab.'];

    // Criando uma linha para os dias da semana
    const weekRow = document.createElement('div');
    weekRow.style.display = 'flex';
    weekRow.style.justifyContent = 'space-around';
    weekRow.style.width = '100%';
    
    daysOfWeek.forEach(day => {
        const dayElem = document.createElement('div');
        dayElem.textContent = day;
        weekRow.appendChild(dayElem);
    });
    
    card.appendChild(weekRow);

    // Criando uma linha para os dias do mês
    const monthRow = document.createElement('div');
    monthRow.style.display = 'flex';
    monthRow.style.justifyContent = 'space-around';
    monthRow.style.width = '100%';
    card.appendChild(monthRow);

    mainContainer.appendChild(card);

    // Criando botões de navegação
    const createButton = (text) => {
        const button = document.createElement('button');
        button.textContent = text;
        button.style.height = '50px';
        button.style.width = '5px';
        return button;
    };

    const prevButton = createButton('<');
    mainContainer.insertBefore(prevButton, card);

    const nextButton = createButton('>');
    mainContainer.appendChild(nextButton);

    // Função para atualizar os dias do mês
    let currentWeek = 0;
    const updateDays = () => {
        monthRow.innerHTML = '';
        for (let i = 1 + (7 * currentWeek); i <= 7 + (7 * currentWeek); i++) {
            const dayElem = document.createElement('div');
            dayElem.textContent = i <= 31 ? String(i).padStart(2, '0') + '.' : '';
            monthRow.appendChild(dayElem);
        }
    };

    prevButton.onclick = () => {
        if (currentWeek > 0) {
            currentWeek -= 1;
            updateDays();
        }
    };

    nextButton.onclick = () => {
        if (currentWeek < 4) {
            currentWeek += 1;
            updateDays();
        }
    };

    // Inserindo o contêiner principal antes do label dentro do contêiner flexível
    label.parentElement.insertBefore(mainContainer, label);

    // Inicializando os dias
    updateDays();
});
