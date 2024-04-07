document.addEventListener('DOMContentLoaded', (event) => {
    let slideIndex = 0;
    const slides = document.getElementsByClassName("mySlides");
    const next = document.querySelector(".w3-right");
    const prev = document.querySelector(".w3-left");
  
    function showSlides() {
      if (slideIndex >= slides.length) { slideIndex = 0; }
      if (slideIndex < 0) { slideIndex = slides.length - 1; }
      Array.from(slides).forEach(slide => slide.style.display = "none");
      slides[slideIndex].style.display = "block";
      slideIndex++;
    }
  
    next.addEventListener('click', () => {
      slideIndex++;
      showSlides();
    });
  
    prev.addEventListener('click', () => {
      slideIndex--;
      showSlides();
    });
  
    showSlides(); // Start the slideshow
  });
  