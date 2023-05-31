// Lazy load any media file

import html from "./LazyMedia/StyleTemplate.html";

class LazyMedia extends HTMLElement {
    static styleTemplate: HTMLTemplateElement;
    static {
        this.styleTemplate = document.createElement("template");
        this.styleTemplate.innerHTML = html;
    }
    static intersectObserv = new IntersectionObserver(function (entries) {
        for (const entry of entries) {
            if (entry.isIntersecting && entry.target instanceof LazyMedia) {
                entry.target.inView();
            }
        }
    });

    static get observedAttributes() {
        return ['src', 'mime', 'w', 'h']
    }

    private built: boolean;
    private mediaType: string;
    private source: string;
    private mediaElem: HTMLElement;

    constructor() {
        super();
        this.attachShadow({mode: "open"});
        this.built = false;
        this.mediaType = "image";
    }

    connectedCallback() {
        if (this.built) return;

        LazyMedia.intersectObserv.observe(this);
        this.shadowRoot.appendChild(LazyMedia.styleTemplate.content.cloneNode(true));

        if (this.hasAttribute("src")) this.source = this.getAttribute("src");
        if (this.hasAttribute("mime")) this.mediaType = this.getAttribute("mime").split("/")[0];

        this.built = true;
    }

    inView() {
        if (this.mediaType === "image") {
            this.mediaElem = document.createElement("img");
            this.mediaElem.setAttribute("src", this.source);
        }
        this.shadowRoot.appendChild(this.mediaElem);
        LazyMedia.intersectObserv.unobserve(this);
    }

    attributeChangedCallback(name: string, oldValue: string, newValue: string) {
        console.log("Attr changed!", name);
        if (name === "mime") {
            this.mediaType = newValue.split("/")[0];
        } else if (name === "src") {

        }
    }
}

customElements.define("lazy-media", LazyMedia)