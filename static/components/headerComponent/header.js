import AbstractComponent from "../abstractComponent.js";
import IconButtonComponent from "../iconButtonComponent/iconButton.js";

export default class HeaderComponent extends AbstractComponent {
    constructor(element) {
        super(element);
        console.log("HeaderComponent.constructor()")
        this.init();
        this.helpButton;
    }

    init() {
        console.log("HeaderComponent.init()")
        this.loadComponents();
    }

    loadComponents() {
        this.helpButton = new IconButtonComponent("#header__help");
        this.notButton = new IconButtonComponent("#header__not");
        this.notButton = new IconButtonComponent("#header__not");
    }

    render() {

    }
}