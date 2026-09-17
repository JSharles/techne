(function () {
  function shuffled(values) {
    const result = values.slice();
    for (let index = result.length - 1; index > 0; index -= 1) {
      const other = Math.floor(Math.random() * (index + 1));
      [result[index], result[other]] = [result[other], result[index]];
    }
    return result;
  }

  function mount(root, questions) {
    root.classList.add("activity", "quiz");
    let answered = 0;
    let correct = 0;
    const score = document.createElement("p");

    questions.forEach((question, questionIndex) => {
      const section = document.createElement("section");
      section.className = "quiz-question";
      const prompt = document.createElement("p");
      prompt.innerHTML = `<strong>${questionIndex + 1}.</strong> ${question.q}`;
      const options = document.createElement("div");
      options.className = "options";
      const feedback = document.createElement("p");

      const indexed = question.options.map((text, index) => ({ text, index }));
      shuffled(indexed).forEach(({ text, index }) => {
        const button = document.createElement("button");
        button.type = "button";
        button.innerHTML = text;
        button.dataset.index = String(index);
        button.addEventListener("click", () => {
          options.querySelectorAll("button").forEach((item) => { item.disabled = true; });
          const isCorrect = index === question.answer;
          button.classList.add(isCorrect ? "correct" : "wrong");
          if (!isCorrect) options.querySelector(`[data-index="${question.answer}"]`)?.classList.add("correct");
          feedback.textContent = `${isCorrect ? "Oui." : "Non."} ${question.explain || ""}`;
          answered += 1;
          if (isCorrect) correct += 1;
          score.textContent = `${answered}/${questions.length} répondues · ${correct} correctes`;
          window.Progress?.send({
            kind: "quiz",
            question: questionIndex + 1,
            prompt: prompt.textContent.slice(0, 240),
            chosen: question.options[index],
            correct: isCorrect,
          });
        });
        options.append(button);
      });

      section.append(prompt, options, feedback);
      root.append(section);
    });
    root.append(score);
  }

  window.Quiz = { mount };
})();
