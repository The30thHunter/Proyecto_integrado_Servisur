document.addEventListener('DOMContentLoaded', () => {
  const ticker = document.getElementById('ticker');
  if (ticker) {
    ticker.addEventListener('mouseenter', () => ticker.style.animationPlayState = 'paused');
    ticker.addEventListener('mouseleave', () => ticker.style.animationPlayState = 'running');
  }

  // pequeño tweak: añadir/remover sombra grande en action-card on hover (para navegadores sin :hover consistente)
  const actions = document.querySelectorAll('.action-card');
  actions.forEach(card => {
    card.addEventListener('mouseenter', () => card.classList.add('shadow-lg'));
    card.addEventListener('mouseleave', () => card.classList.remove('shadow-lg'));
  });
});
