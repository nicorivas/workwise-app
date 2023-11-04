import AbstractComponent from "../abstractComponent.js";
import listItemComponent from "../listItemComponent/listItem.js";

export default class ListComponent extends AbstractComponent {
    constructor(element) {
        super(element);
        this.items = [];
        this.$items = this.$element.find(".list-item:not(.list-item--template)");
        this.$itemTemplate = this.$element.find(".list-item--template");
        this.init();
    }

    init() {
        console.log("ListComponent.init()")
        // Create listItem components for every $item
        this.$items.each((index, item) => {
            this.items.push(new listItemComponent(jQuery(item)));
        });
    }

    clickItemById(id) {
        console.log("ListComponent.clickItemById(id)", id);
        for (const item of this.items) {
            if (item.state["id"] === id) {
                item.$element.click();
                break;
            }
        }
    }

    clickItem(index) {
        this.items[index].$element.click();
    }

    selectItem(item) {
        console.log("ListComponent.selectItem($item)",item);
        // This items
        this.items.forEach((item) => {item.setState({"selected":false})});
        // Select clicked item
        item.setState({"selected":true});
    }

    removeItem(id) {
        // Get item with specific data-id attribute
        console.log("ListComponent.removeItem(id)", id);
        let $item = this.$element.find(`.list-item[data-id="${id}"]`);
        $item.remove();
        this.$items = this.$element.find(".list-item");
        this.clickItem(0);
    }

    renameItem(id, name) {
        console.log("ListComponent.renameItem(id, name)", id, name);
        let $item = this.$element.find(`.list-item[data-id="${id}"]`);
        $item.find(".project-menu-item-text").text(name);
    }

    addItem(item) {
        // Logic to add an item to the list
        console.log("Adding an item to the list...");
        this.$element.find(".list-group").first().prepend(item);
        this.refresh();
        htmx.process(this.$element.find(".list-group").first()[0]);
    }

    newItem(text, id=null) {
        let $item = this.$itemTemplate.clone().removeClass("list-item--template").appendTo(this.$element.find(".list-group"));
        let item = new listItemComponent(jQuery($item), text, id)
        this.items.push(item);
        this.refresh();
        return item;
    }

    refresh() {
        // Logic to refresh the list
        console.log("Refreshing the list...");
        this.$items = this.$element.find(".list-item");
        //this.bindEvents();
    }

    render() {

    }
    
    // ... other component-related methods ...
}