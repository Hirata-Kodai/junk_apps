(() => {
    const $doc = document;
    const $tab = $doc.getElementById('tab-js');
    const $nav = $tab.querySelectorAll('[data-nav]');
    const $content = $tab.querySelectorAll('[data-content]');
    const ACTIVE_CLASS = 'is-active';

    const init = () => {
        $content[0].style.display = 'block';
        $nav[0].classList.add('is-actve');  // 意味ないっぽい
    };
    init();

    const handleClick = (e) => {
        e.preventDefault();
        const $this = e.target;
        const $thisVal = $this.dataset.nav;
        [...$content].forEach((content) => {
            content.style.display = 'none';
        });
        [...$nav].forEach((nav) => {
            nav.classList.remove(ACTIVE_CLASS);
        });
        $thisContent = $tab.querySelectorAll('[data-content="' + $thisVal + '"]')[0];
        $thisContent.style.display = 'block';
        $thisNav = $tab.querySelectorAll('[data-nav="' + $thisVal + '"]')[0];
        $thisNav.classList.add(ACTIVE_CLASS);
    };
    [...$nav].forEach((nav) => {
        nav.addEventListener('click', (e) => handleClick(e));
    });
})();
