import AbstractComponent from "../abstractComponent.js";
import KebabComponent from "../kebabComponent/kebab.js";

/**
 * Table component. Uses DataTables to handle table.
 * 
 * @extends AbstractComponent
 * @class
 */
export default class TableComponent extends AbstractComponent {

    /**
     * 
     * @param {string|jQuery} element 
     */
    constructor(element, fetchUrl=null) {
        super(element);
        this.$table = this.$element.find(".table__table");
        this.table = new DataTable("#"+this.$element.attr("id")+"__table",{
            info: false,
            ordering: true,
            paging: false,
            searching: false,
        });
        this.fetchUrl = fetchUrl;
        this.kebabs = []
        this.init();
        this.state = {
            "empty": false,
        }
    }

    /**
     * @override
     */
    init() {
        // Create Kebab components for each row, if there are.
        this.$table.find(".kebab").each((i, kebab) => {
            let kebabComponent = new KebabComponent(jQuery(kebab));
            this.kebabs.push(kebabComponent);
            kebabComponent.addItem("Remove");
            kebabComponent.addItem("Delete");
        })
        if (this.table.rows().data().length == 0) {
            this.setState({"empty": true});
        };
        this.bindEvents();
    }

    /**
     * @override
     */
    bindEvents() {
        /* Handled by DataTables */
    }

    fetch(id) {
        console.log("TableComponent.fetch()", id);
        if (!this.fetchUrl) {
            throw "TableUrl not set";
        }
        jQuery.ajax({
            url: `${this.fetchUrl}`,
            type: "GET",
            success: (result) => {
                console.log("result")
                this.$element.find("#project-context-table__table").html(result);
                this.init();
            },
            error: (error) => {
                console.error("TableComponent.fetch()", error);
            }
        })
    }

    /**
     * @override
     */
    render() {
        this.$table.toggle(!this.state["empty"]);
    }
    
}