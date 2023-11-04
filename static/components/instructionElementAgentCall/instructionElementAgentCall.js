import AbstractComponent from "../abstractComponent.js";
import ButtonComponent from "../buttonComponent/button.js";

export default class InstructionElementAgentCallComponent extends AbstractComponent {

    constructor(element, instruction = null) {
        super(element);
        if (this.$element.length === 0) {
            throw new Error(`Element not found: ${element}`);
        }
        if (typeof element === "string") {
            this.$element = jQuery(element);
        } else {
            this.$element = element;
        }
        this.id = this.$element.data("id");
        this.instruction = instruction;
        this.state = {
            "status": "idle",
        };
        this.button;
        this.agentCallFunctions = {
            "Generate Feedback Guidelines": this.agentCallWriteToDocument,
            "Write Project Charter": this.agentCallWriteToDocument,
            "Create meeting minutes": this.agentCallWriteToDocument,
            "Create job profile": this.agentCallWriteToDocument,
            "Crear planificación estratégica": this.agentCallWriteToDocument,
            "Evaluate pitch": this.agentCallWriteToDocument,
            "LinkedIn Post": this.agentCallWriteToFormat,
            "Project Charter Email": this.agentCallWriteToFormat,
            "Summary": this.agentCallWriteToFormat,
            "Meeting summary email": this.agentCallWriteToFormat,
            "LinkedIn job post": this.agentCallWriteToFormat,
        }
        this.init();
    }

    init() {
        this.button = new ButtonComponent(this.$element.find(".button"));
        this.bindEvents();
    }

    bindEvents() {
        this.button.clearFunctions();

        // The name of the instruction is used to find the function to call
        let instructionName = this.instruction.typeName.trim();
        if (!Object.keys(this.agentCallFunctions).includes(instructionName)) {
            throw new Error(`Function not found: ${instructionName}`);
        }
        let func = this.agentCallFunctions[this.instruction.typeName.trim()];
        this.button.addFunction(func, [this.instruction]);
    }

    addFunction(instruction) {
        console.log("InstructionElementAgentCallComponent.addFunction()");
    }

    render() {
        // Propagate change of state to button
        this.button.setState(this.state);
    }

    async agentCallWriteToFormat(instruction, event) {
        console.log("InstructionComponent.agentCallWriteToFormat()")
        let instruction_element_id = jQuery(event.currentTarget).closest(".instruction-element").data("id");
        let documentId = instruction.task.document.getId();
        try {
            if (instruction.task.document.state["format_open"] == false) {
                // If the format doesn't exist yet, create it
                console.log("InstructionComponent.agentCallWriteToFormat(): Format didn't exist")
                let data = await instruction.task.createDocument(instruction.typeName, true, documentId);
                documentId = data["document_id"]
            }
            try {
                await instruction.task.document.editorRead(documentId);
                instruction.task.document.stream(instruction, instruction_element_id);
            } catch (error) {
                console.error(error);
            }
        } catch (error) {
            console.error(error);
        }
        // We loose context of this here, that's why we pass instruction as argument.
        /*
        let instruction_element_id = jQuery(event.currentTarget).closest(".instruction-element").data("id");
        let documentId = instruction.task.document.getId();
        try {    
            let data = await instruction.task.createDocument(instruction.instructionTypeName, true, documentId);
            try {
                await instruction.task.document.read(data["document_id"]);
                instruction.task.document.stream(instruction, instruction_element_id);
            } catch (error) {
                console.error(error);
            }
        } catch (error) {
            console.error(error);
        }
        */
    }

    async agentCallWriteToDocument(instruction, event) {
        console.log("InstructionComponent.writeToDocument()")
        instruction.setState({"status":"running"});
        let instruction_element_id = jQuery(event.currentTarget).closest(".instruction-element").data("id");
        instruction.task.document.stream(instruction, instruction_element_id);
    }

}