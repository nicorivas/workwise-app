import AbstractComponent from "../abstractComponent.js";
import ChipsComponent from "../chipsComponent/chips.js";
import DropdownComponent from "../kebabComponent/kebab.js";
import InstructionElementTextInputComponent from "../instructionElementTextInput/instructionElementTextInput.js";
import InstructionElementAgentCallComponent from "../instructionElementAgentCall/instructionElementAgentCall.js";
import InstructionElementReviseComponent from "../instructionElementRevise/instructionElementRevise.js";
import InstructionElementRevisionComponent from "../instructionElementRevision/instructionElementRevision.js";

export default class InstructionComponent extends AbstractComponent{
    
    constructor(element, task) {
        super(element);
        
        // Parent
        this.task = task;
        
        // Elements
        this.$header = this.$element.find(".instruction__header");
        this.$body = this.$element.find(".instruction__body");
        this.$bodySeamless = this.$element.find(".instruction-body-seamless"); // TODO Fix
        
        // Components
        this.options = []; // Options dropdown
        this.instructionElements = []; // List of instruction elements
        
        // Data
        this.id = this.$element.data("id");
        this.step = this.$element.data("step");
        if (this.id == undefined) {
            throw new Error("InstructionComponent.load(): id is undefined");
        }
        this.typeName = this.$element.data("type-name"); // Name of instruction type
        
        // State
        this.state = {
            "loaded": true,
            "hidden": true,
            "open": false,
            "status": "idle",
            "selected": false
        }

        this.init();
    }

    init() {

        // Options dropdown
        if (this.$element.find(".kebab").length > 0) {
            this.options = new DropdownComponent(this.$element.find(".kebab"));
        }

        // Instruction element components

        // ... choices (chips)
        this.$element.find(".chips").each((index, element) => {
            new ChipsComponent(jQuery(element), this);
        })
        
        // ... and text input components
        this.$element.find(".instruction-element__text-input").each((index, element) => {
            let instructionElementTextInputComponent = new InstructionElementTextInputComponent(jQuery(element), this);
            this.instructionElements.push(instructionElementTextInputComponent);
        })

        // ... and agent call components
        this.$element.find(".instruction-element-agent-call").each((index, element) => {
            let instructionElementAgentCallComponent = new InstructionElementAgentCallComponent(jQuery(element), this);
            this.instructionElements.push(instructionElementAgentCallComponent);
        })

        // ... and revise components
        this.$element.find(".instruction-element-revise").each((index, element) => {
            let instructionElementReviseComponent = new InstructionElementReviseComponent(jQuery(element), this);
            this.instructionElements.push(instructionElementReviseComponent);
        })

        // ... and revision components
        this.$element.find(".instruction-element-revision").each((index, element) => {
            let instructionElementRevisionComponent = new InstructionElementRevisionComponent(jQuery(element), this);
            instructionElementRevisionComponent.documentSectionIndex = index-1;
            this.instructionElements.push(instructionElementRevisionComponent);
        })

        this.bindEvents();
        this.setState(this.state);
        this.hideAgentCall();
    }

    bindEvents() {
        this.bindEventToElement("click", this.headerClick, this.$header)
    }

    headerClick(event) {
        console.log("InstructionComponent.headerClick()", this, event)
        event.stopImmediatePropagation();

        if (this.task) {
            // Hide all elements
            this.task.closeInstructions();
        }

        if (this.step == 2) {
            // If this is a format, then try to open the format (if it exists)
            this.select();
            this.task.document.openFormatByName(this.typeName);
        } else {
            // Change state of this element.
            this.setState({
                "open": !this.state.open,
                "selected": !this.state.selected
            });    
        }
    }

    deselect() {
        console.log("InstructionComponent.deselect()")
        this.setState({
            "selected":false,
            "open":false
        })
    }

    select() {
        console.log("InstructionComponent.select()")
        this.setState({
            "selected":true,
            "open":true
        })
    }

    show() {
        this.$element.show();
    }

    hide() {
        this.$element.hide();
    }

    collapse() {
        this.$body.hide();
    }

    expand() {
        this.$body.show();
    }

    open() {
        this.setState({"open":true});
    }

    createRevision(documentSection=null, documentSectionIndex=null) {
        console.log("InstructionComponent.createRevision()",documentSection,documentSectionIndex)

        // Add element to DOM.
        // To add the element, with clone it from the template.
        // The template is part of the html template and has that specific id.
        let $revision = this.$element.find("#instruction-element-revision-template").clone()
        $revision.appendTo(this.$bodySeamless);

        // Create component, pass the element just created as argument.
        let revision = new InstructionElementRevisionComponent($revision, this);
        this.instructionElements.push(revision);

        // Set index (position of render)
        let index = 0;
        if (documentSection) {
            index = documentSection.header.index;
        }
        revision.documentSectionIndex = documentSectionIndex;
        revision.setState({
            "index": index,
            "status": "loading",
            // Even if we are loading, we can get the title of the section
            // from the data that document holds.
            "title": this.task.document.getSectionHeader(documentSection),
        });
        revision.load();
    }

    closeElements(except) {
        // Close all elements
        for (let instructionElement of this.instructionElements) {
            if (instructionElement !== except) {
                instructionElement.setState({
                    "open":false,
                    "selected":false,
                });
            }
        }
    }

    hideAgentCall() {
        this.$element.find(".instruction-element-agent-call").hide();
    }

    showAgentCall() {
        this.$element.find(".instruction-element-agent-call").show();
    }

    render() {
        if (this.state["status"] == "running") {
            this.$element.addClass("instruction--running");
        } else {
            this.$element.removeClass("instruction--running");
            // Propagate end of state to all elements
            for (let instructionElement of this.instructionElements) {
                instructionElement.setState({"status":"idle"});
            }
        }

        // Open or closed
        this.$element.toggleClass("instruction--open", this.state["open"])

        // Selected
        this.$element.toggleClass("instruction--selected", this.state["selected"])

        this.$body.toggle(this.state["open"]);

    }

}