import AbstractComponent from '../abstractComponent.js';
import SelectorComponent from '../selectorComponent/selector.js';
import DocumentComponent from '../documentComponent/document.js';
import InstructionComponent from '../instructionComponent/instruction.js';
import InstructionSidebarComponent from '../instructionSidebarComponent/instructionSidebar.js';

export default class TaskComponent extends AbstractComponent {
    
    constructor($element) {
        super($element);
        // Components
        this.id = jQuery($element).data("id");
        this.instructions = [];
        this.document;
        this.init();
    }

    init() {
        // Initialize instructions
        let $instructions = this.$element.find(".instruction");
        for (const $instruction of $instructions) {
            this.instructions.push(new InstructionComponent(jQuery($instruction), this));
        }

        // Initialize documents
        this.document = new DocumentComponent(".document", this);

        window.navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
            this.loadMediaRecorder(new MediaRecorder(stream));
        });
    }

    hideInstruction(index) {
        this.instructions[index].hide();
    }

    hideInstructions() {
        for (const instruction of this.instructions) {
            instruction.hide();
        }
    }

    showInstruction(index) {
        this.instructions[index].show();
    }

    showInstructions(step=null) {
        for (const instruction of this.instructions) {
            if ((step != null && instruction.step == step) || step == null) {
                instruction.show();
            }
        }
    }

    openInstruction(index) {
        this.instructions[index].open();
    }

    openInstructions() {
        for (const instruction of this.instructions) {
            instruction.open();
        }
    }

    closeInstruction(index) {
        this.instructions[index].close();
    }

    closeInstructions() {
        for (const instruction of this.instructions) {
            instruction.close();
        }
    }

    selectInstruction(index) {
        this.instructions[index].select();
    }

    deselectInstruction(index) {
        this.instructions[index].deselect();
    }

    deselectInstructions() {
        /* Deselect all instructions */
        for (const instruction of this.instructions) {
            instruction.deselect();
        }
    }

    createDocument(name="New document", is_format=false, parent_document_id=null) {
        //path("create/", DocumentCreateView.as_view(), name="create")
        let url = "/document/create/";
        let taskId = this.$element.data("id");
        let dataPost = {
            "task_id": taskId,
            "name": name,
            "is_format": is_format,
            "parent_document_id": parent_document_id,
            "csrfmiddlewaretoken": Cookies.get('csrftoken')
        }
        return new Promise((resolve, reject) => { 
            jQuery.ajax({
                url: url,
                type: "POST",
                data: dataPost,
                success: (data) => {
                    console.log("TaskView.createDocument() success", data);
                    resolve(data);
                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                    reject(err);
                },
            })
        });
    }

    loadMediaRecorder(mediaRecorder) {
        for (let instruction of this.instructions) {
            for (let instructionElement of instruction.instructionElements) {
                if (instructionElement.type == "TXT") {
                    instructionElement.loadMediaRecorder(mediaRecorder);
                }
            }
        }
    }
}