function toggleChoices(questionId) {
    const questionBox = document.getElementById(`question-box-${questionId}`);
    const choicesList = document.getElementById(`choices-list-${questionId}`);
    const moreButton = document.getElementById(`more-button-${questionId}`);
    const chartContainer = document.getElementById(`chart-container-${questionId}`);
    var bars = []
    if(chartContainer)
    {
      bars = chartContainer.getElementsByClassName('bar');
    }
    const isExpanded = choicesList.classList.contains('expanded');

    if (isExpanded) {
        choicesList.classList.remove('expanded');
        moreButton.textContent = 'More';
        questionBox.classList.remove('expanded');
        if(chartContainer)
        {
          for (const bar of bars) {
              bar.style.display = 'none';
          }
          chartContainer.classList.remove('expanded');
        }
    } else {
        choicesList.classList.add('expanded');
        moreButton.textContent = 'Less';
        questionBox.classList.add('expanded');
        if(chartContainer)
        {
          for (const bar of bars) {
              bar.style.display = 'block';
          }
          chartContainer.classList.add('expanded');
        }
    }
}

function setDarkMode(){
  const savedTheme = localStorage.getItem('theme');
  const isDarkMode = savedTheme === 'dark';
  if (isDarkMode) {
      document.documentElement.classList.remove('dark');
  } else {
    document.documentElement.classList.add('dark');
  }
  const toggleIcon = document.getElementById('toggle-dark');
 if (isDarkMode) {
     toggleIcon.textContent = '🌙';
 } else {
     toggleIcon.textContent = '☀️';
 }
}

function toggleDarkMode() {
    const isDarkMode = document.documentElement.classList.contains('dark');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    setDarkMode();
}

document.addEventListener("DOMContentLoaded", function () {
  setDarkMode();

  const choicesDiv = document.getElementById('choices');
  function addChoice() {
      const newChoice = document.querySelector('#choices div').cloneNode(true);
      newChoice.querySelector('input').value = '';
      choicesDiv.appendChild(newChoice);
  }

    document.getElementById('add-choice').addEventListener('click', function() {
        addChoice();
    });

    choicesDiv.addEventListener('input', function(event) {
        const lastInput = choicesDiv.lastElementChild.querySelector('input');
        if (event.target === lastInput && event.target.value !== '') {
            addChoice();
        }
    });





    const modal = document.getElementById("myModal");
    const openModalBtn = document.getElementById("openModalBtn");
    const closeModalBtn = document.getElementById("closeModalBtn");

    openModalBtn.onclick = function () {
        modal.style.display = "flex";
    };

    closeModalBtn.onclick = function () {
        modal.style.display = "none";
    };

    const createPollBtn = document.getElementById("createPollBtn");
    createPollBtn.onclick = function () {
        modal.style.display = "none";
    };


    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
});
