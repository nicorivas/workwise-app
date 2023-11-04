import AbstractComponent from "../abstractComponent.js";

/**
 * Kebab component (dropdown menu with three vertical icons)
 * @class
 */
export default class KebabComponent extends AbstractComponent {

    /**
     * 
     * @param {string|jQuery} element 
     */
    constructor(element) {
        super(element);
        this.$button = this.$element.find(".kebab__button"); // Toggle button
        this.$menu = this.$element.find(".kebab__menu"); // Dropdown menu
        this.$itemTemplate = this.$element.find(".kebab__menu__item__template"); // Dropdown menu item
        this.$items = this.$element.find(".kebab__menu__item"); // Dropdown menu items
        this.init();
    }

    /**
     * @override
     */
    init() {
        this.bindEvents();
        this.setState({
            "open": false
        })
    }

    /**
     * @override
     */
    bindEvents() {
        this.bindEvent("click", this.buttonClicked, this.$button);
        this.bindEvent("click", this.itemClicked, this.$items);
        
        // Hide the dropdown when clicked outside
        // Only bind if it's not already bound
        if (!jQuery._data(document, ".kebabClickOutside")) {
            jQuery(document).on("click.kebabClickOutside", this.handleClickOutside.bind(this));
        }
    }

    getItemById(id) {
        return this.$items.filter(id);
    }

    handleClickOutside(e) {
        if (!jQuery(e.target).closest('.kebab').length) {
            this.hideDropdown();
        }
    }

    addItem(text, id=null) {
        console.log("KebabComponent.addItem()");
        let $item = this.$itemTemplate.clone().removeClass("kebab__menu__item__template").appendTo(this.$menu);
        $item.find(".kebab__menu__item__text").text(text);
        if (!id) id = text.toLowerCase().replace(" ", "-");
        $item.attr("id",id);
        return $item;
    }

    itemClicked(event) {
        /* Implement */
    }

    buttonClicked(event) {
        // Handle item click
        this.setState({"open": !this.state["open"]});
    }

    hideDropdown() {
        this.setState({"open": false});
    }

    render() {
        if (this.$items.length <= 1) {
            this.$menu.toggle(this.state["open"]);
        }
    }
    
}