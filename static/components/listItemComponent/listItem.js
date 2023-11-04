import AbstractComponent from "../abstractComponent.js";

export default class ListItemComponent extends AbstractComponent{
    constructor(element, text=null, id=null) {
        super(element)
        this.$text = this.$element.find(".project-menu-item-text");
        this.selected = false;
        this.state = {
            "selected": false,
        }
        if (!text) {
            this.state["text"] = this.$text.text();
        } else {
            this.state["text"] = text
        }
        if (!id) {
            this.state["id"] = this.$element.data("id");
        } else {
            this.state["id"] = id;
        }
        this.init();
    }

    init() {
        console.log("ListItemComponent.init()")
        this.setState(this.state);
    }

    render() {
        this.$element.toggleClass("selected", this.state.selected);
        this.$text.text(this.state.text);
        this.$element.attr("data-id", this.state.id);
    }
}