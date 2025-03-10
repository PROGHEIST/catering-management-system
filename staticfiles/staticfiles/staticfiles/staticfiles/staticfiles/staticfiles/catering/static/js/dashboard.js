var tl = gsap.timeline();
var navs = document.querySelectorAll('#nav-links');

tl.from('#logo', {
    duration: 0.5,
    y: -100,
    opacity: 0
})
tl.from(navs, {
    duration: 0.5,
    y: -100,
    opacity: 0,
    stagger: 0.2
})

tl.from('#main-head', {
    duration: 0.5,
    y: -100,
    opacity: 0,
    stagger: 0.2
})

tl.from('#booking-container h2', {
    duration: 0.5,
    y: -100,
    opacity: 0,
    stagger: 0.2
})
tl.from('#booking-container div', {
    duration: 0.5,
    scale: 0,
    opacity: 0,
    stagger: 0.2
})

gsap.to('.your-events',{
    duration: 0.5,
    x: -100,
    scrollTrigger: {
        trigger: '.your-events h1',
        start: 'top 80%',
        end: 'top 50%',
        scrub: 2,
        pin: true
    }
})


onscroll = function () {
    if (window.scrollY > 100) {
        gsap.to('nav',{
            duration: 0.5,
            backgroundColor: 'rgb(41, 41, 41)',
        })
    } else {
        gsap.to('nav',{
            duration: 0.5,
            backgroundColor: 'transparent',
        })
    }
}

// ------
