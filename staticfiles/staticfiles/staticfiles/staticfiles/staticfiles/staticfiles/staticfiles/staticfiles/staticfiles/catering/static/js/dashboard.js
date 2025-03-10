document.addEventListener("DOMContentLoaded", function() {
    // Animate sidebar
    gsap.from(".sidebar", {
        duration: 1,
        x: -300,
        ease: "power3.out",
    });

    // Animate main content when it enters the page
    gsap.from(".main-content", {
        duration: 1.5,
        opacity: 0,
        y: 100,
        ease: "power4.out",
        delay: 0.5,
    });

    // Animate top navigation elements
    gsap.from(".top-nav .greeting", {
        duration: 1,
        opacity: 0,
        y: -50,
        ease: "power2.out",
        delay: 1,
    });

    gsap.from(".top-nav .user-profile", {
        duration: 1,
        opacity: 0,
        x: 50,
        ease: "power2.out",
        delay: 1.2,
    });

    // Animate stats cards with stagger effect
    gsap.from(".card", {
        duration: 1,
        opacity: 0,
        y: 50,
        stagger: 0.2,
        ease: "power3.out",
        delay: 1.5,
    });
});
