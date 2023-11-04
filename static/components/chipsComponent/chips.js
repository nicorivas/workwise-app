import AbstractComponent from "../abstractComponent.js";

export default class ChipsComponent extends AbstractComponent {

    constructor(element, radio = false) {
        super(element);
        console.log(typeof element);
        if (typeof element === "string") {
            this.$element = jQuery(element);
        } else {
            this.$element = element;
        }
        if (this.$element.length === 0) {
            throw new Error(`Element not found: ${element}`);
        }
        this.$chips = this.$element.find(".chips__chip");
        this.radio = radio;
        this.selected = {};
        this.init();
    }

    init() {
        console.log("ChipsComponent.init()", this.$element);
        this.bindEvents();

        
        
        // Create object with chip id's as keys, and false as values
        for (let $chip of this.$chips) {
            this.selected[jQuery($chip).data("id")] = false;
        }

        console.log(this.selected)
        this.setState({
            "selected": this.selected
        });

    }

    bindEvents() {
        console.log("ChipsComponent.bindEvents()");

        this.bindEvent("click", this.chipClick, ".chips__chip");
    }

    chipClick(e) {
        console.log("ChipsComponent.itemClick()");
        e.stopPropagation();

        // Select the one we clicked. If this is a radio, deselect all.
        // We iterate even in case it is not a radio just to make it
        // easier to understand.
        let clickId = jQuery(e.currentTarget).data("id")
        for (let $chip of this.$chips) {
            let id = jQuery($chip).data("id");
            if (clickId === id) {
                this.selected[id] = !this.selected[id];
            } else {
                if (this.radio) {
                    this.selected[id] = false;
                }
            }
        }
        this.setState({"selected": this.selected});
    }

    render() {
        console.log("ChipsComponent.render()");
        // Show or hide selector items
        for (let $chip of this.$chips) {
            if (this.state.selected[jQuery($chip).data("id")]) {
                jQuery($chip).addClass("chips__chip--selected")
                jQuery($chip).attr("value","1")
            } else {
                jQuery($chip).removeClass("chips__chip--selected")
                jQuery($chip).attr("value","0")
            }
        }
    }
    
}