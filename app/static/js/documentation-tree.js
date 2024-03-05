let togglers = document.getElementsByClassName('tree-caret');
for (let i = 0; i < togglers.length; i++) {
    togglers[i].addEventListener('click', function () {
        this.parentElement.querySelector('.tree-node').classList.toggle('active');
        this.classList.toggle('opened');
    });
}
