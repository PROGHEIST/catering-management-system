var tl = gsap.timeline();
var navs = document.querySelectorAll('#nav-links');
var feature_card = document.querySelectorAll('.feature-card')

Array.from(feature_card).forEach(card => {
    card.onmouseover = function() {
        gsap.to(card, {
            duration: 0.5,
            scale: 1.1,
            backgroundColor: 'rgb(9, 255, 1)'
        });
    };
    card.onmouseout = function() {
        gsap.to(card, {
            duration: 0.5,
            scale: 1,
            boxShadow: 'none',
            backgroundColor: 'hsl(120, 55.60%, 98.20%)'
        });
    };
});

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

tl.from('#main-stagger', {
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

gsap.from(feature_card, {
  duration: 1,
  opacity: 0,
  y: 50,
  scrollTrigger:{
    trigger: '.whyContainer',
    scroller: 'body', 
    start: 'top 80%',
    end: 'bottom 50%',
    scrub: true
  }  
})

gsap.from('.whyContainer h2', {
    duration: 1,
    opacity: 0,
    y: 50,
    scrollTrigger:{
      trigger: '.whyContainer',
      scroller: 'body', 
      start: 'top 80%',
      end: 'bottom 50%',
      scrub: true
    }  
  })

gsap.to('.BestContainer h1',{
    transform: 'translateX(-55%)',
    scrollTrigger: {
        trigger: '.BestContainer',
        scroller:'body',
        start: 'top 20%',
        end: 'bottom 40%',
        scrub:4,
        pin:true
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

var tl2 = gsap.timeline()

tl2.to('#headline h1',{
    duration: 10,
    delay: 1,
    repeat: -1,
    
    transform: 'translateX(-290%)',
})


function LogoutBar(){
    console.log('LogoutBar');
    
}