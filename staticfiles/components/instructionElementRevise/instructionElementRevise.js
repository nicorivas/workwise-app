import AbstractComponent from "../abstractComponent.js";
import ButtonComponent from "../buttonComponent/button.js";

export default class InstructionElementReviseComponent extends AbstractComponent {

    constructor(element, instruction = null) {
        super(element);
        this.id = this.$element.data("id");
        // Parent
        this.instruction = instruction;
        // Define state
        this.state = {
            "status": "idle",
        };
        // Components
        this.button;

        this.init();
    }

    init() {
        console.log("InstructionElementReviseComponent.init()", this.$element);
        
        this.button = new ButtonComponent(this.$element.find(".button"), false);
        this.bindEvents();
    }

    bindEvents() {
        console.log("InstructionElementReviseComponent.bindEvents()");

        this.button.addFunction(this.revise, [this.instruction]);
    }

    async revise(instruction) {
        console.log("InstructionElementReviseComponent.revise()")
        // We loose context of this here, that's why we pass instruction as argument.
        // Iterate over document sections
        for (const [documentSectionIndex, documentSection] of instruction.task.document.sections.entries()) {
            // Duplicate revision element
            instruction.createRevision(documentSection, documentSectionIndex);
        }
        console.log("InstructionElementReviseComponent.revise(): instruction", instruction);
    }

    render() {
        console.log("InstructionElementReviseComponent.render()");
        // Propagate change of state to button
        this.button.setState(this.state);
    }

}