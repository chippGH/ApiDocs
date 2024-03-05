async function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
    } else {
        // Use the 'out of viewport hidden text area' trick
        const textArea = document.createElement("textarea");
        textArea.value = text;

        // Move textarea out of the viewport so it's not visible
        textArea.style.position = "absolute";
        textArea.style.left = "-999999px";

        document.body.prepend(textArea);
        textArea.select();

        try {
            document.execCommand('copy');
        } finally {
            textArea.remove();
        }
    }
}


let languages = new Map();

let code_blocks = {};
$("div[id$='-code']").each((i, el) => {
    lang = el.id.slice(0, el.id.length - '-code'.length);
    languages.set(lang, el.title);

    pre_wrapper = el.firstChild;

    console.log(pre_wrapper);

    tooltip = document.createElement('div');
    tooltip.classList.add('copy-tooltip')
    copy_btn = document.createElement('button');
    copy_btn.classList.add('copy-code-button');
    copy_btn.innerText = 'copy';
    tooltip_text = document.createElement('span');
    tooltip_text.innerText = 'press to copy';
    tooltip_text.classList.add('copy-tooltip-text');

    tooltip.appendChild(tooltip_text);

    function wrapper(pre_wrapper, tooltip)
    {
        copy_btn.addEventListener('click', () => {
            var text = "";
            $(pre_wrapper).find("tr").each((i, el) => {
                if (i) text += '\n';
                var lineBuffer = "";
                $(el).find('.hljs-ln-code').each((i, el) => {
                    lineBuffer += el.innerText;
                })
                text += lineBuffer.replaceAll('\n', '');
            })

            copyToClipboard(text).then(() =>  tooltip.innerText = 'code copied!');
        });
        copy_btn.addEventListener('mouseout', () => tooltip.innerText = 'press to copy')
    }

    wrapper(pre_wrapper, tooltip_text);

    tooltip.appendChild(copy_btn);

    el.appendChild(tooltip);


    if(!code_blocks[lang]) code_blocks[lang] = [];
    code_blocks[lang] = code_blocks[lang].concat(el);
})

if (languages.size){
    let active_language = languages.keys().next().value;

    buttons_root = $(".language-selector-buttons")[0];

    code_blocks[active_language].map((el) => el.classList.add('active'));

    buttons = {};
    Array.from(languages.keys()).map((lang, i) => {
        let btn = document.createElement('button');

        if (lang === active_language) btn.classList.add('active');

        btn.id = `${lang}-selector`;
        btn.innerHTML = languages.get(lang);

        btn.addEventListener('click', () => {
            if (active_language === lang) return void null;
            buttons[active_language].classList.remove('active');
            code_blocks[active_language].map((el) => el.classList.remove('active'));

            btn.classList.add('active');
            code_blocks[lang].map((el) => el.classList.add('active'));
            active_language = lang;
        });
        buttons_root.appendChild(btn);

        buttons[lang] = btn;
    });
}

