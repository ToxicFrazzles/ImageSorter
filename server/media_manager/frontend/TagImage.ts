class TagImage extends HTMLElement{
    private shadow: ShadowRoot;
    private built: boolean;

    constructor() {
        super();
        this.shadow = this.attachShadow({mode:"open"});
        this.built = false;
    }

    connectedCallback(){

    }
}