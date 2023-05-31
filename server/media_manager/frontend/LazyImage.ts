const intersectObserv = new IntersectionObserver(function(entries){
    for(const entry of entries){
        if(entry.isIntersecting && entry.target instanceof LazyImage){
            entry.target.inView();
        }
    }
});

const style = document.createElement("style");
style.innerHTML = `
:host {
    display: block;
}
img {
    width: 100%;
    height: 100%;
}
`;

class LazyImage extends HTMLElement{
    built: boolean;

    constructor() {
        super();
        this.attachShadow({mode: "open"});
        this.built = false;
    }

    connectedCallback(){
        if(this.built) return;

        intersectObserv.observe(this);
        this.shadowRoot.appendChild(style.cloneNode(true));
        // if(!this.style.minWidth) this.style.minWidth = "5px";
        // if(!this.style.minHeight) this.style.minHeight = "5px";

        this.built = true;
    }

    inView(){
        const img = document.createElement("img");
        img.src = this.getAttribute("src");
        this.shadowRoot.appendChild(img);
        intersectObserv.unobserve(this);
    }
}

customElements.define("lazy-img", LazyImage)