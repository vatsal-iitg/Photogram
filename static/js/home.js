console.log('home loaded')
ScrollReveal({
	// reset:true,
	distance:'40px',
	duration:2000,
	delay:500
  })
  
  ScrollReveal().reveal('.logo',{origin:'top'});
  ScrollReveal().reveal('.btn,.footer',{origin:'bottom'});
  ScrollReveal().reveal('.title',{origin:'left'});
  ScrollReveal().reveal('.sub-title',{origin:'right'});