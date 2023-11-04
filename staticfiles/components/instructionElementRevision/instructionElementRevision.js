import AbstractComponent from "../abstractComponent.js";
import ButtonComponent from "../buttonComponent/button.js";

export default class InstructionElementReviseComponent extends AbstractComponent {

    constructor(element, instruction = null) {
        super(element);
        // Elements
        this.$header = this.$element.find(".document-revision-element-header");
        this.$title = this.$element.find(".document-revision-element-title");
        this.$body = this.$element.find(".document-revision-element-body");
        this.$button = this.$element.find(".icon-button");
        // Parent
        this.instruction = instruction;
        // Define state
        this.state = {
            "id": this.$element.data("id"),
            "index": this.$element.data("index"),
            "hidden": this.$element.hasClass("instruction-element-revision--hidden"),
            "open": false,
            "selected": false,
            "status": "idle",
            "title": this.$title.text(),
        };
        // Others
        this.documentSectionIndex; // This is the index of the revision element in regards to the others.
        this.type = "REV";
        console.log(this.state);

        this.init();
    }

    init() {
        console.log("InstructionElementRevisionComponent.init()", this.$element);

        this.render();
        this.bindEvents();
    }

    bindEvents() {
        console.log("InstructionElementRevisionComponent.bindEvents()");

        this.$header.on("click", (event) => this.headerClick(event)) 
        this.$button.on("click", (event) => this.revise(event))
    }

    headerClick(event) {
        console.log("InstructionElementRevisionComponent.headerClick()", event, this.index);
        event.stopImmediatePropagation();

        this.instruction.closeElements(this);
        this.setState({
            "open": !this.state.open,
            "selected": !this.state.selected,
        });
        this.instruction.task.document.selectSection(this.documentSectionIndex, true);
    }

    load() {
        // AJAX call to get (or create!) the data of this revision
        console.log("InstructionElementRevisionComponent.load()")
        this.setState({"status": "loading"})

        // If we don't have an id it means that this element exists only in the DOM
        // and not in the database. We need to create it.
        if (this.state.id == null || this.state.id == undefined || this.state.id == "") {
            jQuery.ajax({
                url: `/instruction/api/instruction_element/create`,
                type: "POST",
                data: {
                    "type": this.type,
                    "name": this.state["title"],
                    "index": this.state["index"],
                    "instruction": this.instruction.id,
                    "mimesis_action": "./mimesis/library/project_charter/ReviseProjectCharterSection",
                    "document": this.instruction.task.document.state.id,
                    "document_section_index": this.documentSectionIndex,
                    "csrfmiddlewaretoken": Cookies.get('csrftoken')
                },
                success: (data) => {
                    data = JSON.parse(data);
                    let object = data[0];
                    this.setState({
                        "id": object.pk,
                        "status": "idle"
                    })
                },
                error: (data) => {
                    console.log("InstructionElementRevisionComponent.load(): error", data);
                    this.setState({"status": "error"})
                }
            });
        }

        /*
        jQuery.ajax({
            url: `/api/instruction_element_revision/${this.id}/`,
            type: "GET",
            success: (data) => {
                console.log("InstructionElementRevisionComponent.load(): success", data);
                this.setState({"status": "success"})
            },
            error: (data) => {
                console.log("InstructionElementRevisionComponent.load(): error", data);
                this.setState({"status": "error"})
            }
        });
        */
    }

    revise() {
        jQuery.ajax({
            url: `/instruction/${this.instruction.id}/element/${this.state.id}/revision_call`,
            type: "POST",
            data: {
                "csrfmiddlewaretoken": Cookies.get('csrftoken')
            },
            success: (data) => {
                console.log("InstructionElementRevisionComponent.revise(): success", data);
                this.setState({"status": "success"})
            },
            error: (data) => {
                console.log("InstructionElementRevisionComponent.revise(): error", data);
                this.setState({"status": "error"})
            }
        });
    }

    render() {
        console.log("InstructionElementRevisionComponent.render()");

        // Open or closed
        if (this.state["open"]) {
            this.$body.show();
        } else {
            this.$body.hide();
        }

        // Hidden
        this.$element.toggleClass("instruction-element-revision--hidden", this.state["hidden"]);

        // Selected
        this.$element.toggleClass("instruction-element-revision--selected", this.state["selected"]);

        // Title
        this.$title.text(this.state["title"])

        // ID
        this.$element.attr("data-id", this.state["id"])
    }

}