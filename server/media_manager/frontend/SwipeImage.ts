import html from "./SwipeImage/Template.html"

class SwipeImage extends HTMLElement{
    private static template: HTMLTemplateElement;
    static {
        this.template = document.createElement("template");
        this.template.innerHTML = html;
    }
    static get observedAttributes() {
        return ['src', 'mime']
    }

    private built: boolean = null;
    private mediaType: string = null;
    private source: string = null;
    private mediaElem: HTMLElement = null;

    constructor() {
        super();
        this.attachShadow({mode: "open"});
        this.built = false;
        this.mediaType = "image";
    }

    connectedCallback() {
        if (this.built) return;

        this.shadowRoot.appendChild(SwipeImage.template.content.cloneNode(true));

        if (this.hasAttribute("src")) this.source = this.getAttribute("src");
        if (this.hasAttribute("mime")) this.mediaType = this.getAttribute("mime").split("/")[0];

        this.mediaElem = this.shadowRoot.querySelector("img");

        this.built = true;
        if(this.source && this.mediaType) this.updateMedia();
    }

    updateMedia(){
        if(!this.built) return;
        console.log(this.source, this.mediaType);
        if(this.mediaElem.tagName !== "img" && this.mediaType === "image"){
            this.mediaElem.remove();
            this.mediaElem = document.createElement("img");
            // this.shadowRoot.querySelector("div.media-container").appendChild(this.mediaElem);
            this.shadowRoot.appendChild(this.mediaElem);
        }else if(this.mediaElem.tagName !== "video" && this.mediaType === "video"){
            this.mediaElem.remove();
            // let container = this.shadowRoot.querySelector("div.media-container");
            let videoTag = document.createElement("video");
            videoTag.setAttribute("autoplay", "");
            videoTag.setAttribute("loop", "");
            videoTag.setAttribute("controls", "");
            this.shadowRoot.appendChild(videoTag);

            this.mediaElem = document.createElement("source");
            videoTag.appendChild(this.mediaElem);
        }
        this.mediaElem.setAttribute("src", this.source);
    }

    attributeChangedCallback(name: string, oldValue: string, newValue: string) {
        console.log("Attr changed!", name);
        if (name === "mime") {
            this.mediaType = newValue.split("/")[0];
        } else if (name === "src") {
            this.source = newValue;
        }

        if(name === "mime" || name === "src") this.updateMedia();
    }
}



customElements.define("swipe-image", SwipeImage);