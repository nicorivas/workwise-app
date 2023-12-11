import InstructionElement from "../instructionElement/instructionElement.js";
import InstructionElementFeedback from "../instructionElementFeedback/instructionElementFeedback.js";
import ButtonComponent from "../buttonComponent/button.js";
import IconButtonComponent from "../iconButtonComponent/iconButton.js";

export default class InstructionElementTextInputComponent extends InstructionElement {

    constructor(element, instruction = null, view = null) {
        super(element);
        console.log("InstructionElementTextInputComponent.constructor()", element, instruction, view);
        this.id = this.$element.data("id");
        this.type = this.$element.data("type");
        this.$feedback = this.$element.find(".instruction-element-feedback-wrapper");
        // Parent
        this.instruction = instruction;
        // Define state
        this.state = {
            "status": "idle",
            "has_transcription": false,
        };
        this.record = this.$element.find("#btn-start-record").length > 0;
        this.audioChunks = [];
        // Components
        this.feedback = null;
        this.rerecordRecordButton = null;
        this.startRecordButton = null;
        this.startRecordIconButton = null;
        this.stopRecordButton = null;
        this.restartRecordButton = null;
        this.textField = null;
        this.RECORD_TIME = 4 * 60;
        this.time = this.RECORD_TIME;
        this.timer = null;
        this.init();
    }

    init() {
        console.log("InstructionElementTextInputComponent.init()");
        this.createComponents();
        this.bindEvents();
    }

    createComponents() {
        if (this.record) {
            this.timer = jQuery('#timer');
            this.startRecordButton = new ButtonComponent(this.$element.find('#btn-start-record'), false, false);
            this.startRecordIconButton = new ButtonComponent(this.$element.find('#btn-start-record-icon'), false, false);
            this.stopRecordButton = new ButtonComponent(this.$element.find('#btn-stop-record'), false, false);
            this.restartRecordButton = new ButtonComponent(this.$element.find('#btn-restart-record'), false, false);
            this.rerecordRecordButton = new ButtonComponent(this.$element.find('#btn-rerecord-record'), false, false);
        }
        if (this.$feedback.length > 0) {
            this.feedback = new InstructionElementFeedback(this.$feedback, this);
        }
        this.textField = this.$element.find(`#instruction-text-${this.id}`);
        if (this.textField.text().length > 0) {
            this.setState({"has_transcription": true});
        }
    }

    bindEvents() {
        console.log("InstructionElementTextInputComponent.bindEvents()");
        if (this.record) {
            this.startRecordButton.bindEvent("click", this.startRecordHandler, null, this);
            this.startRecordIconButton.bindEvent("click", this.startRecordHandler, null, this);
            this.stopRecordButton.bindEvent("click", this.stopRecordHandler, null, this);
            this.restartRecordButton.bindEvent("click", this.restartRecordHandler, null, this);
            this.rerecordRecordButton.bindEvent("click", this.rerecordRecordHandler, null, this);
        }
        if (this.$feedback.length > 0) {
            this.textField.on('blur', (event) => this.textFieldInputHandler(event, this));
        }
    }

    render() {
        // Propagate change of state to button
        if (this.record) {
            jQuery(".instruction-element__text-input").show();
            jQuery(".instruction-element__text-input__indicator").hide();
            if (this.state.status == "recording") {
                jQuery(".record-icon").show();
                jQuery(".record-icon").addClass("record-icon--recording");
                jQuery(".record-icon").find(".pulse").show();
                jQuery(".timer").show();
                this.$title.show();
                this.startRecordButton.$element.hide();
                this.stopRecordButton.$element.show();
                this.restartRecordButton.$element.show();
                this.rerecordRecordButton.$element.hide();
                this.instruction.hideAgentCall();
                this.textField.hide();
            } else if (this.state.status == "transcribing") {
                jQuery(".record-icon").hide();
                jQuery(".instruction-element__text-input").hide();
                jQuery(".instruction-element__text-input__indicator").show();
                this.textField.hide();
            } else if (this.state.status == "idle")  {
                if (this.state.has_transcription) {
                    jQuery(".record-icon").hide();
                    jQuery(".timer").hide();
                    this.$title.hide();
                    this.rerecordRecordButton.$element.show();
                    this.startRecordButton.$element.hide();
                    this.textField.show();
                    this.instruction.showAgentCall();
                } else {
                    jQuery(".record-icon").show();
                    jQuery(".timer").show();
                    this.$title.show();
                    this.rerecordRecordButton.$element.hide();
                    this.startRecordButton.$element.show();
                    this.textField.hide();
                    this.instruction.hideAgentCall();
                }
                jQuery(".record-icon").removeClass("record-icon--recording");
                jQuery(".record-icon").find(".pulse").hide();
                this.stopRecordButton.$element.hide();
                this.restartRecordButton.$element.hide();
            }
        } else {
            jQuery(".instruction-element__text-input__indicator").hide();
        }
    }
    
    // -- - - - -- -- -- - -

    loadMediaRecorder(mediaRecorder) {
        this.mediaRecorder = mediaRecorder;
    }

    startRecord(component) {

        component.mediaRecorder.ondataavailable = (e) => {
            component.audioChunks.push(e.data);
        };

        return new Promise((resolve, reject) => {
            
            component.mediaRecorder.onstop = (event) => {
                let blob = new Blob(component.audioChunks, { 'type': 'audio/ogg; codecs=opus' });
                resolve(blob);
            };

            // Handle the case where there is an error with the recording
            component.mediaRecorder.onerror = event => reject(event.error);
            component.mediaRecorder.start();      

        });

    }

    startRecordHandler(component) {
        if (component.state.status != "recording") {
            component.setState({"status":"recording"})
            component.startRecord(component).then(blob => {
                component.resetTimer(component);
                if (component.state.status != "restarting") {
                    component.transcribe(blob);
                }
            });
            component.startTimer(component);
        }
    }

    stopRecordHandler(component) {
        component.mediaRecorder.stop();
    }

    restartRecordHandler(component) {
        component.setState({"status":"idle"})
        component.mediaRecorder.stop();
    }

    rerecordRecordHandler(component) {
        component.startRecordHandler(component);
    }

    resetTimer(component) {
        clearInterval(component.timerInterval);
        component.time = component.RECORD_TIME;
        component.updateTimer(component);
    }

    updateTimer(component) {
        const minutes = Math.floor(component.time / 60);
        let seconds = component.time % 60;
        seconds = seconds < 10 ? '0' + seconds : seconds;
        component.timer.find("h3").text(`${minutes}:${seconds}`);
    }

    startTimer(component) {
        component.timerInterval = setInterval(() => {
            component.time--;
            component.updateTimer(component);
            if (component.time <= 0) {
                component.timer.find("h3").text("¡Se acabó el tiempo!");
                component.mediaRecorder.stop();
            }
        }, 1000);
    }

    transcribe(blob) {
        this.setState({"status":"transcribing"})
        let fd = new FormData();
        fd.append('audio', blob, 'audio.ogg');
        fd.append('csrfmiddlewaretoken', Cookies.get("csrftoken"));
        fd.append('task', this.instruction.task.id);

        jQuery.ajax({
            type: 'POST',
            url: `/instruction/${this.instruction.id}/element/${this.id}/transcribe`,
            data: fd,
            processData: false,
            contentType: false,
            success: (successData) => {
                this.textField.text(successData.transcript);
                this.audioChunks = [];
                this.setState({"status":"idle", "has_transcription": true})
            },
            error: (xhr, status, error) => {
                this.showError("Error en transcripción");
                this.restartRecordHandler(this);
                this.setData({"transcribing": false});
            }
        })
    }

    textFieldInputHandler(event, component) {
        console.log("InstructionElementTextInputComponent.textFieldInputHandler()", event, component, this);
        this.feedback.call();
    }
}