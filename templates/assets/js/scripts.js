(() => {
  const $formDelete = document.querySelectorAll(".delete-recipe-form")

  $formDelete.forEach(
    (html) => {
      html.addEventListener(
        "submit", (e) => {
          e.preventDefault();
          const confirmed = confirm("Are you sure?")

          if (confirmed) { html.submit() }
        }
      );
    }
  );
})();

