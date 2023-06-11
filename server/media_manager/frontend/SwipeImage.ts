import html from "./SwipeImage/Template.html"
import {getCookie} from "./Utils";
import * as events from "events";

class SwipeImage extends HTMLElement{
    private static template: HTMLTemplateElement;
    private container: HTMLDivElement;
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

    private dragStartX: number = null;
    private dragStartY: number = null;

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

        const self = this;
        this.container = this.shadowRoot.querySelector("div.media-container");
        this.container.addEventListener("dragstart", (e: DragEvent) => {self.onDragStart(e)});
        this.container.addEventListener("dragend", (e: DragEvent) => {self.onDragEnd(e)});

        this.built = true;
        if(this.source && this.mediaType) this.updateMedia();
    }

    async removeOldMedia(){
        if (this.mediaElem.tagName === "IMG") {
            this.mediaElem.remove();
        } else if(this.mediaElem.tagName==="SOURCE"){
            let videoTag = this.mediaElem.parentElement;
            this.mediaElem.remove();
            videoTag.remove();
        }
    }

    async updateMedia(){
        if(!this.built) return;
        console.log(this.source, this.mediaType);
        if(this.mediaElem.tagName !== "IMG" && this.mediaType === "image"){
            if(this.mediaElem.getAttribute("src")){
                let newImg = await this.preloadImage(this.source);
                await this.removeOldMedia();
                this.mediaElem = newImg;
                this.container.appendChild(newImg);
            }else{
                await this.removeOldMedia();
                this.mediaElem = document.createElement("img");
                this.container.appendChild(this.mediaElem);
            }
            this.mediaElem.setAttribute("draggable", "false");
            // this.mediaElem.addEventListener("dragstart", this.onDragStart);
            // this.mediaElem.addEventListener("dragend", this.onDragEnd);
        }else if(this.mediaType === "video"){
            await this.removeOldMedia();
            let videoTag = document.createElement("video");
            videoTag.setAttribute("autoplay", "");
            videoTag.setAttribute("loop", "");
            videoTag.setAttribute("controls", "");
            videoTag.setAttribute("draggable", "true");
            const self = this;
            videoTag.addEventListener("dragstart", (e: DragEvent) => {self.onDragStart(e)});
            videoTag.addEventListener("dragend", (e: DragEvent) => {self.onDragEnd(e)});
            this.container.appendChild(videoTag);

            this.mediaElem = document.createElement("source");
            videoTag.appendChild(this.mediaElem);
        }
        this.mediaElem.setAttribute("src", this.source);
    }

    async preloadImage(source: string): Promise<HTMLImageElement>{
        return new Promise((resolve, reject) => {
                let img = new Image();
                img.addEventListener('load', e => resolve(img));
                img.addEventListener('error', () => {
                    reject(new Error(`Failed to load image's URL: ${source}`));
                });
                img.src = source;
            });
    }

    async tagMedia(positivity: boolean){
        const url = window.location.pathname;
        let mediaId = this.source.split("/")[2];
        console.log(url, mediaId);

        let postData = JSON.stringify({
            image_id: mediaId,
            positive: positivity
        });

        let response = await fetch(url, {
            method: 'post',
            body: postData,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        let jsonResponse = await response.json();
        if(jsonResponse["next_image"] === null){
            location.reload();
            return;
        }
        let newSrc = jsonResponse["next_image"]["url"];
        let newMimeType = jsonResponse["next_image"]["mime-type"];
        this.source = newSrc;
        this.mediaType = newMimeType.split("/")[0];
        await this.updateMedia();
    }

    onDragStart(event: DragEvent){
        console.log("Drag start", event);
        this.dragStartX = event.clientX;
        this.dragStartY = event.clientY;
    }

    onDragEnd(event: DragEvent){
        console.log("Drag end", event);
        let deltaY = Math.abs(this.dragStartY-event.clientY);
        let deltaX = event.clientX - this.dragStartX;
        if(Math.abs(this.dragStartX-event.clientX) <= deltaY) return;
        if(Math.abs(deltaX) < 50) return;
        if(deltaX < 0){
            // Drag direction was left
            console.log("Dragged Left")
            console.log(this);
            this.tagMedia(false);
        }else{
            // Drag direction was right
            console.log("Dragged Right")
            console.log(this);
            this.tagMedia(true);
        }
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